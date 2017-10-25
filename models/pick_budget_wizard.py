# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
from operator import itemgetter
from math import ceil


class PickBudgetWizard(models.TransientModel):
    _name = 'pick.budget.wizard'
    _description = "Please select the dates for Timesheets:"

    date_from = fields.Datetime('Date From')
    date_until = fields.Datetime('Date Until')


    # action for a button
    @api.multi
    def reconciliate_budgets_and_timesheets(self):

        current_project = self.env["project.project"].search([('id', '=', self._context['project_id'])])
        date_from_as_datetime = datetime.strptime(self.date_from, '%Y-%m-%d %H:%M:%S')
        midnight_date_until = datetime.strptime(self.date_until, '%Y-%m-%d %H:%M:%S') + timedelta(days=1, microseconds=-1)

        self.book_timesheets_on_budget(date_from_as_datetime, midnight_date_until,current_project)


    @api.multi
    def consolidate_timesheets(self, date_from_as_datetime, midnight_date_until, current_project):

        # step 1: find timesheets for the current project and order them according to date
        ts_lst = []

        for record in self.env['account.analytic.line'].search([]):
            date_as_datetime = datetime.strptime(record.date, '%Y-%m-%d')  # for Datetime '%Y-%m-%d %H:%M:%S'
            date_correct = (date_as_datetime > date_from_as_datetime) and (date_as_datetime < midnight_date_until)
            if date_correct and (record.account_id.name == current_project.name):
                ts_lst.append((record.id, record.date)) #(record.id, record.name)

        ts_lst.sort(key=itemgetter(1))  # sort by date

        # step 2: sum the timesheets on the same day (i.e. make a copy of the timesheet list where each day would be unique)

        def insertIntoDataStruct(id, date, aDict):
            if not date in aDict:
                aDict[date] = [id]
            else:
                aDict[date].append(id)

        timesheets_per_date = {}
        for x in ts_lst:
            insertIntoDataStruct(x[0], x[1], timesheets_per_date)

        # step 3: round the time *up* to the multiple of project.project tickettime
        # & calculate the price for each ticket and the total price
        consolidated_timesheets = []
        for date in timesheets_per_date.keys():
            orig_timesheets = timesheets_per_date[date]
            totaltime = 0
            for id in orig_timesheets:
                totaltime += self.env['account.analytic.line'].search([('id', '=', id)]).unit_amount

            cost = ceil(totaltime/current_project.tickettime)*current_project.ticketprice
            consolidated_timesheets.append((date, cost, orig_timesheets))

        return consolidated_timesheets


    @api.multi
    def pick_budget(self, current_project):

        budget_list_all = []

        for record in self.env['helpdesk.budget'].search([]):
            if record.project_id == current_project:
                budget_list_all.append((record.id, record.amount_remaining, record.sale_order_date))

        # remove budgets that are spent, but not those that
        # still have budget on them or are negative (to be made into Sale Order manually)
        budget_list = [item for item in budget_list_all if item[1] <> 0]

        budget_list.sort(key=itemgetter(1))  # sort by amount_remaining

        print "budget_list before"
        print budget_list

        any_budget = False
        any_positive = False
        any_negative = False
        total_remaining_budget = 0

        if len(budget_list) != 0:
            any_budget = True

        if not any_budget:
            print "There is no existing Budget within those dates. We need to make a new Budget from a Sales Order."
            return False

        if any_budget:
            for item in budget_list:
                total_remaining_budget += item[1]
                if item[1] > 0:
                    any_positive = True
                if item[1] < 0:
                    any_negative = True

        print "The total remaining amount on all budgets within those dates is: ", total_remaining_budget

        if any_positive and not any_negative: # This is the normal scenario
            budget_list.sort(key=itemgetter(2))  # sort by date, then return the oldest
            return budget_list[0][0]

        if any_positive and any_negative:
            print "There are both positive and negative Budgets..."
            return False

        if any_negative and not any_positive:
            raise UserError(_("We are already running credit (remaining Budget < 0)"))
            return False

        # TODO
        # try to pick first budget with amount_remaining > 0 and amount not equal to amount_remaining -> i.e open budget
        # if None, then the budget with amount remaining > 0 and oldest by date
        # check if there is already a Budget with amount remaining < 0
        # if still None make new budget (to be manually made into new Sales Order)


    @api.multi
    def book_timesheets_on_budget(self, date_from_as_datetime, midnight_date_until, current_project):
        """
        This function should:
        - book the timesheets on the open budget
        - keep track of bookings on budget_debit objects
        - if the open_budget is spent request new one via pick_budget(budget_list)
        """
        consolidated_timesheets = self.consolidate_timesheets(date_from_as_datetime, midnight_date_until, current_project)
        print "consolidated_timesheets"
        print consolidated_timesheets

        open_budget_id = self.pick_budget(current_project)
        open_budget = self.env["helpdesk.budget"].search([('id', '=', open_budget_id)])

        while len(consolidated_timesheets) > 0:

            timesheet_tup = consolidated_timesheets[0]
            # timesheet_tup is (date, cost, orig_timesheets)
            #  which looks like this ('2017-10-12', 1200.0, [9, 8, 7])

            timesheet_date = timesheet_tup[0]
            timesheet_cost = timesheet_tup[1]
            timesheet_ids = timesheet_tup[2]

            print "timesheet_cost"
            print timesheet_cost

            # check if the consolidated timesheet still fits in the budget
            amount_to_transfer = None
            new_amount_remaining = open_budget.amount_remaining - timesheet_cost
            if new_amount_remaining < 0.0:
                amount_to_transfer = -new_amount_remaining
                new_amount_remaining = 0

            print "Going to write to budget with id: ", open_budget_id
            # make a new budget_debit object
            bd = self.env["budget.debit"]
            bd_to_write = {"budget_id" : open_budget_id,
                           "project_id": current_project.id,
                           "amount": timesheet_cost,
                           }

            new_bd = bd.create(bd_to_write)

            for id in timesheet_ids:
                timesheet = self.env["account.analytic.line"].search([('id', '=', id)])
                timesheet.write({"budget_debit_ids": (4, new_bd.id)}) # TODO

            open_budget.write({"amount_remaining" : new_amount_remaining}) # This does not seem to work correctly

            if amount_to_transfer is not None:
                print "Warning: we need to tranfer to another Budget, this one is used up!"

                consolidated_timesheets[0] = (timesheet_date, amount_to_transfer, timesheet_ids) # make sure this actually modifies the cons timesheets
                open_budget_id = self.pick_budget(current_project)

                if open_budget_id is False:
                    # TODO remake to make a new negative Budget, not a Timesheet

                    new_name = "Payment for Extra Helpdesk Timesheet(s): " + str(timesheet_ids)

                    tasks_from_current_project = self.env['project.task'].search([('project_id', '=', current_project.id)])
                    if len(tasks_from_current_project)>0:
                        partner_id = tasks_from_current_project[0].partner_id

                    if not partner_id:
                        raise UserError("Please fill in Customer for the Project, then retry.")

                    # make a corresponding Sale Order
                    new_so = self.env["sale.order"]
                    so_to_write = {'name': new_name,
                                   'partner_id': partner_id,
                                   #'date_order': date.today(),
                                   }
                    new_sale_order = new_so.create(so_to_write)

                    # make a new NEGATIVE Budget
                    new_budget = self.env["helpdesk.budget"]

                    budget_to_write = {'sale_order_id':new_sale_order,
                                       'project_id': current_project,
                                       'amount': -amount_to_transfer,
                                       'amount_remaining': -amount_to_transfer,
                                        }

                    new_helpdesk_budget = new_budget.create(budget_to_write)

                else:
                    open_budget = self.env["helpdesk.budget"].search([('id', '=', open_budget_id)])

            else:
                del consolidated_timesheets[0]

