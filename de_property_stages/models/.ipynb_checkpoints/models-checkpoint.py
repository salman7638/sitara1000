# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplateStage(models.Model):
    _name = 'product.template.stage'
    _description = 'Product Stage'
    name = fields.Char(string="Name")
    
class ProductCategoryInherite(models.Model):
    _inherit = 'product.category'
    _description = 'Product Category'
    stage_ids = fields.Many2many('product.template.stage', string="Stages")