from odoo import models, fields, api, _
from  odoo import models
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class PlotDetailXlS(models.AbstractModel):
    _name = 'report.de_property_report.detail_report_xlx'
    _description = 'Plot Detail report'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        docs = self.env['plot.detail.wizard'].browse(self.env.context.get('active_id'))
        sheet = workbook.add_worksheet('Plot Detail Report')
        bold = workbook. add_format({'bold': True, 'align': 'center','bg_color': '#FFFF99','border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#FFFF99', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border':True})
        format2 = workbook.add_format({'align': 'center'})
        format3 = workbook.add_format({'align': 'center','bold': True,'border': True,})        
        
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)   
        sheet.set_column(7, 7, 20)   
        sheet.set_column(8, 8, 20)   
        sheet.set_column(9, 9, 20)   
        sheet.set_column(10, 10, 20)   
        sheet.set_column(11, 11, 20)   
        sheet.set_column(12, 12, 20)   
        sheet.set_column(13, 13, 20)   
        plots_detail = self.env['product.product'].search([]) 
        if docs.type=='available': 
            plots_detail = self.env['product.product'].search([('state','=','available')])
        if docs.type=='unconfirm': 
            plots_detail = self.env['product.product'].search([('state','=','unconfirm')])    
        if docs.type=='reserved': 
            plots_detail = self.env['product.product'].search([('state','=','reserved')]) 
        if docs.type=='booked': 
            plots_detail = self.env['product.product'].search([('state','=','booked')])
        if docs.type=='un_posted_sold': 
            plots_detail = self.env['product.product'].search([('state','in', ('un_posted_sold', 'posted_sold'))])
        if docs.type=='posted_sold': 
            plots_detail = self.env['product.product'].search([('state','in', ('reserved','booked','un_posted_sold','posted_sold'))])    
        col_no = 0    
        sheet.write(2, col_no, 'SR.NO', header_row_style)
        col_no += 1  
        sheet.write(2, col_no, 'PLOT STATUS', header_row_style)
        col_no += 1  
        if docs.type!='available': 
            sheet.write(2, col_no, 'NAME OF BUYER',header_row_style)
            col_no += 1  
        sheet.write(2, col_no, 'PLOT NO.',header_row_style)
        col_no += 1  
        sheet.write(2, col_no, "CATEGORY",header_row_style)
        col_no += 1  
        sheet.write(2, col_no, 'SIZE',header_row_style) 
        col_no += 1 
        if docs.type in ('reserved', 'booked', 'un_posted_sold'):
            sheet.write(2, col_no, "ADVANCE AMOUNT RECEIVED",header_row_style)
            col_no += 1  
            sheet.write(2, col_no, "% OF AMOUNT RECEIVED",header_row_style)
            col_no += 1  
        if docs.type in ('unconfirm', 'reserved'): 
            sheet.write(2, col_no, 'DATE OF RESERVATION',header_row_style)
            col_no += 1 
            sheet.write(2, col_no, "VALIDITY",header_row_style)
            col_no += 1  
        sheet.write(2, col_no, "PHASE",header_row_style)
        if docs.type =='posted_sold':
            sheet.write(2, col_no, 'TOTAL AMOUNT',header_row_style)
            col_no += 1 
            sheet.write(2, col_no, "AMOUNT RECEIVED TO-DATE",header_row_style)
            col_no += 1
            sheet.write(2, col_no, "BALANCE DUE AMOUNT",header_row_style)
            col_no += 1
            sheet.write(2, col_no, "OVERDUE AMOUNT",header_row_style)
            col_no += 1
            sheet.write(2, col_no, "OVERDUE DAYS",header_row_style)
            col_no += 1
            
        col_no = 0  
        
        row = 3
        sr_no = 1
        for plt in plots_detail:
            col_no=0
            adv_amount_received=0
            amt_percent_received=0
            for amt_receive in plt.payment_ids:
                adv_amount_received += amt_receive.amount
            amt_percent_received =  (adv_amount_received/plt.list_price) * 100 
            sheet.write(row, col_no, str(sr_no), format2)
            col_no += 1 
            sheet.write(row, col_no, str(plt.state), format2)
            col_no += 1
            if docs.type!='available': 
                sheet.write(row, col_no, str(plt.partner_id.name if plt.partner_id else ' '), format2)
                col_no += 1
            sheet.write(row, col_no, str(plt.name), format2)
            col_no += 1
            sheet.write(row, col_no, str(plt.categ_id.name), format2)
            col_no += 1
            sheet.write(row, col_no, str(plt.plot_area_marla), format2) 
            col_no += 1
            if docs.type in ('reserved', 'booked', 'un_posted_sold'): 
                sheet.write(row, col_no, '{0:,}'.format(int(round(adv_amount_received))), format2)
                col_no += 1
                sheet.write(row, col_no, '{0:,}'.format(int(round(amt_percent_received))), format2)
                col_no += 1
            if docs.type in ('unconfirm', 'reserved'): 
                sheet.write(row, col_no, str(plt.date_reservation), format2)
                col_no += 1
                sheet.write(row, col_no, str(plt.date_validity), format2)
                col_no += 1
            sheet.write(row, 10, str(plt.property_location_id.location_id.name), format2)
            if docs.type =='posted_sold':
                sheet.write(row, col_no, '{0:,}'.format(int(round(plt.list_price))), format2)
                col_no += 1
                sheet.write(row, col_no, '{0:,}'.format(int(round(plt.amount_paid))), format2)
                col_no += 1
                sheet.write(row, col_no, '{0:,}'.format(int(round(plt.amount_residual))), format2)
                col_no += 1
                sheet.write(row, col_no, '{0:,}'.format(int(round(0))), format2)
                col_no += 1
                sheet.write(row, col_no, str(), format2)
                col_no += 1
                
            col_no =0 
            sr_no += 1
            row += 1    
                
                
            