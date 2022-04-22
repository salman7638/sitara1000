from odoo import models, fields, api, _
from  odoo import models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class PlotDetailXlS(models.AbstractModel):
    _name = 'report.de_commission_report.commission_report_xlx'
    _description = 'Commission report'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        docs = self.env['commission.wizard'].browse(self.env.context.get('active_id'))
        sheet = workbook.add_worksheet('Commission report')
        bold = workbook. add_format({'bold': True, 'align': 'center','bg_color': '#FFFF99','border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 15, 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border':True})
        format2 = workbook.add_format({'align': 'center'})
        format3 = workbook.add_format({'align': 'center','bold': True,'border': True,})

        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 25)
        sheet.set_column(3, 3, 25)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 25)

        sheet.write(2, 0, 'SR NO', header_row_style)
        sheet.write(2, 1, 'Plot No', header_row_style)
        sheet.write(2, 2, 'Customer Name', header_row_style)
        sheet.write(2, 3, "Commission", header_row_style)
        sheet.write(2, 4, "Commission Date", header_row_style)
        row = 3

            
                
                
            