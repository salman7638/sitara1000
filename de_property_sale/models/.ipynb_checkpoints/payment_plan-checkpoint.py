# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class SalePaymentPlan(models.Model):
    _name = "sale.payment.plan"
    _description = "Sales Payment Plan"
    _order = 'id desc'
    
    name = fields.Char(string='Payment Plan', translate=True, required=True)
    active = fields.Boolean(default=True, help="If the active field is set to False, it will allow you to hide the payment terms without removing it.")
    type = fields.Selection([
            ('percent', 'Percent'),
            ('fixed', 'Fixed Amount')
        ], string='Type', required=True, default='percent',
        help="Select here the kind of valuation related to this payment terms line.")
    line_ids = fields.One2many('sale.payment.plan.line', 'payment_plan_id', string='Terms', copy=True, )
    note = fields.Html(string='Description on the Invoice', translate=True)
    amount_percent = fields.Float(string='Total Percentage', compute='_compute_all_amount',store=True)
    
    @api.constrains('type', 'line_ids','line_ids.amount')
    def _check_percent(self):
        percent = sum(self.line_ids.mapped('amount'))
        if self.type == 'percent' and (percent != 100.0):
                raise ValidationError(_('The total Installment Percentage must be 100.'))
    
    @api.depends('line_ids','line_ids.amount')
    def _compute_all_amount(self):
        percent = total = 0
        for plan in self:
            if plan.type == 'percent':
                percent = sum(plan.line_ids.mapped('amount'))
            plan.amount_percent = percent

class SalePaymnetPlanLine(models.Model):
    _name = "sale.payment.plan.line"
    _description = "Payment Plan Line"
    _order = "sequence, id"
    
    name = fields.Char(string='Payment Terms', translate=True, required=True)
    days = fields.Integer(string='Days', required=True, default=0)
    amount = fields.Float(string='Value', digits='Payment Terms', help="For percent enter a ratio between 0-100.")
    payment_plan_id = fields.Many2one('sale.payment.plan', string='Payment Plan', required=True, index=True, ondelete='cascade')
    sequence = fields.Integer(default=10, help="Gives the sequence order when displaying a list of payment terms lines.")
    is_downpayment = fields.Boolean(string='Downpayment')
    
    @api.constrains('payment_plan_id', 'amount')
    def _check_percent(self):
        for plan in self:
            if plan.payment_plan_id.type == 'percent' and (plan.amount < 0.0 or plan.amount > 100.0):
                raise ValidationError(_('Percentages on the Payment Installment lines must be between 0 and 100.'))