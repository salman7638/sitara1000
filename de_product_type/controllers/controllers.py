# -*- coding: utf-8 -*-
# from odoo import http


# class DeProductType(http.Controller):
#     @http.route('/de_product_type/de_product_type', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_type/de_product_type/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_type.listing', {
#             'root': '/de_product_type/de_product_type',
#             'objects': http.request.env['de_product_type.de_product_type'].search([]),
#         })

#     @http.route('/de_product_type/de_product_type/objects/<model("de_product_type.de_product_type"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_type.object', {
#             'object': obj
#         })
