# -*- coding: utf-8 -*-

""" Class BudgetDebit stores the Budget Debits made by using Helpdesk """

from odoo import fields, models, api, _

class BudgetDebit(models.Model):
    _name = "budget.debit"
    budget_id = fields.Many2one('helpdesk.budget', string='Budget')
    project_id = fields.Many2one('project.project', string='Project')

    timesheet_ids = fields.Many2many('account.analytic.line') #string='Timesheet Line'
    amount = fields.Float('Amount')

