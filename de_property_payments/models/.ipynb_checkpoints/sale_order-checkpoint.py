# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_view_payments(self):
        self.ensure_one()
        return {
         'type': 'ir.actions.act_window',
         'binding_type': 'object',
         'domain': [('order_id', '=', self.id)],
         'multi': False,
         'name': 'Payments',
         'target': 'current',
         'res_model': 'account.payment',
         'view_mode': 'tree,form',
        }
           
    def get_bill_count(self):
        count = self.env['account.payment'].search_count([('order_id', '=', self.id)])
        self.bill_count = count
        
    bill_count = fields.Integer(string='Payments', compute='get_bill_count')
    amount_paid = fields.Float(string='Amount Paid', compute='_compute_property_amount')
    amount_residual = fields.Float(string='Amount Due')
    received_percent = fields.Float(string='Percentage')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('booked', 'Booked'),
        ('sale', 'Allotted'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')    
    installment_line_ids = fields.One2many('order.installment.line', 'order_id' , string='Installment')
    

    def _compute_property_amount(self):
        for line in self:
            total_paid_amount=0
            residual_amount=0
            payments = self.env['account.payment'].search([('order_id','=',self.id)])
            for pay in payments:
                if pay.type!='fee':
                    total_paid_amount += pay.amount
            residual_amount = self.amount_total - total_paid_amount 
            line.update({
                'amount_paid':  total_paid_amount,
                'amount_residual':  residual_amount,
            })
            
    def action_register_payment(self):
        return {
            'name': ('Register Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'register.pay.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_sale_id': self.id, 'default_partner_id': self.partner_id.id},
        }
    
    def action_confirm_booking(self):
        for line in self:
            line.update({
                'state': 'booked',
            })
            for line_product in line.order_line:
                line_product.product_id.update({
                    'state': 'booked',
                })
    
    def action_register_allottment(self):
        for line in self:
            line.update({
                'state': 'sale',
            })
            for line_product in line.order_line:
                line_product.product_id.update({
                    'state': 'un_posted_sold',
                })
    
    def action_generate_installment(self):
        return {
            'name': ('Register Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'register.installment.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_sale_id': self.ids},
        }
    
    
class OrderInstallmentLine(models.Model):
    _name = 'order.installment.line'
    _descrption='Order Installment Line'
    
    
    name = fields.Char(string='Description')
    date = fields.Date(string='Due Date')
    payment_date = fields.Date(string='Payment Date')
    amount_paid = fields.Float(string='Amount Paid')
    amount_residual = fields.Float(string='Amount Due')
    remarks = fields.Char(string='Remarks')
    order_id = fields.Many2one('sale.order', string='Order')
    
    