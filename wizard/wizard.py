# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2one('openacademy.session',
                                  string=_("Sessions"), required=True,
                                  default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string=_("Attendees"))
    seats = fields.Integer(string=_("Add or delete seats"))

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
            session.seats += self.seats
            if (100.0 * len(session.attendee_ids)/session.seats) >= 50:
                session.state = 'confirmed'
        return {}
