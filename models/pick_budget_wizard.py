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
        print "lookup_budgets in progress..."
        lst = []
        number = 1
        date_from_as_datetime = datetime.strptime(self.date_from, '%Y-%m-%d %H:%M:%S')
        midnight_date_until = datetime.strptime(self.date_until, '%Y-%m-%d %H:%M:%S') +timedelta(days=1,microseconds=-1)
        for record in self.env['helpdesk.budget'].search([]):
            so_date_as_datetime = datetime.strptime(record.sale_order_date, '%Y-%m-%d %H:%M:%S')
            if ((so_date_as_datetime > date_from_as_datetime) and (so_date_as_datetime < midnight_date_until)):
                lst.append((record.id,record.sale_order_date))
            number = number + 1
        print lst
        #
        # print "looking up helpdesk timesheets..."
        # ts_lst = []
        # for record in self.env['project.analytic_account'].search([]):
        #     ts_lst.append(record.id)
        # print ts_lst