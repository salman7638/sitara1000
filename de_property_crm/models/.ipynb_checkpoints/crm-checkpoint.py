# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    property_type_id = fields.Many2one('op.property.type', string='Property Type')
    property_unit_type_id = fields.Many2one('op.property.unit.type', string='Unit Type', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)
    property_id = fields.Many2one('op.property', string='Property')
    product_id = fields.Many2one('product.product', string='Unit')
    property_unit_area = fields.Integer(string='Unit Area', size=10)
    
    city = fields.Char(string='City')
    
    property_count = fields.Integer(string='Property Count')
    
    def assign_matched_properties(self):
        t = 0
        
    def action_view_matched_property(self):
        t = 0
