# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    order_id = fields.Many2one('sale.order', string='Order')
    type = fields.Selection([
        ('fee', 'Fee'),
        ('book', 'Booking'),
        ('allott', 'Allottment'),
        ('installment', 'Installment'),
        ], string='Type')
    
    
    
    
