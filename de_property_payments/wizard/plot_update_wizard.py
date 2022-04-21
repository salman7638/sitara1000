
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class PlotUpdateWizard(models.TransientModel):
    _name = "plot.update.wizard"
    _description = "Plot Update wizard"
    

    plot_update_id = fields.Many2one('product.product', string='Plot', required=True)
    plot_id = fields.Many2one('product.product', string='Plot', required=True)
    
    
    
    def action_confirm(self):
        self.plot_update_id.update({
            'cnic': self.plot_id.cnic,
            'phone': self.plot_id.phone,
            
                })
#         reseller = self.env['plot.reseller.line'].create(resell_vals)
#         self.sale_id.update({
#             'partner_id': self.partner_id.id,
#             'membership_fee_submit':  False,
#         })
#         payments=self.env['account.payment'].search([('order_id','=',self.sale_id.id)])        
#         for prd_line in self.sale_id.order_line:
#             if prd_line.product_id:
#                 prd_line.product_id.update({
#                      'partner_id':  self.partner_id.id,
#                      'cnic':  self.partner_id.nic,
#                 })             
#         for pay in payments:
#             pay.action_draft()
#             pay.update({
#                 'partner_id': self.partner_id.id,
#             })
#             pay.action_post()
        
        