# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, date

class PickBudgetWizard(models.TransientModel):
    _name = 'pick.budget.wizard'
    _description = "Please select the dates for Budgets:"

    date_from = fields.Datetime('Date From')
    date_until = fields.Datetime('Date Until')


    # action for a button
    @api.multi
    def reconciliate_budgets_and_timesheets(self):

        current_project = self.env["project.project"].search([('id', '=', self._context['project_id'])])

        date_from_as_datetime = datetime.strptime(self.date_from, '%Y-%m-%d %H:%M:%S')
        midnight_date_until = datetime.strptime(self.date_until, '%Y-%m-%d %H:%M:%S') + timedelta(days=1, microseconds=-1)

        consolidated_timesheets = self.consolidate_timesheets(current_project)
        self.book_timesheets_on_budget(date_from_as_datetime, midnight_date_until,current_project,consolidated_timesheets)

    @api.multi
    def consolidate_timesheets(self,current_project):
        # TODO
        # step 1: order open timesheets according to date
        # step 2: sum the timesheets on the same day (i.e. make a copy of the timesheet list where each day would be unique)
        # step 3: round the time *up* to the multiple of project.project tickettime
        # step 4: calculate the price for each ticket and the total price
        # return total price

        ts_lst = []

        for record in self.env['account.analytic.line'].search([]):
            if record.account_id.name == current_project.name:
                ts_lst.append(record.id) #(record.id, record.name)

        return ts_lst

    @api.multi
    def pick_budget(self, date_from_as_datetime, midnight_date_until,current_project):

        budget_list = []

        for record in self.env['helpdesk.budget'].search([]):
            so_date_as_datetime = datetime.strptime(record.sale_order_date, '%Y-%m-%d %H:%M:%S')
            date_correct = (so_date_as_datetime > date_from_as_datetime) and (so_date_as_datetime < midnight_date_until)
            if date_correct and (record.project_id == current_project):
                budget_list.append(record.id) #(record.id,record.sale_order_date)

        # TODO
        # try to pick first budget with amount_remaining > 0 and amount not equal to amount_remaining -> i.e open budget
        # if None, then the budget with amount remaining > 0 and oldest by date
        # if still None make new budget (to be manually made into new Sales Order)

        return budget_list[0]

    @api.multi
    def book_timesheets_on_budget(self, date_from_as_datetime, midnight_date_until,current_project,
                                  consolidated_timesheets):
        open_budget_id = self.pick_budget(date_from_as_datetime, midnight_date_until,current_project)
        open_budget = self.env["helpdesk.budget"].search([('id', '=', open_budget_id)])

        for timesheet_id in consolidated_timesheets:
            timesheet = self.env["account.analytic.line"].search([('id', '=', timesheet_id)])

            # check if the timesheet still fits in the budget
            amount_to_transfer = None
            new_amount_remaining = open_budget.amount_remaining + timesheet.amount
            if new_amount_remaining < 0.0:
                amount_to_transfer = -new_amount_remaining
                new_amount_remaining = 0

            # make a new budget_debit object
            bd = self.env["budget.debit"]
            bd_to_write = {"budget_id" : open_budget_id,
                           "project_id": timesheet.project_id.id,
                           "timesheet_id": timesheet.id,
                           "amount": -timesheet.amount, # timesheet amount typically negative!!!
                           }

            new_bd = bd.create(bd_to_write)
            timesheet.amount_due = 0
            open_budget.write({"amount_remaining" : new_amount_remaining})

            if amount_to_transfer is not None:
                # TODO fix - goes to infinite cycle, but probably only because pick_budget not yet implemented
                new_name = "Back-order of " + timesheet.name
                new_timesheet = timesheet.copy(default={
                                    'name': new_name,
                                    'amount': -amount_to_transfer,
                                    'amount_due': amount_to_transfer,})

                consolidated_timesheets = self.consolidate_timesheets(current_project)
                self.book_timesheets_on_budget(date_from_as_datetime, midnight_date_until, current_project,
                                          consolidated_timesheets)
        # book the timesheets on the open budget
        # keep track of bookings on budget_debit objects
        # if the open_budget is spent request new one via pick_budget(budget_list)


