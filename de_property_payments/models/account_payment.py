# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    order_id = fields.Many2one('sale.order', string='Order')
    installment_id = fields.Many2one('order.installment.line', string='Order Installment')
    
    type = fields.Selection([
        ('token','Token'),
        ('fee', 'Fee'),
        ('book', 'Booking'),
        ('allott', 'Allottment'),
        ('installment', 'Installment'),
        ], string='Type')
    
    
    def action_cancel(self):
        for line in self:
            if line.installment_id:
                line.installment_id.update({
                    'remarks': 'Pending',
                    'amount_paid': line.installment_id.amount_paid - line.amount,
                })
            if line.order_id.amount_paid==0:
               line.order_id.update({
                   'state': 'draft'
               }) 
            res = super(AccountPayment, line).action_cancel()
            return  res
    
    
    
