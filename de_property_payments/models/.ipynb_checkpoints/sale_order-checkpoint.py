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
                       
    def get_bill_count(self):
        count = self.env['account.payment'].search_count([('order_id', '=', self.id)])
        self.bill_count = count
        
    bill_count = fields.Integer(string='Payments', compute='get_bill_count')
    amount_paid = fields.Float(string='Total Amount Paid', compute='_compute_property_amount')
    booking_amount_residual = fields.Float(string='Booking Amount Due')
    allotment_amount_residual = fields.Float(string='Allotment Amount Due')
    installment_amount_residual = fields.Float(string='Installment Amount Due')
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
    processing_fee_submit = fields.Boolean(string='Processing Fee Submitted')
    membership_fee_submit = fields.Boolean(string='Membership Fee Submitted')
    installment_line_ids = fields.One2many('order.installment.line', 'order_id' , string='Installment')
    installment_created=fields.Boolean(string='Installment Generated')

    
    @api.depends('amount_paid','amount_residual','installment_amount_residual','booking_amount_residual','allotment_amount_residual','received_percent')
    def _compute_property_amount(self):
        for line in self:
            total_paid_amount=0
            residual_amount=0
            if line.amount_residual<=0:
                for order_line in line.order_line:
                    order_line.product_id.update({
                         'state':  'posted_sold',
                    })
            for order_line in  line.order_line:
                commission_amount = order_line.comission_amount
                if order_line.commission_type=='percent':
                    commission_amount = (order_line.price_unit/100) * order_line.comission_amount
                order_line.product_id.update({
                    'commission_amount': commission_amount ,
                    'discount_amount': (order_line.price_subtotal/100) * order_line.discount ,
                })
                for pay_line in order_line.product_id.payment_ids:
                    pay_line.update({
                        'order_id': line.id,
                    })
            payments = self.env['account.payment'].search([('order_id','=',line.id),('state','in',('draft','posted'))])
            for pay in payments:
                if pay.type!='fee':
                    total_paid_amount += pay.amount  
            residual_amount = line.amount_total - total_paid_amount
            tot_booking_amount = (((line.amount_total)/100) * 10) 
            booking_amount = (((line.amount_total)/100) * 10) - total_paid_amount
            allotment_amount = (((line.amount_total)/100) * 15)
            if booking_amount <=0:
                allotment_amount = (((line.amount_total)/100) * 15) - (total_paid_amount - tot_booking_amount)
            advance_amount = (((line.amount_total)/100) * 25)
            installment_amount = (((line.amount_total)/100) * 75)
            if booking_amount <=0 and allotment_amount<=0: 
                remaining_amount=total_paid_amount - advance_amount
                installment_amount = (((line.amount_total)/100) * 75) - (total_paid_amount - advance_amount)
#             if booking_amount > 0:
#                line.update({
#                    'state': 'draft',
#                })
#                for line_prod in line.order_line:
#                     line_prod.product_id.update({
#                         'state': 'available',
#                         'partner_id': False,
#                     })                    
            if line.amount_paid > advance_amount:
                diff_advance_amt = total_paid_amount - advance_amount
                installment_amount = (((line.amount_total)/100) * 75) - diff_advance_amt
            line.update({
                'amount_paid':  total_paid_amount,
                'amount_residual':  residual_amount,
                'booking_amount_residual':  booking_amount if booking_amount > 0 else 0,
                'allotment_amount_residual': allotment_amount if allotment_amount > 0 else 0,
                'installment_amount_residual':installment_amount if installment_amount > 0 else 0, 
            })
            if line.amount_paid >= ((line.amount_total)/100) * 10:
                line.received_percent = 10
                line.action_confirm_booking()
            if line.amount_paid >= ((line.amount_total)/100) * 25:
                line.received_percent = 25
                line.action_register_allottment()

            
    def action_register_payment(self):
        amount_calc=0
        allow_amount=0
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
                    allow_amount=installment_line.amount_residual
                    installment_line=installment_line.id
                    break
        process_fee_submit=False   
        member_fee_submit=False
        if self.processing_fee_submit==True:
            process_fee_submit=True
        if self.membership_fee_submit==True:
            member_fee_submit=True    
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
                        'default_processing_fee_submit': process_fee_submit,
                        'default_membership_fee_submit': member_fee_submit,
                        'default_installment_id': installment_line,
                       },
        }
    
    def action_confirm_booking(self):
        for line in self:
            if line.amount_paid >= ((line.amount_total)/100) * 10:
                line.update({
                    'state': 'booked',
                })
                for line_product in line.order_line:
                    commission_amount = line_product.comission_amount
                    if line_product.commission_type=='percent':
                        commission_amount = (line_product.price_unit/100) * line_product.comission_amount
                    line_product.product_id.update({
                        'state': 'booked',
                        'partner_id': line.partner_id.id,
                        'booking_id': self.id,
                        'commission_amount': commission_amount,
                        'discount_amount':  (line_product.price_subtotal/100)* line_product.discount,
                    })
    
    def action_register_allottment(self):
        for line in self:
            if line.amount_paid >= ((line.amount_total)/100) * 25:
                line.update({
                    'state': 'sale',
                })
                for line_product in line.order_line:
                    commission_amount = line_product.comission_amount
                    if line_product.commission_type=='percent':
                        commission_amount = (line_product.price_unit/100) * line_product.comission_amount
                    line_product.product_id.update({
                        'state': 'un_posted_sold',
                        'booking_id': self.id,
                        'commission_amount': commission_amount,
                        'partner_id': line.partner_id.id,
                        'discount_amount': (line_product.price_subtotal/100)* line_product.discount,
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
    
    comission_amount = fields.Float(string='Commission')
    commission_type = fields.Selection([
        ('amount', 'Amount'),
        ('percent', 'Percentage'),
        ], string='Commission Type', default='amount')   
    

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','comission_amount')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = (line.price_unit) * (1 - (line.discount or 0.0) / 100.0) 
            commission_amount = line.comission_amount
            if line.commission_type=='percent':
                commission_amount = (line.price_unit/100) * line.comission_amount    
#             price = price - commission_amount
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
    total_amount = fields.Float(string='Total Amount')
    payment_date = fields.Date(string='Payment Date')
    amount_paid = fields.Float(string='Amount Paid')
    amount_residual = fields.Float(string='Amount Due')
    remarks = fields.Char(string='Remarks')
    order_id = fields.Many2one('sale.order', string='Order')
    
    