from odoo import models, fields, api, _
from  odoo import models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class AdvanceReceivableXlS(models.AbstractModel):
    _name = 'report.de_property_report.adv_receive_xlx'
    _description = 'Advance Receivable report'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        docs = self.env['advance.receivable.wizard'].browse(self.env.context.get('active_id'))
        sheet = workbook.add_worksheet('Forcast Receivables Report')
        bold = workbook. add_format({'bold': True, 'align': 'center','bg_color': '#FFFF99','border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#FFFF99', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border':True})
        format2 = workbook.add_format({'align': 'center'})
        format3 = workbook.add_format({'align': 'center','bold': True,'border': True,})        
        plots = self.env['product.product'].search([('state','in',('unconfirm','reserved','booked','un_posted_sold'))])
#         for plt in plots:
                      
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 10)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 35)   
        sheet.write(2,0,'SR.NO', header_row_style)
        sheet.write(2,1 , 'DATE',header_row_style)
        sheet.write(2,2 , 'PLOT NO.',header_row_style)
        sheet.write(2,3 , "AMOUNT",header_row_style)
        sheet.write(2,4 , 'REMARKS',header_row_style) 
        row = 3
#         for phase in uniq_location_list:    
#             sheet.write(row, 0, str(plot_phase.name), format2)
#             sheet.write(row, 1, str(plot_category.name), format2) 
#             sheet.write(row, 2, '{0:,}'.format(int(round(total_number_of_plots))), format2)
#             grand_total_number_of_plots += total_number_of_plots
#             sheet.write(row, 3, '{0:,}'.format(int(round(total_number_of_marlas))), format2)
#             grand_total_number_of_marlas += total_number_of_marlas
#             sheet.write(row, 4, '{0:,}'.format(int(round(available_total_number_of_plots))), format2)
#             grand_available_total_number_of_plots += available_total_number_of_plots
#             row += 1
            
#         sheet.write(row, 0, str(), header_row_style)
#         sheet.write(row, 1, str(), header_row_style) 
#         sheet.write(row, 2, '{0:,}'.format(int(round(grand_total_number_of_plots))), header_row_style)
#         sheet.write(row, 3, '{0:,}'.format(int(round(grand_total_number_of_marlas))), header_row_style)
#         sheet.write(row, 4, '{0:,}'.format(int(round(grand_available_total_number_of_plots))), header_row_style) 
            
#         row += 1
            