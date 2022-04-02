
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class RegisterPayWizard(models.TransientModel):
    _name = "register.pay.wizard"
    _description = "Register Pay wizard"
    

    token_amount = fields.Float(string='Amount', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date(string='Date', required=True, default=fields.date.today())
    allow_amount = fields.Float(string='Allow Amount')
    installment_id = fields.Many2one('order.installment.line', string='Installment')
    check_number = fields.Char(string='Check Number')
    type = fields.Selection([
        ('fee', 'Fee'),
        ('book', 'Booking'),
        ('allott', 'Allottment'),
        ('installment', 'Installment'),
        ], string='Type', required=True)
    
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type','in',('bank','cash'))])
    sale_id = fields.Many2one('sale.order', string='Order')
    
    @api.onchange('installment_id')
    def onchange_installment(self):
        for line in self:
            if line.installment_id:
                line.token_amount = line.installment_id.amount_residual
    
    
    @api.constrains('amount_residual')
    def _check_state(self):
        for line in self:
            if line.amount_residual<=0:
                for order_line in line.order_line:
                    order_line.update({
                         'state':  'posted_sold',
                    })   
    
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
            'installment_id': self.installment_id.id,
            }
        record_pay = self.env['account.payment'].sudo().create(vals)
        for order_line in self.sale_id.order_line:
            payment_list = []
            for pay_line in order_line.product_id.payment_ids:
                payment_list.append(pay_line.id)
            if record_pay:
                payment_list.append(record_pay.id)
            order_line.product_id.payment_ids=payment_list
        if self.type=='book':
            fee_amount=0
            for o_line in self.sale_id.order_line:
                fee_amount=o_line.product_id.categ_id.process_fee 
            if  fee_amount > 0:    
                vals = {
                 'partner_id': self.partner_id.id,
                 'date': self.date,
                 'journal_id': self.journal_id.id,
                 'amount': fee_amount,
                 'ref': self.check_number,
                 'payment_type': 'inbound',
                 'order_id': self.sale_id.id,
                 'type': 'fee',
                 }
                record = self.env['account.payment'].sudo().create(vals)
        if self.type=='allott':
            fee_amount=0
            for o_line in self.sale_id.order_line:
                fee_amount=o_line.product_id.categ_id.allottment_fee
            if  fee_amount > 0:   
                vals = {
                 'partner_id': self.partner_id.id,
                 'date': self.date,
                 'journal_id': self.journal_id.id,
                 'amount': fee_amount,
                 'ref': self.check_number,
                 'payment_type': 'inbound',
                 'order_id': self.sale_id.id,
                 'type': 'fee',
                 }
                record = self.env['account.payment'].sudo().create(vals)                              
        if self.installment_id:            
            status= 'Partial Payment'
            installment_amount = self.installment_id.amount_residual - self.token_amount 
            if installment_amount > 0:
                self.installment_id.update({
                'amount_paid': self.installment_id.amount_paid + self.token_amount,
                'payment_date':self.date,
                'remarks': status ,
                })    
                self.installment_id.update({
                'amount_residual': self.installment_id.amount_residual - self.token_amount
                })
            elif installment_amount==0:
                self.installment_id.update({
                'remarks': 'Paid' ,
                })             
            elif installment_amount < 0:
                self.installment_id.update({
                'amount_paid': self.installment_id.amount_paid + self.installment_id.amount_residual,
                'payment_date':self.date,
                'remarks': 'Paid' ,
                })    
                self.installment_id.update({
                'amount_residual': 0
                })
                remaining_amount = self.token_amount - self.installment_id.amount_residual  
                for installment_line in self.sale_id.installment_line_ids:
                    if installment_line.amount_residual > 0:
                        if installment_line.amount_residual < remaining_amount:
                            installment_line.update({
                            'amount_paid': installment_line.amount_paid + installment_line.amount_residual,
                            'payment_date':self.date,
                            'remarks': 'Paid' ,
                            })    
                            installment_line.update({
                            'amount_residual': 0
                            })    
                        elif installment_line.amount_residual == remaining_amount:    
                            installment_line.update({
                            'amount_paid': installment_line.amount_paid + installment_line.amount_residual,
                            'payment_date':self.date,
                            'remarks': 'Paid' ,
                            })    
                            installment_line.update({
                            'amount_residual': 0
                            })
                            break
                        elif installment_line.amount_residual > remaining_amount:   
                            installment_line.update({
                            'amount_paid': installment_line.amount_paid + remaining_amount,
                            'payment_date':self.date,
                            'remarks': 'Partial Payment' ,
                            })    
                            installment_line.update({
                            'amount_residual': installment_line.amount_residual - installment_line.amount_paid 
                            })
                            break
                            
                            