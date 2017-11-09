# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = "Please select the dates for Timesheets:"

    date_from = fields.Datetime('Date From')
    date_until = fields.Datetime('Date Until')

    # action for a button
    @api.multi
    def make_report(self):
        current_project = self.env["project.project"].search([('id', '=', self._context['project_id'])])
        print current_project
        datas = {'project': self._context['project_id'],
                 }
        return {
        'type' : 'ir.actions.report.xml',
        'report_name' : 'helpdesk_rhea.report_helpdesk_activity',
        'datas' : datas,
        }

