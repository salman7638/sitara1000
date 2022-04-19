# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductType(models.Model):
    _name = 'op.stock.product.type'
    _description = 'Product Type'
    
    
    name = fields.Char('Product Type', required=True, translate=True)
    color = fields.Integer('Color')
    sequence = fields.Integer('Sequence', help="Used to order the 'All Operations' kanban view")
    
    
    def get_action_op_stock_product(self):
        pass
    

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    op_type_id = fields.Many2one('op.stock.product.type', string="OP Type")
