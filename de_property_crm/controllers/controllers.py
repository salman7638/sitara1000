# -*- coding: utf-8 -*-
# from odoo import http


# class DePropertyCrm(http.Controller):
#     @http.route('/de_property_crm/de_property_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_property_crm/de_property_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_property_crm.listing', {
#             'root': '/de_property_crm/de_property_crm',
#             'objects': http.request.env['de_property_crm.de_property_crm'].search([]),
#         })

#     @http.route('/de_property_crm/de_property_crm/objects/<model("de_property_crm.de_property_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_property_crm.object', {
#             'object': obj
#         })
