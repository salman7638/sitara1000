
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AssignDealerWizard(models.TransientModel):
    _name = "assign.dealer.wizard"
    _description = "Assign Dealer wizard"
    

    partner_id = fields.Many2one('res.partner', string='Dealer/Customer')
    product_ids = fields.Many2many('product.product', string='Plot')
    date_reservation = fields.Date(string='Date of Reservation')
    date_validity = fields.Date(string='Date Validity')
    
    def action_assign_partner(self):
        for line in self.product_ids:
            line.update({
                'partner_id': self.partner_id.id,
                'state': 'unconfirm',
            })
        
        