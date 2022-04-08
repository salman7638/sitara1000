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
        
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 10)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 35)   
        sheet.write(2,0,  'SR.NO', header_row_style)
        sheet.write(2,1 , 'DATE',  header_row_style)
        sheet.write(2,2 , 'PLOT NO.', header_row_style)
        sheet.write(2,3 , "AMOUNT",  header_row_style)
        sheet.write(2,4 , 'REMARKS', header_row_style) 
        row = 3
        date_wise_receivables = []
        unconfirm_plot_list = self.env['product.product'].search([('state','=','unconfirm'),('booking_validity', '>=' , docs.date_from),('booking_validity', '<=' , docs.date_to) ])
        for unconf_plot in unconfirm_plot_list:            
            line_vals = {
                'date':  unconf_plot.booking_validity,
                'plot_no':  unconf_plot.name , 
                'amount':   unconf_plot.booking_amount ,
                'remarks': '' ,
            }
            date_wise_receivables.append(line_vals)
            
        reserve_plot_list = self.env['product.product'].search([('state','=','reserved'),('booking_validity', '>=' , docs.date_from),('booking_validity', '<=' , docs.date_to) ])
        for reserve_plot in reserve_plot_list:  
            if not reserve_plot.booking_id:
                token_amt = reserve_plot.booking_amount - reserve_plot.amount_paid
                line_vals = {
                    'date':  reserve_plot.booking_validity,
                    'plot_no':  reserve_plot.name , 
                    'amount':  token_amt if token_amt > 0 else 0,
                    'remarks': '' ,
                }
                date_wise_receivables.append(line_vals)                
            elif reserve_plot.booking_id:
                line_vals = {
                    'date':  reserve_plot.booking_validity,
                    'plot_no':  reserve_plot.name , 
                    'amount':  reserve_plot.booking_id.booking_amount_residual,
                    'remarks': '' ,
                }
                date_wise_receivables.append(line_vals)
                
        booked_plot_list = self.env['product.product'].search([('state','=','booked'),('date_validity', '>=' , docs.date_from),('date_validity', '<=' , docs.date_to) ])
        for book_plot in booked_plot_list:  
            if book_plot.booking_id:
                line_vals = {
                    'date':  book_plot.date_validity ,
                    'plot_no': book_plot.name , 
                    'amount':  book_plot.booking_id.allotment_amount_residual ,
                    'remarks': '' ,
                }
                date_wise_receivables.append(line_vals)   
                
        sr_no = 1 
        total_amount = 0
        for receiv in date_wise_receivables:             
            sheet.write(row, 0, str(sr_no), format2)
            sheet.write(row, 1, str(receiv['date']), format2) 
            sheet.write(row, 2, str(receiv['plot_no']), format2)
            sheet.write(row, 3, '{0:,}'.format(int(round(receiv['amount']))), format2)
            total_amount += float(receiv['amount'])
            sheet.write(row, 4, str(receiv['remarks']), format2) 
            row += 1
            sr_no += 1
            
        sheet.write(row, 0, str(), header_row_style)
        sheet.write(row, 1, str(), header_row_style) 
        sheet.write(row, 2, str(), header_row_style)
        sheet.write(row, 3, str('{0:,}'.format(int(round(total_amount)))), header_row_style)
        sheet.write(row, 4, str(), header_row_style)       
        row += 1
            