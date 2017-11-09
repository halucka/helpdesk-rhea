# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class HelpdeskTimesheet(models.Model):
    _inherit = 'account.analytic.line'
    budget_debit_ids = fields.Many2many('budget.debit',relation='timesheet_debit_rel')
    is_paid = fields.Boolean('Is paid', default=False)

