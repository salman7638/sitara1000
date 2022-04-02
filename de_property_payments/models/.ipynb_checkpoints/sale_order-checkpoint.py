# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

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
    
    @api.constrains('amount_residual')
    def _check_amount_residual(self):
        for line in self:
            if line.amount_residual<=0:
                for order_line in line.order_line:
                    order_line.product_id.update({
                         'state':  'posted_sold',
                    })            
            if line.amount_paid >= ((line.amount_residual+line.amount_paid)/100) * 10:
                line.received_percent = 10
                line.action_confirm_booking()
            if line.amount_paid >= ((line.amount_residual+line.amount_paid)/100) * 25:
                line.received_percent = 25
                line.action_register_allottment()  
                   
           
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
    installment_created=fields.Boolean(string='Installment Generated')

    def _compute_property_amount(self):
        for line in self:
            total_paid_amount=0
            residual_amount=0
            for order_line in  self.order_line:
                for pay_line in order_line.product_id.payment_ids:
                    pay_line.update({
                        'order_id': self.id,
                        'type': 'token',
                    })
            payments = self.env['account.payment'].search([('order_id','=',self.id),('state','in',('draft','posted'))])
            for pay in payments:
                if pay.type!='fee':
                    total_paid_amount += pay.amount  
            residual_amount = self.amount_total - total_paid_amount 
            line.update({
                'amount_paid':  total_paid_amount,
                'amount_residual':  residual_amount,
            })
            
    def action_register_payment(self):
        amount_calc=0
        type='installment'
        installment_line=0
        if self.state=='draft':
            type='book'
            total_amount=self.amount_residual + self.amount_paid
            amount_calc=(((total_amount)/100)*10)
        if self.state=='booked': 
            amount_calc=(((self.amount_residual+self.amount_paid)/100)*25) - self.amount_paid
            type='allott'
        if self.state=='sale' and self.installment_line_ids:
            for installment_line in self.installment_line_ids:
                if  installment_line.amount_residual > 0:
                    amount_calc=installment_line.amount_residual
                    installment_line=installment_line.id
                    break
        return {
            'name': ('Register Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'register.pay.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_sale_id': self.id, 
                        'default_partner_id': self.partner_id.id, 
                        'default_token_amount':  amount_calc,
                        'default_type': type,
                        'default_installment_id': installment_line,
                       },
        }
    
    def action_confirm_booking(self):
        for line in self:
            line.update({
                'state': 'booked',
            })
            for line_product in line.order_line:
                line_product.product_id.update({
                    'state': 'booked',
                    'commission_amount': line_product.comission_amount,
                    'discount_amount': line_product.discount,
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
    
 
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    comission_amount = fields.Float(string='Comission Amount')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) - line.comission_amount
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
    

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
    
    