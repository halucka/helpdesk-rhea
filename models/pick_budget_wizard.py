# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date

class PickBudgetWizard(models.TransientModel):
    _name = 'pick.budget.wizard'
    _description = "Please select the dates:"

    date_from = fields.Datetime('Date From')
    date_until = fields.Datetime('Date Until (excl.)')

    # action for a button
    def lookup_budgets(self):
        print "lookup_budgets in progress..."
        lst = []
        number = 1
        for record in self.env['helpdesk.budget'].search([]):
            if ((record.sale_order_date > self.date_from) and (record.sale_order_date <= self.date_until)):
                lst.append((record.id))
            number = number + 1
        print lst