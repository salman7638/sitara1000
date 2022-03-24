# -*- coding: utf-8 -*-
{
    'name': "Property Sale",

    'summary': """
        Property Sale
        """,

    'description': """
        Property Sales
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    'category': 'Sale',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['de_property', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_book_invoice_advance_views.xml',
        'views/sale_payment_plan_views.xml',
        'views/sale_order_views.xml',
        'report/sale_property_schedule.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
