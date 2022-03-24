# -*- coding: utf-8 -*-
# from odoo import http


# class DePropertySales(http.Controller):
#     @http.route('/de_property_sales/de_property_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_property_sales/de_property_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_property_sales.listing', {
#             'root': '/de_property_sales/de_property_sales',
#             'objects': http.request.env['de_property_sales.de_property_sales'].search([]),
#         })

#     @http.route('/de_property_sales/de_property_sales/objects/<model("de_property_sales.de_property_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_property_sales.object', {
#             'object': obj
#         })
