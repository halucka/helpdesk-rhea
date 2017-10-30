from odoo import fields, models, api, _

class helpdesk_report_pdf(models.AbstractModel):
    _name = 'report.helpdesk_rhea.helpdesk_report_pdf'


# https://www.odoo.com/forum/help-1/question/how-to-call-report-action-from-method-or-inside-method-17159

# this should be action to get a report after clicking on Button
    def generate_report(self):
        context = {}

        datas = {
            'ids': context.get('active_ids', []),
            'model': 'account.analytic.account',
            'form': data
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.analytic.account.balance',  # change this for my report name
            'datas': {},  # dictionary
        }