# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    premium_id = fields.Many2one('op.premium.factor', string='Premium')
    standard_price = fields.Float(string="Standard price")
    list_price = fields.Float(compute='_compute_sum')

    @api.depends('standard_price', 'premium_id')
    def _compute_sum(self):
        for line in self:
            line.list_price = line.standard_price + (line.premium_id.percent * (line.standard_price / 100))

    
    # @api.constrains('premium_id')
    # def _check_premium(self):
    #     for line in self:
    #         if line.premium_id:
    #             line.list_price = line.standard_price + (line.premium_id.percent * (line.standard_price/100))
     
    
   
    can_be_property = fields.Boolean(string="Can be Property", compute='_compute_can_be_property',
        store=True, readonly=False, help="Specify whether the product can be selected in a property.")
    
    property_id = fields.Many2one('op.property', string='Property')
    property_location_id = fields.Many2one('op.property.location', string='Location')
    property_type_id = fields.Many2one('op.property.type')
    property_unit_type_id = fields.Many2one('op.property.unit.type', string='Unit Type')
    plot_type = fields.Selection([
        ('plot file', 'Plot File')
    ], default='plot file')
    plot_file = fields.Char(string="Plot File")
    property_amenities_ids = fields.Many2many("op.property.amenities", string="Amenities")
    property_unit_feature_group_ids = fields.Many2many("op.property.unit.feature.group", string="Feature Groups", )
    

    plot_size = fields.Char(string='Plot Size')
    road_width = fields.Char(string='Road Width')                       
    plot_area_marla = fields.Char(string='Plot Area in Marla')
    plot_area_sft = fields.Char(string='Plot Area in sft')
    

    
    property_owner_ids = fields.One2many('product.template.partner.line', 'product_tmpl_id', string='Owner Lines', copy=True, auto_join=True)
    property_feature_line = fields.One2many('product.template.feature.line', 'product_tmpl_id', string='Feature Lines', copy=True, auto_join=True)

    stage_id = fields.Many2one('product.template.stage', string='Stage', ondelete='restrict', compute='_compute_categ',
                               tracking=True, index=True, copy=False, group_expand='_read_group_stage_ids',
                               domain="[('id', '=', stages)]")
    stages = fields.Many2many("product.template.stage", string="Stages", )

    @api.constrains('categ_id')
    def _check_categ(self):
        for line in self:
            if line.categ_id:
                line.stages = line.categ_id.stage_ids

    def _compute_categ(self):
        for line in self:
            line.stages = line.categ_id.stage_ids

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', self.categ_id.stage_ids.ids)]
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    
            
    #@api.model_create_multi
    #def create(self, vals_list):
    #    for vals in vals_list:
            # When creating an expense product on the fly, you don't expect to
            # have taxes on it
   #         if vals.get('can_be_property', False) and not self.env.context.get('import_file'):
   #             vals.update({'supplier_taxes_id': False})
   #     return super(ProductTemplate, self).create(vals_list)

    @api.depends('type')
    def _compute_can_be_property(self):
        self.filtered(lambda p: p.type not in ['consu', 'service']).update({'can_be_property': False})

class ProductTemplateFeatureLine(models.Model):
    _name = "product.template.feature.line"
    _description = "Product Template Feature Line"
    _order = 'product_tmpl_id, id'
    
    product_tmpl_id = fields.Many2one('product.template', string='Product', required=True, ondelete='cascade', index=True, copy=False)
    property_unit_feature_group_id = fields.Many2one('op.property.unit.feature.group', string='Feature Group', readonly=False, ondelete='restrict', index=True, copy=False)
    property_unit_feature_id = fields.Many2one('op.property.unit.feature', string='Feature')
    property_feature_evaluation_type = fields.Selection(related='property_unit_feature_id.evaluation_type')
    
    property_unit_feature_item_id = fields.Many2one('op.property.unit.feature.item', string='Item', domain="[('property_unit_feature_id','=',property_unit_feature_id)]")
    property_unit_feature_item_select = fields.Boolean(string='Yes/No', ondelete=False)
    property_unit_feature_item = fields.Char(string='Value')
    
    name = fields.Char(string='Name', compute='_compute_name', store=True)
    
    @api.depends('property_unit_feature_item_id','property_unit_feature_item_select','property_unit_feature_item')
    def _compute_name(self):
        for feature in self:
            if feature.property_unit_feature_item_id.id:
                feature.name = feature.property_unit_feature_item_id.name
            elif feature.property_unit_feature_item_select:
                feature.name = feature.property_unit_feature_item_select
            elif feature.property_unit_feature_item:
                feature.name = feature.property_unit_feature_item
                
    
class ProductTemplatePartnerLine(models.Model):
    _name = "product.template.partner.line"
    _description = "Product Template Partner Line"
    _order = 'product_tmpl_id, date_owner, id'
    
    product_tmpl_id = fields.Many2one('product.template', string='Product', required=True, ondelete='cascade', index=True, copy=False)
    name = fields.Char(string='Name',compute='_compute_name', store=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    date_owner = fields.Datetime(string='Ownership Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now, help="Ownership date property of customers.")

        
    @api.depends('product_tmpl_id','partner_id')
    def _compute_name(self):
        for partner in self:
            if partner.partner_id:
                partner.name = str(partner.partner_id.name) + ' - ' + str(partner.product_tmpl_id.name)
                