# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date

class PickBudgetWizard(models.TransientModel):
    _name = 'pick.budget.wizard'
    _description = "Please select the dates:"

    date_from = fields.Datetime('Date From')
    date_until = fields.Datetime('Date Until')

    # action for a button
    def lookup_budgets(self):
        current_project = self.env["project.project"].search([('id', '=', self._context['project_id'])])

        print "looking up helpdesk budgets..."
        lst = []
        number = 1
        date_from_as_datetime = datetime.strptime(self.date_from, '%Y-%m-%d %H:%M:%S')
        midnight_date_until = datetime.strptime(self.date_until, '%Y-%m-%d %H:%M:%S') +timedelta(days=1,microseconds=-1)
        for record in self.env['helpdesk.budget'].search([]):
            so_date_as_datetime = datetime.strptime(record.sale_order_date, '%Y-%m-%d %H:%M:%S')
            date_correct = (so_date_as_datetime > date_from_as_datetime) and (so_date_as_datetime < midnight_date_until)
            if date_correct and (record.project_id == current_project):
                lst.append((record.id,record.sale_order_date))
                number = number + 1
        print "Helpdesk Budgets within those dates are:"
        print lst

        print "looking up helpdesk timesheets..."
        ts_lst = []

        for record in self.env['account.analytic.line'].search([]):
           if record.account_id.name == current_project.name:   #not sure if project.name is correct
                ts_lst.append((record.id, record.name))
        print "Helpdesk Timesheets for this project are:"
        print ts_lst

        # TODO could probably return a new wizard and show these for reconciliation
        #return {'budgets': lst,'timesheets': ts_lst,}