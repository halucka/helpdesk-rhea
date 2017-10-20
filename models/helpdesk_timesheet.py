# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class HelpdeskTimesheet(models.Model):
    _inherit = 'account.analytic.line'
    amount_due = fields.Float('Amount Due')
    budget_debit_id = fields.Many2one('budget.debit', string='Budget Debit')

    # TODO set up amount and amount_due on creation
    # based on project_id => tickettime, ticketprice, is_servicedesk

    # def create(self):
    #     current_project = self.env["project.project"].search([('id', '=', self.project_id)])
    #     if current_project.is_servicedesk:
    #         amount = self.unit_amount/current_project.tickettime)*current_project.ticketprice
    #         self.amount_due = amount
    #         self.amount = amount
    #     return super(HelpdeskTimesheet, self).create(self)
