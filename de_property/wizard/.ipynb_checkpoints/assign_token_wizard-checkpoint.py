
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AssignTokenWizard(models.TransientModel):
    _name = "assign.token.wizard"
    _description = "Assign Token wizard"
    

    token_amount = fields.Float(string='Token Amount', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    product_ids = fields.Many2many('product.product', string='Plot')
    
    def action_assign_token(self):
        vals = {
            'partner_id': self.partner_id.id,            
            'date': self.date,
            'journal_id': self.env['account.journal'].search([('company_id','=',self.employee_id.company_id.id),('name','=','Blank Journal')], limit=1).id,
            'amount': self.amount,
            'ref': self.description,
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            }
        record = self.env['account.payment'].sudo().create(vals)
        
        for line in self.product_ids:
            line.update({
                'payment_ids':  record.ids,
                'state': 'reserved',
            })
        
        