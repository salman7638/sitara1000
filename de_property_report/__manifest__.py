# -*- coding: utf-8 -*-
{
    'name': "Property Report",

    'summary': """
            Property Report
             1) booking_report
             2) allotment_report
       """,

    'description': """
            Property Report
             1) booking_report
             2) allotment_report
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','de_sale_booking','de_property_payments','de_property','report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
#         'wizard/advance_receivable_wizard.xml',
#         'wizard/plot_status_wizard.xml',
#         'report/plot_status_report.xml',
        'report/booking_report.xml',
        'report/booking_template.xml',
        'report/allotment_report.xml',
        'report/allotment_template.xml',
        'report/payment_schedule_report.xml',
        'report/payment_schedule_template.xml',
        'report/payment_report.xml',
        'report/payment_template.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
