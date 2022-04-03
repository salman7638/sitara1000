# # -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PlotStatusWizard(models.Model):
    _name = 'plot.status.wizard'
    _description = 'Plot Status Wizard'
    
    
    date = fields.Date(string='Date', required=True, default=fields.date.today() )
    
    def check_report(self):
        data = {}
        data['form'] = self.read(['date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date'])[0])
        return self.env.ref('de_hr_attendance_report.open_hr_report_wizard_action').report_action(self, data=data, config=False)
    
    
