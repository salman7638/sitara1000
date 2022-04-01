
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class RegisterPayWizard(models.TransientModel):
    _name = "register.pay.wizard"
    _description = "Register Pay wizard"
    

    token_amount = fields.Float(string='Amount', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date(string='Date', required=True, default=fields.date.today())
    installment_id = fields.Many2one('order.installment.line', string='Installment', domain=[('order_id','=',)])
    check_number = fields.Char(string='Check Number')
    type = fields.Selection([
        ('fee', 'Fee'),
        ('book', 'Booking'),
        ('allott', 'Allottment'),
        ('installment', 'Installment'),
        ], string='Type', required=True)
    
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type','in',('bank','cash'))])
    sale_id = fields.Many2one('sale.order', string='Order')
    
    def action_confirm(self):
        vals = {
            'partner_id': self.partner_id.id,
            'date': self.date,
            'journal_id': self.journal_id.id,
            'amount': self.token_amount,
            'ref': self.check_number,
            'payment_type': 'inbound',
            'order_id': self.sale_id.id,
            'type': self.type,
            }
        record = self.env['account.payment'].sudo().create(vals)
        
            
        
        