# -*- coding: utf-8 -*-

import time
from odoo import api, models, _ , fields 
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class OvertimeReport(models.AbstractModel):
    _name = 'report.de_property_report.plot_pdf_report'
    _description = 'Plot Status Report'

    
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env['plot.status.wizard'].browse(self.env.context.get('active_id'))
        
        plots = self.env['product.product'].search([])
        plot_location_list = []
        plot_location = self.env['op.property.location'].search([])
        plot_categories = []
        uniq_location_list = []        
        plot_category = self.env['product.category'].search([('can_be_property','=',True)])
        for plt_categ in plot_category:
            plot_categories.append(plt_categ.id)
        for plt_loc in plot_location:
            if plt_loc.location_id:
                plot_location_list.append(plt_loc.location_id.id)
        uniq_location_list = set(plot_location_list)  
        uniq_category_list = set(plot_categories)
#         uniq_category_list=[]
        for phase in uniq_location_list:
            phase_count=0
            grand_total_number_of_plots = 0
            grand_total_number_of_marlas = 0
            grand_available_total_number_of_plots = 0
            grand_available_total_number_of_marlas = 0
            grand_unconfirm_total_number_of_plots = 0
            grand_unconfirm_total_number_of_marlas = 0
            grand_reserve_total_number_of_plots = 0
            grand_reserve_total_number_of_marlas = 0
            grand_booked_total_number_of_plots = 0
            grand_booked_total_number_of_marlas = 0
            grand_sold_total_number_of_plots = 0
            grand_sold_total_number_of_marlas = 0 
            plot_phase = self.env['op.property.location'].search([('id','=', phase)], limit=1)
            
            for categ in uniq_category_list:
                uniq_category_list=[]
                total_number_of_plots = 0
                total_number_of_marlas = 0
                available_total_number_of_plots = 0
                available_total_number_of_marlas = 0
                unconfirm_total_number_of_plots = 0
                unconfirm_total_number_of_marlas = 0
                reserve_total_number_of_plots = 0
                reserve_total_number_of_marlas = 0
                booked_total_number_of_plots = 0
                booked_total_number_of_marlas = 0
                sold_total_number_of_plots = 0
                sold_total_number_of_marlas = 0 
                plot_category = self.env['product.category'].search([('id','=', categ)], limit=1)
                phase_plots = self.env['product.product'].search([('categ_id','=', plot_category.id),('property_location_id.location_id','=',plot_phase.id)] )
                
                
                mydict = {'plot_category': '','plot_phase':''}
               
                for pl in phase_plots:
                    
                    total_number_of_plots += 1
                    total_number_of_marlas += pl.plot_area_marla
                    if pl.state=='available':
                        available_total_number_of_plots += 1
                        available_total_number_of_marlas += pl.plot_area_marla
                    if pl.state=='unconfirm':
                        unconfirm_total_number_of_plots += 1
                        unconfirm_total_number_of_marlas += pl.plot_area_marla
                    if pl.state=='reserved':
                        reserve_total_number_of_plots += 1
                        reserve_total_number_of_marlas += pl.plot_area_marla 
                    if pl.state=='booked':
                        booked_total_number_of_plots += 1
                        booked_total_number_of_marlas += pl.plot_area_marla
                    if pl.state in ('un_posted_sold','posted_sold'):
                        sold_total_number_of_plots += 1
                        sold_total_number_of_marlas += pl.plot_area_marla 
                        
                        mydict['plot_phase'] = plot_phase.name
                        mydict['plot_category'] = plot_category.name

                        uniq_category_list.append(mydict)

#                 uniq_category_list.append({
#                     'plot_category': plot_category.name
            
#                 })
        
        return {
            'uniq_category_list': uniq_category_list,
            'docs': docs,
        }