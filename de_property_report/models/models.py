# # -*- coding: utf-8 -*-
# from odoo import models, api
# from odoo.tools import amount_to_text_en



# class AccountPayment(models.Model):
#     _inherit = 'account.payment'
    
#     @api.depends('amount', 'currency_id')
#     def compute_text(self):
#         return amount_to_text_en(self.amount, self.currency_id.symbol)