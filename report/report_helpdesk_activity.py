from odoo import fields, models, api, _

class report_helpdesk_activity(models.AbstractModel):
    _name = 'report.helpdesk_rhea.report_helpdesk_activity'

    @api.model
    def render_html(self, docids, data=None):
        print self          # TODO
        data = data if data is not None else {}
        budgets = self.env['helpdesk.budget'].search([])
        timesheets = self.env['account.analytic.line'].search([])
        docargs = {
            'docs': budgets,
            'data': {'budgets': budgets,
            'timesheets': timesheets,}
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