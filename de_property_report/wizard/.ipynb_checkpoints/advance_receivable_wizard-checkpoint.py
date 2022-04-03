# # -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AdvanceReceivableWizard(models.Model):
    _name = 'advance.receivable.wizard'
    _description = 'Advance Receivable Wizard'
    
    
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    type = fields.Selection([
        ('date_wise', 'Date Wise'),
        ('month', 'Monthly'),
        ('year', 'Yearly'),
        ], string='Type', required=True, default='date_wise')
    
