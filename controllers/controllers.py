# -*- coding: utf-8 -*-
from odoo import http


class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('openacademy.index', {'helloworld': 'Hello World'})

    @http.route('/openacademy/openacademy/courses/', auth='public', website=True)
    def course(self, **kw):
        courses = http.request.env['openacademy.course']
        return http.request.render('openacademy.course', {
            'course': courses.search([])
        })

    @http.route('/openacademy/openacademy/<model("openacademy.course"):course>/', auth='public', website=True)
    def info(self, course):
        return http.request.render('openacademy.info', {
            'course': course
        })

# class Restrict(Openacademy):
#     @http.route('/openacademy/openacademy/courses/', auth='user')
#     def course(self):
#         return super(Restrict, self).list()
