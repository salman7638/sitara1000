
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AssignTokenWizard(models.TransientModel):
    _name = "assign.token.wizard"
    _description = "Assign Token wizard"
    

    token_amount = fields.Float(string='Token Amount', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date(string='Date', required=True, default=fields.date.today())
    check_number = fields.Char(string='Check Number')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type','in',('bank','cash'))])
    product_ids = fields.Many2many('product.product', string='Plot')
    
    def action_assign_token(self):
        vals = {
            'partner_id': self.partner_id.id,
            'date': self.date,
            'journal_id': self.journal_id.id,
            'amount': self.token_amount,
            'ref': self.check_number,
            'type':  'token',
            'payment_type': 'inbound',
            }
        record = self.env['account.payment'].sudo().create(vals)
        
        for line in self.product_ids:
            line.update({
                'payment_ids':  record.ids,
                'state': 'reserved',
            })
            if not line.partner_id:
                line.update({
                'partner_id':  self.partner_id.id,
                })    
        
        