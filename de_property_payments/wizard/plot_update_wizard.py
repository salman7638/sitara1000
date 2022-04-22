
# -*- coding: utf-8 -*-

# from odoo import api, fields, models, _
# from dateutil.relativedelta import relativedelta
# from datetime import datetime, timedelta


# class PlotUpdateWizard(models.TransientModel):
#     _name = "plot.update.wizard"
#     _description = "Plot Update wizard"
    

#     plot_update_id = fields.Many2one('product.product', string='Plot', required=True)
#     plot_id = fields.Many2one('product.product', string='Plot', required=True)
    
    
    
#     def action_confirm(self):
#         self.plot_update_id.update({
#             'booking_id': self.plot_id.booking_id.id,
#             'partner_id': self.plot_id.partner_id.id,
#             'booking_validity': self.plot_id.booking_validity,
#             'date_reservation': self.plot_id.date_reservation,
#             'date_validity': self.plot_id.date_validity,
#             'token_validity': self.plot_id.date_validity,
#             'cnic': self.plot_id.cnic,
#             'phone': self.plot_id.phone,
#                 })
        
#         self.plot_id.update({
#             'booking_id': False,
#             'partner_id': False,
#             'booking_validity': False,
#             'date_reservation': False,
#             'date_validity': False,
#             'token_validity': False,
#             'cnic': '',
#             'phone': '',
#         })

        
        