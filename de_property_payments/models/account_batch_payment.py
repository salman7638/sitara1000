# -*- coding: utf-8 -*-
from odoo import models, fields, api, _




class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'
    
    order_id = fields.Many2one('sale.order', string='Order')
    
    
    
    
