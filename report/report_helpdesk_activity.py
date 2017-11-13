from odoo import fields, models, api, _

class report_helpdesk_activity(models.AbstractModel):
    _name = 'report.helpdesk_rhea.report_helpdesk_activity'

    @api.model
    def render_html(self, docids, data=None):
        print "self"
        print self          # TODO
        print "docids"
        print docids  # [18]
        print "data"
        print data    # {u'project': 6, u'date_from': u'2017-11-01 00:00:00', u'date_until': u'2017-11-30 00:00:00'}
        data = data if data is not None else {}
        budgets = self.env['helpdesk.budget'].search([('project_id', '=', data['project'])])

        total_budget_purchased = 0
        total_budget_used = 0
        total_budget_remaining = 0

        for budget in budgets:
            total_budget_purchased += budget.amount
            total_budget_remaining += budget.amount_remaining

        total_budget_used = total_budget_purchased - total_budget_remaining

        timesheets = self.env['account.analytic.line'].search([('project_id', '=', data['project'])])
        budgetdebits = self.env['budget.debit'].search([('project_id', '=', data['project'])])

        docargs = {
            'docs': budgets,
            'data': {'budgets': budgets,
                    'timesheets': timesheets,
                     'budgetdebits': budgetdebits,
                     'total_budget_purchased': total_budget_purchased,
                     'total_budget_used': total_budget_used,
                     'total_budget_remaining': total_budget_remaining,
                     }
        }

        return self.env['report'].render('helpdesk_rhea.report_helpdesk_activity', docargs)



    def _get_budgets(self):
        pass

# https://www.odoo.com/forum/help-1/question/how-to-call-report-action-from-method-or-inside-method-17159

# # this should be action to get a report after clicking on Button
#     def generate_report(self):
#         context = {}
#
#         datas = {
#             'ids': context.get('active_ids', []),
#             'model': 'account.analytic.account',
#             'form': data
#         }
#
#         return {
#             'type': 'ir.actions.report.xml',
#             'report_name': 'account.analytic.account.balance',  # change this for my report name
#             'datas': {},  # dictionary
#         }