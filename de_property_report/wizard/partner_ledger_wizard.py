# # -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PartnerLedgerWizard(models.Model):
    _name = 'partner.ledger.wizard'
    _description = 'Partner Ledger Wizard'
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
   
    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from','date_to'])[0]
        return self._print_report(data)

    
    def _print_report(self, data):
        data['form'].update(self.read(['date_from','date_to'])[0])
        return self.env.ref('de_property_report.open_partner_ledger_report').report_action(self, data=data, config=False)