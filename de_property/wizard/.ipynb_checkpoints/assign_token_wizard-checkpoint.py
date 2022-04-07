
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta

class AssignTokenWizard(models.TransientModel):
    _name = "assign.token.wizard"
    _description = "Assign Token wizard"
    

    token_amount = fields.Float(string='Token Amount', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date(string='Date', required=True, default=fields.date.today())
    check_number = fields.Char(string='Check Number')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type','in',('bank','cash'))])
    date_reservation = fields.Date(string='Date of Reservation', required=True, default=fields.date.today() )
    booking_validity = fields.Date(string='Booking Validity', required=True, default=fields.date.today()+ timedelta(4) )
    date_validity = fields.Date(string='Date Validity', required=True, default=fields.date.today()+timedelta(30) )
    product_ids = fields.Many2many('product.product', string='Plot')
    
    def action_assign_token(self):
        total_plot = 0
        for order_count in self.product_ids:
            total_plot += 1 
        for line in self.product_ids:
            vals = {
                'partner_id': self.partner_id.id,
                'date': self.date,
                'journal_id': self.journal_id.id,
                'amount': (self.token_amount/total_plot) ,
                'ref': self.check_number ,
                'type':  'token' ,
                'payment_type': 'inbound' ,
                }
            record = self.env['account.payment'].sudo().create(vals) 
            record.action_post()      
            line.update({
                'payment_ids':  record.ids,
                'state': 'reserved',
                'date_validity': self.date_validity ,
                'booking_validity': self.booking_validity,
                'date_reservation': self.date_reservation ,
            })
            if not line.partner_id:
                line.update({
                'partner_id':  self.partner_id.id,
                'cnic': self.partner_id.nic,    
                })    
        
        