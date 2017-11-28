from odoo import fields, models, api, _
from datetime import datetime, timedelta, date

class report_helpdesk_activity(models.AbstractModel):
    _name = 'report.helpdesk_rhea.report_helpdesk_activity'

    @api.model
    def render_html(self, docids, data=None):

        date_from_as_datetime = datetime.strptime(data['date_from'], '%Y-%m-%d %H:%M:%S')
        midnight_date_until = datetime.strptime(data['date_until'], '%Y-%m-%d %H:%M:%S') + timedelta(days=1,
                                                                                                  microseconds=-1)

        budgets = self.env['helpdesk.budget'].search([('project_id', '=', data['project'])]).sorted(key=lambda r: r.sale_order_date)

        total_budget_purchased = 0
        total_budget_used = 0
        total_budget_remaining = 0

        for budget in budgets:
            total_budget_purchased += budget.amount
            total_budget_remaining += budget.amount_remaining

        total_budget_used = total_budget_purchased - total_budget_remaining

        # find Timesheets for current Project within the dates selected on the wizard
        timesheets = []
        for record in self.env['account.analytic.line'].search([('project_id', '=', data['project'])]).sorted(key=lambda r: r.date):
            date_as_datetime = datetime.strptime(record.date, '%Y-%m-%d')  # for Datetime '%Y-%m-%d %H:%M:%S'
            date_correct = (date_as_datetime > date_from_as_datetime) and (date_as_datetime < midnight_date_until)
            if date_correct:
                timesheets.append(record)

        budgetdebits = self.env['budget.debit'].search([('project_id', '=', data['project'])])

        budgetdebit_dict = {}  # dict of lists like {'February 2017': [5, 225.0],}
        for bd in budgetdebits:
            bd_month_year = datetime.strptime(bd.create_date, '%Y-%m-%d %H:%M:%S').strftime("%m/%Y")
            if not bd_month_year in budgetdebit_dict:
                budgetdebit_dict[bd_month_year] = [1, bd.amount]
            else:
                budgetdebit_dict[bd_month_year][0] += 1
                budgetdebit_dict[bd_month_year][1] += bd.amount

        budgetdebit_stats = []
        for key in budgetdebit_dict:
           budgetdebit_stats.append((key, budgetdebit_dict[key][0], budgetdebit_dict[key][1]))
        budgetdebit_stats.sort()

        # TODO figure out a good way to determine the language of the report
        if len(budgets)>0:
            client = budgets[0].sale_order_id.partner_id
        elif len(timesheets)>0:
            client = timesheets[0].partner_id
        else:
            client = None

        language = client.lang
        print client
        print language
        print timesheets[0].partner_id.lang
        # if not language:
        #     language = user_id.lang
        if not language:
            language = 'en_US'

        docargs = {'docs': self.env['account.analytic.line'].search([('project_id', '=', data['project'])]),
            'data': {'client': client,
                     'lang': language,
                    'budgets': budgets,
                    'timesheets': timesheets,
                     'budgetdebit_stats': budgetdebit_stats,
                     'total_budget_purchased': total_budget_purchased,
                     'total_budget_used': total_budget_used,
                     'total_budget_remaining': total_budget_remaining,
                     'date_from': date_from_as_datetime.strftime("%d-%m-%Y"),
                     'date_until': midnight_date_until.strftime("%d-%m-%Y"),
                     }
        }

        return self.env['report'].render('helpdesk_rhea.report_helpdesk_activity', docargs)



