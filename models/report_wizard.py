# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = _("Please select the dates for Timesheets:")

    date_from = fields.Datetime(string='Date From')
    date_until = fields.Datetime(string='Date Until')

    # action for a button
    @api.multi
    def make_report(self):
        datas = {'project': self._context['project_id'],
                 'date_from': self.date_from,
                 'date_until': self.date_until,
                 }
        return {
        'type' : 'ir.actions.report.xml',
        'report_name' : 'helpdesk_rhea.report_helpdesk_activity',
        'datas' : datas,  # accessed through "data" variable in render_html function in /helpdesk_rhea/report/report_helpdesk_activity.py
        }

