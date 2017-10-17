# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date

class PickBudgetWizard(models.TransientModel):
    _name = 'pick.budget.wizard'
    _description = "Please select the dates:"

    date_from = fields.Datetime('Date From')
    date_until = fields.Datetime('Date Until')


    # action for a button
    def reconciliate_budgets_and_timesheets(self):

        current_project = self.env["project.project"].search([('id', '=', self._context['project_id'])])

        date_from_as_datetime = datetime.strptime(self.date_from, '%Y-%m-%d %H:%M:%S')
        midnight_date_until = datetime.strptime(self.date_until, '%Y-%m-%d %H:%M:%S') + timedelta(days=1, microseconds=-1)

        consolidated_timesheets = self.consolidate_timesheets(current_project)
        self.book_timesheets_on_budget(date_from_as_datetime, midnight_date_until,current_project,consolidated_timesheets)


    def consolidate_timesheets(self,current_project):
        # step 1: order open timesheets according to date
        # step 2: sum the timesheets on the same day (i.e. make a copy of the timesheet list where each day would be unique)
        # step 3: round the time *up* to the multiple of project.project tickettime
        # step 4: calculate the price for each ticket and the total price
        # return total price

        print "Looking up helpdesk timesheets..."
        ts_lst = []

        for record in self.env['account.analytic.line'].search([]):
            if record.account_id.name == current_project.name:
                ts_lst.append((record.id, record.name))
        print "Helpdesk Timesheets for this Project are:"
        print ts_lst
        print
        return ts_lst


    def pick_budget(self, date_from_as_datetime, midnight_date_until,current_project):

        print "Looking up helpdesk budgets..."
        budget_list = []

        for record in self.env['helpdesk.budget'].search([]):
            so_date_as_datetime = datetime.strptime(record.sale_order_date, '%Y-%m-%d %H:%M:%S')
            date_correct = (so_date_as_datetime > date_from_as_datetime) and (so_date_as_datetime < midnight_date_until)
            if date_correct and (record.project_id == current_project):
                budget_list.append((record.id,record.sale_order_date))

        print "Helpdesk Budgets within those dates for this Project are:"
        print budget_list
        print


        # try to pick first budget with amount_remaining > 0 and amount not equal to amount_remaining -> i.e open budget
        # if None, then the budget with amount remaining > 0 and oldest by date
        # if still None make new budget (to be manually made into new Sales Order)

        # # make a new helpdesk_budget object
        # so = self.env["sale.order"].search([('id', '=', self._context['sale_order_id'])])
        # hbo = self.env["helpdesk.budget"]
        # hbo_to_write = {
        #     "sale_order_id": self._context['sale_order_id'],
        #     "project_id": self.project_selection,
        #     "amount_remaining": so.amount_untaxed,
        # }
        #
        # chbo = hbo.create(hbo_to_write)

        return budget_list[0][0]


    def book_timesheets_on_budget(self, date_from_as_datetime, midnight_date_until,current_project,
                                  consolidated_timesheets):
        print "Trying to book timesheets on budget(s)..."
        open_budget = self.pick_budget(date_from_as_datetime, midnight_date_until,current_project)
        print open_budget

        print consolidated_timesheets
        for timesheet in consolidated_timesheets:

            # make a new budget_debit object
            #so = self.env["sale.order"].search([('id', '=', self._context['sale_order_id'])])
            bd = self.env["budget.debit"]
            bd_to_write = {
                                "budget_id" : open_budget,
                                "project_id" : timesheet.project_id,
                                "timesheet_ids" : timesheet.id,
                                "amount" : -timesheet.amount,
                }

            new_bd = bd.create(bd_to_write)


        # book the timesheets on the open budget
        # keep track of bookings on budget_debit objects
        # if the open_budget is spent request new one via pick_budget(budget_list)


