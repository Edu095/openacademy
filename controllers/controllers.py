# -*- coding: utf-8 -*-
from odoo import http


class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('openacademy.index', {'helloworld': 'Hello World'})

    @http.route('/openacademy/openacademy/users/', auth='public', website=True)
    def list(self, **kw):
        return http.request.render('openacademy.listing', {
            'root': 'users page'
        })


class Restrict(Openacademy):
    @http.route('/openacademy/openacademy/users/', auth='user')
    def list(self):
        return super(Restrict, self).list()

#     @http.route('/openacademy/openacademy/objects/<model("openacademy.openacademy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openacademy.object', {
#             'object': obj
#         })
