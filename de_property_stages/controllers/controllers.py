# -*- coding: utf-8 -*-
# from odoo import http


# class DePropertyStages(http.Controller):
#     @http.route('/de_property_stages/de_property_stages', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_property_stages/de_property_stages/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_property_stages.listing', {
#             'root': '/de_property_stages/de_property_stages',
#             'objects': http.request.env['de_property_stages.de_property_stages'].search([]),
#         })

#     @http.route('/de_property_stages/de_property_stages/objects/<model("de_property_stages.de_property_stages"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_property_stages.object', {
#             'object': obj
#         })
