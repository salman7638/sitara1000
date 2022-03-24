# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplateStage(models.Model):
    _name = 'product.template.stage'
    _description = 'Product Stage'

    name = fields.Char(string="Name")
    sequence = fields.Integer(string="Sequence")
    stages_category = fields.Selection([
        ("draft", "Draft"),
        ("in progess", "In Progress"),
        ("close", "Close")
    ], default='draft', tracking=True,
        string="Stages Category")
    security_group = fields.Many2one('res.groups', string="Security Group")

    
class ProductCategoryInherite(models.Model):
    _inherit = 'product.category'
    _description = 'Product Category'
    stage_ids = fields.Many2many('product.template.stage', string="Stages")

