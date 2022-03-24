# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero, float_repr
from odoo.tools.misc import clean_context, format_date
from collections import defaultdict, OrderedDict
from odoo.addons.website.tools import get_video_embed_code

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]

class OPPropertyType(models.Model):
    _name = 'op.property.type'
    _description = 'Property Type'
    _order = "id desc"
    
    name = fields.Char(string='Name', required=True)

class OPPropertyType(models.Model):
    _name = 'op.property.unit.type'
    _description = 'Property Unit Type'
    _order = "id desc"
    
    name = fields.Char(string='Name', required=True)
    property_type_id = fields.Many2one('op.property.type', string='Property Type')
    
    unit_feature_ids = fields.One2many('op.property.unit.feature', 'property_unit_type_id', string='Features', copy=True)
    feature_count = fields.Integer(string='Property Features', compute='_count_unit_features')
    
    property_feature_ids = fields.Many2many("op.property.feature", string="Features")
    
    def _count_unit_features(self):
        f = 0
        for feature in self.unit_feature_ids:
            f += 1
        self.feature_count = f

class OPPropertyFeatureField(models.Model):
    _name = 'op.property.feature.field'
    _description = 'Feature Fields'
    _order = 'id desc'
    
    name = fields.Char(string='Name', required=True)
    evaluation_type = fields.Selection([
        ('boolean','Yes/No'),
        ('selection','List of Values'),
        ('text','Single Value'),
    ], default='boolean', string='Evaluation Type')
    
    feature_item_ids = fields.One2many('op.property.feature.field.item', 'property_feature_field_id', string='Feature Item', copy=True)
    
class OPPropertyFeatureFieldItem(models.Model):
    _name = 'op.property.feature.field.item'
    _description = 'Feature Fields'
    _order = 'id desc'
    
    property_feature_field_id = fields.Many2one('op.property.feature.field', string='Items', readonly=False, ondelete='restrict', index=True, copy=False)
    name = fields.Char(string='Value', required=True)

    
class OPPropertyFeature(models.Model):
    _name = 'op.property.feature'
    _description = 'Property Feature'
    _order = "id desc"
    
    name = fields.Char(string='Name', required=True)
    property_feature_line = fields.One2many('op.property.feature.line', 'property_feature_id', string='Feature', copy=True)
    display_type = fields.Selection([
        ('global','Global'),
        ('property','Property'),
        ('unit','Unit')
    ], default='global', string='Display Type')
    
class OPPropertyFeatureLine(models.Model):
    _name = 'op.property.feature.line'
    _description = 'Property Feature Line'
    _order = "id desc"
    
    property_feature_id = fields.Many2one('op.property.feature', string='Featuree', readonly=False, ondelete='restrict', index=True, copy=False)
    property_feature_field_id = fields.Many2one('op.property.feature.field', string='Feature')
    property_feature_evaluation_type = fields.Selection(related='property_feature_field_id.evaluation_type')
    
    property_feature_field_item_id = fields.Many2one('op.property.feature.field.item', string='Values', domain="[('property_feature_field_id','=',property_feature_field_id)]")
    property_feature_field_item_selecction = fields.Boolean(string='Yes/No', ondelete=False)
    property_feature_field_item_value = fields.Char(string='Value')
    
    name = fields.Char(string='Name', required=True)
    
class OPPropertyUnitFeature(models.Model):
    _name = 'op.property.unit.feature'
    _description = 'Property Feature'
    _order = "id desc"
    
    property_unit_type_id = fields.Many2one('op.property.unit.type', string='Unit Type', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)
    property_feature_id = fields.Many2one('op.property.feature', string='Feature')
    name = fields.Char(string='Name')
    sequence = fields.Integer(string='Sequence', default=10)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    
class OPPropertyAmenities(models.Model):
    _name = 'op.property.amenities'
    _description = 'Property Amenities'
    _order = "id desc"
    
    name = fields.Char(string='Name', required=True)
    
class OPPropertyPolicy(models.Model):
    _name = 'op.property.policy'
    _description = 'Property Policy'
    _order = "id desc"
    
        
class OPProperty(models.Model):
    _name = 'op.property'
    _description = 'Property'
    _order = "id desc"
    
    name = fields.Char(related='partner_id.name', string='Property Name', required=True, store=True, readonly=False)
    sequence = fields.Integer(help='Used to order properties', default=10)
    parent_id = fields.Many2one('op.property', string='Parent Property', index=True)
    child_ids = fields.One2many('op.property', 'parent_id', string='Child Properties')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_image = fields.Binary(related='partner_id.image_1920', string="Property Image", readonly=False)
    
    street = fields.Char(compute='_compute_address', inverse='_inverse_street')
    street2 = fields.Char(compute='_compute_address', inverse='_inverse_street2')
    zip = fields.Char(compute='_compute_address', inverse='_inverse_zip')
    city = fields.Char(compute='_compute_address', inverse='_inverse_city')
    state_id = fields.Many2one(
        'res.country.state', compute='_compute_address', inverse='_inverse_state',
        string="Fed. State", domain="[('country_id', '=?', country_id)]"
    )
    
    country_id = fields.Many2one('res.country', compute='_compute_address', inverse='_inverse_country', string="Country")
    email = fields.Char(related='partner_id.email', store=True, readonly=False)
    phone = fields.Char(related='partner_id.phone', store=True, readonly=False)
    mobile = fields.Char(related='partner_id.mobile', store=True, readonly=False)
    website = fields.Char(related='partner_id.website', readonly=False)
    
    property_type_id = fields.Many2one('op.property.type', string='Property Type')
    property_area = fields.Integer(string='Property Area', size=10)
    no_of_blocks = fields.Integer(string='No. of Blocks', size=10,)
    
    property_amenities_ids = fields.Many2many("op.property.amenities", string="Amenities")
    property_division_ids = fields.Many2many("op.property.division", string="Divisions")
    
    property_image_ids = fields.One2many('op.property.image', 'property_id', string="Extra Property Media", copy=True)
    
    #optional fields
    has_room = fields.Selection(CATEGORY_SELECTION, string="Has Room", default="no", required=True,)

    def _compute_address(self):
        for property in self.filtered(lambda property: property.partner_id):
            address_data = property.partner_id.sudo().address_get(adr_pref=['contact'])
            if address_data['contact']:
                partner = property.partner_id.browse(address_data['contact']).sudo()
                property.update(property._get_company_address_update(partner))
   
    def _get_company_address_field_names(self):
        """ Return a list of fields coming from the address partner to match
        on company address fields. Fields are labeled same on both models. """
        return ['street', 'street2', 'city', 'zip', 'state_id', 'country_id']

    def _get_company_address_update(self, partner):
        return dict((fname, partner[fname])
                    for fname in self._get_company_address_field_names())
    
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('partner_id'):
            self.clear_caches()
            return super(OPProperty, self).create(vals)
        partner = self.env['res.partner'].create({
            'name': vals['name'],
            'is_company': True,
            'image_1920': vals.get('logo'),
            'email': vals.get('email'),
            'phone': vals.get('phone'),
            'website': vals.get('website'),
            'country_id': vals.get('country_id'),
        })
        # compute stored fields, for example address dependent fields
        partner.flush()
        vals['partner_id'] = partner.id
        self.clear_caches()
        property = super(OPProperty, self).create(vals)
        # The write is made on the user to set it automatically in the multi company group.
        #self.env.user.write({'company_ids': [Command.link(property.id)]})
        
        return property
    
    def _inverse_street(self):
        for property in self:
            property.partner_id.street = property.street

    def _inverse_street2(self):
        for property in self:
            property.partner_id.street2 = property.street2

    def _inverse_zip(self):
        for property in self:
            property.partner_id.zip = property.zip

    def _inverse_city(self):
        for property in self:
            property.partner_id.city = property.city

    def _inverse_state(self):
        for property in self:
            property.partner_id.state_id = property.state_id

    def _inverse_country(self):
        for property in self:
            property.partner_id.country_id = property.country_id

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id.country_id:
            self.country_id = self.state_id.country_id
    
    
class PropertyImage(models.Model):
    _name = 'op.property.image'
    _description = "Property Image"
    _inherit = ['image.mixin']
    _order = 'sequence, id'

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)

    image_1920 = fields.Image(required=True)

    property_id = fields.Many2one('op.property', "Property", index=True, ondelete='cascade')
    video_url = fields.Char('Video URL', help='URL of a video for showcasing your property.')
    embed_code = fields.Html(compute="_compute_embed_code", sanitize=False)

    can_image_1024_be_zoomed = fields.Boolean("Can Image 1024 be zoomed", compute='_compute_can_image_1024_be_zoomed', store=True)

    @api.depends('image_1920', 'image_1024')
    def _compute_can_image_1024_be_zoomed(self):
        for image in self:
            image.can_image_1024_be_zoomed = image.image_1920 and tools.is_image_size_above(image.image_1920, image.image_1024)

    @api.depends('video_url')
    def _compute_embed_code(self):
        for image in self:
            image.embed_code = get_video_embed_code(image.video_url)

    @api.constrains('video_url')
    def _check_valid_video_url(self):
        for image in self:
            if image.video_url and not image.embed_code:
                raise ValidationError(_("Provided video URL for '%s' is not valid. Please enter a valid video URL.", image.name))
                
    @api.model_create_multi
    def create(self, vals_list):
        """
            We don't want the default_product_tmpl_id from the context
            to be applied if we have a product_variant_id set to avoid
            having the variant images to show also as template images.
            But we want it if we don't have a product_variant_id set.
        """
        context_without_template = self.with_context({k: v for k, v in self.env.context.items() if k != 'default_property_id'})
        normal_vals = []
        variant_vals_list = []

        for vals in vals_list:
            if 'default_property_id' in self.env.context:
                variant_vals_list.append(vals)
            else:
                normal_vals.append(vals)

        return super().create(normal_vals) + super(PropertyImage, context_without_template).create(variant_vals_list)

class OPPropertyDevision(models.Model):
    _name = "op.property.division"
    _description = "Property Devisions"
    #_parent_name = "division_id"
    #_parent_store = True
    _order = 'complete_name'
    _rec_name = 'complete_name'

    name = fields.Char('Name', required=True)
    complete_name = fields.Char("Full Name", compute='_compute_complete_name', recursive=True, store=True)
    active = fields.Boolean('Active', default=True, help="By unchecking the active field, you may hide a division without deleting it.")
    usage = fields.Selection([
        ('view', 'Group'),
        ('block', 'Block'),
        ], string='Division Type',
        default='normal', index=True, required=True,)
    
    division_id = fields.Many2one('op.property.division', 'Parent Division', index=True, ondelete='cascade', help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent location.")
    child_ids = fields.One2many('op.property.division', 'division_id', 'Contains')
    #child_internal_division_ids = fields.Many2many('op.property.division', string='Internal locations amoung descendants',      compute='_compute_child_internal_division_ids', recursive=True, help='This location (if it\'s internal) and all its descendants filtered by type=Internal.')
    comment = fields.Html('Additional Information')
    
    @api.depends('name', 'division_id.complete_name')
    def _compute_complete_name(self):
        for division in self:
            if division.division_id:
                division.complete_name = '%s/%s' % (division.division_id.complete_name, division.name)
            else:
                division.complete_name = division.name
                
    @api.depends('child_ids.usage', 'child_ids.child_internal_division_ids')
    def _compute_child_internal_division_ids(self):
        # batch reading optimization is not possible because the field has recursive=True
        for div in self:
            div.child_internal_division_ids = self.search([('id', 'child_of', div.id)])