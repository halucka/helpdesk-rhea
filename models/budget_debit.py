# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

""" Class BudgetDebit stores the Budget Debits made by using Helpdesk"""

class BudgetDebit(models.Model):
    _name = "budget.debit"
    name = fields.Char("budget debit transaction")
    budget_id = fields.Many2one('helpdesk.budget', string='Budget')
    project_id = fields.Many2one('project.project', string='Project')

    timesheet_ids = fields.One2many('account.analytic.line', 'id',
                                    'Timesheet lines')
    amount = fields.Float('Amount')

