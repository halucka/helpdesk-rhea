# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class HelpdeskTimesheet(models.Model):
    _inherit = 'account.analytic.line'
    amount_due = fields.Float('Amount Due')
    budget_debit_id = fields.Many2one('budget.debit', string='Budget Debit')