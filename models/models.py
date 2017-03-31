# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string=_("Title"), required=True)
    description = fields.Text()
    code = fields.Selection(string='Code', selection=[('a', 'A'), ('b', 'B')])

    responsible_id = fields.Many2one('res.users', ondelete='set null',
                                     string=_("Responsible"), index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id',
                                  string=_("Sessions"))

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         _("The title of the course should not be the description")),
        ('name_unique',
         'UNIQUE(name)',
         _("The course title must be unique")),
    ]


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help=_("Duration in days"))
    seats = fields.Integer(string=_("Number of seats"))
    active = fields.Boolean(default=True)
    color = fields.Integer()

    instructor_id = fields.Many2one('res.partner', string=_("Instructor"),
                                    domain=['|', ('instructor', '=', True),
                                            ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course', ondelete='cascade',
                                string=_("Course"), required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string=_("Taken seats"), compute='_taken_seats')

    end_date = fields.Date(string=_("End Date"), store=True,
                           compute='_get_end_date', inverse='_set_end_date')

    hours = fields.Float(string=_("Duration in hours"),
                         compute='_get_hours', inverse='_set_hours')

    attendees_count = fields.Integer(string=_("Attendees count"),
                                     compute='_get_attendees_count',
                                     store=True)

    state = fields.Selection([
        ('draft', _("Draft")),
        ('confirmed', _("Confirmed")),
        ('done', _("Done")),
    ], default='draft')

    @api.multi
    @api.onchange('taken_seats')
    def action_draft(self):
        if self.taken_seats < 50:
            self.state = 'draft'
        else:
            self.state = 'confirmed'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids)/r.seats

    @api.onchange('seats', 'attendee_ids')
    def _very_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of availabel seats may not be negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError(_("A session's intructor can't be an attendee"))
