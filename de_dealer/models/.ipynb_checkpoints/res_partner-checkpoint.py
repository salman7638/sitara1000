# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    active_dealer = fields.Boolean(string='Is Dealer')
    
    @api.model
    def create(self, vals):
        if 'vat' in vals:
            if vals['vat']:
                vat = vals['vat'].strip().lower()
                 
                sql = """ select lower(vat) from res_partner where lower(vat)='""" +str(vat)+"""' """
                self.env.cr.execute(sql)
                exists = self.env.cr.fetchone()
                
                if exists:
                    raise UserError(('Same CNIC number already exists with another contact!'))
                else:
                    pass

        rec = super(ResPartner, self).create(vals)
        return rec