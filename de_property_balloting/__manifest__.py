# -*- coding: utf-8 -*-
{
    'name': "Property Balloting",
    'summary': """
        Property Balloting
        """,
    'description': """
        Property BAlloting
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'CRM/Sale',
    'version': '15.0.0.1',
    'sequence': 170,

    # any module necessary for this one to work correctly
    'depends': ['de_property_crm','de_property_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menuitem_views.xml',
        'views/balloting_config_views.xml',
        'views/balloting_order_views.xml',
        'views/allotment_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
