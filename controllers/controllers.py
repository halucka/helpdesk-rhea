# -*- coding: utf-8 -*-
from odoo import http

# class HelpdeskRhea(http.Controller):
#     @http.route('/helpdesk_rhea/helpdesk_rhea/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_rhea/helpdesk_rhea/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_rhea.listing', {
#             'root': '/helpdesk_rhea/helpdesk_rhea',
#             'objects': http.request.env['helpdesk_rhea.helpdesk_rhea'].search([]),
#         })

#     @http.route('/helpdesk_rhea/helpdesk_rhea/objects/<model("helpdesk_rhea.helpdesk_rhea"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_rhea.object', {
#             'object': obj
#         })