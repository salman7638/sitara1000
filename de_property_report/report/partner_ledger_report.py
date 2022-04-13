from odoo import models, fields, api, _
from  odoo import models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class PartnerLedgerXlS(models.AbstractModel):
    _name = 'report.de_property_report.ledger_report_xlx'
    _description = 'Partner Ledger report'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, lines):
        docs = self.env['partner.ledger.wizard'].browse(self.env.context.get('active_id'))
        sheet = workbook.add_worksheet('Partner Ledger Report')
        bold = workbook. add_format({'bold': True, 'align': 'center','bg_color': '#FFFF99','border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#FFFF99', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border':True})
        format2 = workbook.add_format({'align': 'center'})
        format3 = workbook.add_format({'align': 'center','bold': True,'border': True,})        
#         plot_categories = []
#         uniq_location_list = []        
        
        
        sheet.set_column(1, 1, 40)
        sheet.set_column(2, 2, 30)
        sheet.set_column(3, 3, 30)
        sheet.set_column(4, 4, 30)
        sheet.set_column(5, 5, 30)
        
            
        
        sheet.write(2,1, 'Partner', header_row_style)
        sheet.write(2,2 , 'Debit', header_row_style)
        sheet.write(2,3 , "Credit", header_row_style)
        sheet.write(2,4 , "Balance", header_row_style)
        row = 3
        
        
        all_partners = self.env['res.partner'].search([])
        for partner in all_partners:
            total_debit = total_credit = total_balnce = 0
            partner_ledger = self.env['account.move.line'].search([('partner_id','=',partner.id),('date','>=',docs.date_from),('date_maturity','<=',docs.date_to)])
            

            
            for linessssss in partner_ledger:
                total_debit += linessssss.debit
                total_credit += linessssss.credit
                total_balnce = total_debit - total_credit
                
                sheet.write(row, 1, linessssss.partner_id.name, format2)
                sheet.write(row, 2, total_debit, format2)
                sheet.write(row, 3, total_credit, format2)
                sheet.write(row, 4, total_balnce, format2)
            
            row += 1
                
    
            