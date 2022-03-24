# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    payment_plan_line_id = fields.Many2one('sale.order.payment.line', string='Payment Plan Line', ondelete='cascade', copy=False)
