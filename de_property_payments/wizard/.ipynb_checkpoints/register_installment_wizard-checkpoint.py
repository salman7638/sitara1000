
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class RegisterInstallmentWizard(models.TransientModel):
    _name = "register.installment.wizard"
    _description = "Register Installment wizard"
    

    number_of_installment = fields.Integer(string='Number Of Installment', required=True)
    installment_start_date = fields.Date(string='Installment Start Date', required=True, default=fields.date.today() )
    sale_id = fields.Many2many('sale.order', string='Order')
    
    def action_confirm(self):
        installment_days =(921/self.number_of_installment)
        installment_date = self.installment_start_date
        installment_count = 0
        for installment in range(self.number_of_installment):            
            installment_count += 1
            vals = {
                'name':  'Installment Number '+str(installment_count),
                'date':  installment_date,
                'amount_paid':   0,
                'order_id': self.sale_id.id,
                'amount_residual':  (self.sale_id.amount_residual/self.number_of_installment) ,
                'remarks': 'Pending',
            }
            installment_vals = self.env['order.installment.line'].create(vals)
            installment_date = installment_date + timedelta(installment_days)
        
            
        
        