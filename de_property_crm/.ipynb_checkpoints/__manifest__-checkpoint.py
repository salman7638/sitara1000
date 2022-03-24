# -*- coding: utf-8 -*-
{
    'name': "Property CRM",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','de_property'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
