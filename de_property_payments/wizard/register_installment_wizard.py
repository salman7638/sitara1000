
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class RegisterInstallmentWizard(models.TransientModel):
    _name = "register.installment.wizard"
    _description = "Register Installment wizard"
    

    number_of_installment = fields.Integer(string='Number Of Installment', required=True)
    sale_id = fields.Many2many('sale.order', string='Order')
    
    def action_confirm(self):
        installment_days =(921/self.number_of_installment)
        installment_date = fields.date.today()
        for sale in self.sale_id:            
            installment_date = self.sale_id.date_order
        installment_count = 0
        for installment in range(self.number_of_installment):            
            installment_count += 1
            installment_date = installment_date + timedelta(installment_days)
            vals = {
                'name':  'Installment Number '+str(installment_count),
                'date':  installment_date,
                'amount_paid':   0,
                'order_id': self.sale_id.id,
                'total_amount':  (self.sale_id.amount_residual/self.number_of_installment),
                'amount_residual':  (self.sale_id.amount_residual/self.number_of_installment) ,
                'remarks': 'Pending',
            }
            installment_vals = self.env['order.installment.line'].create(vals)
            
        for sale in self.sale_id:
            sale.update({
                'installment_created': True,
            })    
        
        