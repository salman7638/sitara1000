# -*- coding: utf-8 -*-
# from odoo import http


# class DePropertyBalloting(http.Controller):
#     @http.route('/de_property_balloting/de_property_balloting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_property_balloting/de_property_balloting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_property_balloting.listing', {
#             'root': '/de_property_balloting/de_property_balloting',
#             'objects': http.request.env['de_property_balloting.de_property_balloting'].search([]),
#         })

#     @http.route('/de_property_balloting/de_property_balloting/objects/<model("de_property_balloting.de_property_balloting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_property_balloting.object', {
#             'object': obj
#         })
