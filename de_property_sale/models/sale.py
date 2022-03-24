# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def _default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id')
    
    is_property_order = fields.Boolean("Created In App Property")
    order_status = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('reserved', 'Reserved'),
        ('sale', 'Sale Order'),
        ('refund', 'Booking Cancelled'),
        ('expire', 'Booking Expired'),
        ('cancel', 'Cancelled'),
    ], string="Order Status", default='draft', compute='_compute_property_order_status', store=True)
    
    payment_plan_id = fields.Many2one('sale.payment.plan', 'Payment Plan', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    payment_line = fields.One2many('sale.order.payment.line', 'order_id', string='Order Lines', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True, auto_join=True)

    product_id = fields.Many2one('product.product', string='Property', tracking=True, domain="[('can_be_property', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", ondelete='restrict', required=True, readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', compute='_compute_from_product_id_company_id',
        store=True, default=_default_product_uom_id, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one('uom.category', readonly=True, string="UoM Category")
    unit_amount = fields.Float("Unit Amount", compute='_compute_from_product_id_company_id', store=True, copy=True, digits='Product Price', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    tax_ids = fields.Many2many('account.tax', 'property_sale_tax', 'sale_id', 'tax_id', compute='_compute_from_product_id_company_id', store=True, domain="[('company_id', '=', company_id), ('type_tax_use', '=', 'sale')]", string='Taxes', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', check_company=True)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.depends('state','is_property_order')
    def _compute_property_order_status(self):
        # TODO replace multiple assignations by one write?
        status = 'draft'
        for order in self:
            if order.is_property_order:
                if order.state in ('draft','sent'):
                    status = order.state
                else:
                    status = order.order_status
            else:
                status = order.order_status
            order.order_status = status
                    #if sum(order.payment_line.mapped('amount_residual')) == 0:
                    #    status == 'sale'
                    #else:
                    #    status == 'reserved'
                
    @api.onchange('payment_plan_id')
    def onchange_payment_plan_id(self):
        data = {}
        order_lines = [(5, 0, 0)]
        amount_total = self.amount_total
        amount_installment = 0
        date_due = self.date_order
        for line in self.payment_plan_id.line_ids:
            date_due = self.date_order + relativedelta(days=line.days)
            if line.payment_plan_id.type == 'percent':
                amount_installment = amount_total * (line.amount/100)
            data = {
                'sequence': line.sequence,
                'name': line.name,
                'amount_installment': amount_installment,
                'date_due': date_due,
                'is_downpayment': line.is_downpayment,
                }

            order_lines.append((0, 0, data))
        self.payment_line = order_lines
    
    @api.depends('product_id', 'company_id')
    def _compute_from_product_id_company_id(self):
        price = 0
        for order in self.filtered('product_id'):
            order.product_uom_id = order.product_id.uom_id
            order.tax_ids = order.product_id.taxes_id.filtered(lambda tax: tax.company_id == order.company_id)  # taxes only from the same company
            if order.product_id:
                price = order.product_id.lst_price
                if order.pricelist_id:
                    price = self.pricelist_id.with_context(uom=order.product_uom_id.id).get_product_price(order.product_id, 1, False)
        self.unit_amount = price
    
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        order_lines = [(5, 0, 0)]
        data = {}
        price = discount = 0
        for order in self:
            if order.product_id:
                price = order.product_id.lst_price
                discount = 0
                
                if order.pricelist_id:
                    pricelist_price = self.pricelist_id.with_context(uom=order.product_uom_id.id).get_product_price(order.product_id, 1, False)

                    if self.pricelist_id.discount_policy == 'without_discount' and price:
                        discount = max(0, (price - pricelist_price) * 100 / price)
                    else:
                        price = pricelist_price

                data = {
                    'price_unit': price,
                    'discount': discount,
                    'product_uom_qty': 1,
                    'product_id': order.product_id.id,
                    'product_uom': order.product_uom_id.id,
                }

            order_lines.append((0, 0, data))
        self.order_line = order_lines
        self.order_line._compute_tax_id()
            
    # -----------------------------------------
    # Action Buttons
    # -----------------------------------------
    def action_property_reserve(self):
        for picking in self.picking_ids:
            picking.action_assign()                    
        self.write({
            'order_status':'reserved',
        })
    def action_booking_confirm(self):
        for picking in self.picking_ids:
            picking.action_assign()
            picking.action_confirm()
            for mv in picking.move_ids_without_package:
                mv.quantity_done = mv.product_uom_qty
            picking.button_validate()
        self.write({
            'order_status':'sale',
        })
    
    def _action_cancel(self):
        inv = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
        inv.button_cancel()
        return self.write({'state': 'cancel','order_status':'cencel'})
    
class SaleOrderPaymentLine(models.Model):
    _name = 'sale.order.payment.line'
    _description = 'Sales Order Payment Line'
    _order = 'order_id, sequence, id'
    _check_company_auto = True
    _rec_name = 'display_name'
    
    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    name = fields.Char(string='Description', )
    display_name = fields.Char(string='Display Name',store=True, compute='_compute_name')
    sequence = fields.Integer(string='Sequence', default=10)
    currency_id = fields.Many2one(related='order_id.currency_id', depends=['order_id.currency_id'], store=True, string='Currency')
    company_id = fields.Many2one(related='order_id.company_id', string='Company', store=True, index=True)
    order_partner_id = fields.Many2one(related='order_id.partner_id', store=True, string='Customer')
    payment_plan_id = fields.Many2one(related='order_id.payment_plan_id', store=True, string='Payment Plan')
    is_downpayment = fields.Boolean(string='Downpayment')
    amount_installment = fields.Monetary("Installment Amount", currency_field='currency_id', store=True)
    amount_residual = fields.Monetary("Residual Amount", currency_field='currency_id', store=True, compute='_compute_amount_all')
    payment_status = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('cancel', 'Cancel'),
    ], default="not_paid", compute="_compute_payment_status", store=True, )
    date_due = fields.Date('Due Date')
    move_id = fields.Many2one('account.move', string='Invoice', compute='_get_invoiced')
    
    @api.depends('order_id','display_name')
    def _compute_name(self):
        for payment in self:
            payment.display_name = payment.order_id.name + ' - ' + str(payment.name)
            
    @api.depends('order_id','order_id.invoice_ids','order_id.invoice_ids.state')
    def _compute_amount_all(self):
        for payment in self:
            payment.amount_residual = payment.amount_installment - sum(payment.order_id.invoice_ids.filtered(lambda x: x.state not in ('cancel') and x.payment_plan_line_id.id == payment.id).mapped('amount_residual'))
    
    def _get_invoiced(self):
        for payment in self:
            move_id = self.env['account.move'].search([('payment_plan_line_id','=',payment.id),('state','!=','cancel')],limit=1)
            payment.update({
                'move_id': move_id.id
            })
            
    @api.depends('order_id','order_id.invoice_ids','order_id.invoice_ids.payment_state')
    def _compute_payment_status(self):
        for payment in self:
            status_lst = payment.mapped('order_id.invoice_ids.payment_state')
            if status_lst:
                if status_lst.count('in_payment'):
                    status = 'paid'
                elif status_lst.count('paid'):
                    status = 'paid'
                elif status_lst.count('partial'):
                    status = 'partial'
                else:
                    status = 'not_paid'
            else:
                status = 'not_paid'
            payment.payment_status = status
            
    