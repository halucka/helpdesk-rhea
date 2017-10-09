# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class PickProjectWizard(models.TransientModel):
    _name = 'pick.project.wizard'
    _description = "Pick the helpdesk project"

    state = "open"

    project_selection = fields.Selection(selection='get_helpdesk_projects', string='Helpdesk Projects')

    def get_helpdesk_projects(self):
        lst = []
        number = 1
        for record in self.env['project.project'].search([]):
            if record.is_servicedesk:
                lst.append((record.id, record.name))
            number = number + 1
        return lst

    # action for a button
    def book_budget(self):
        print self.project_selection
        print self.state
        # TODO assign budget to helpdesk project
        self.state = "booked"
        print self.state









    # project_id = fields.Many2one('helpdesk.project',
    #     string="Project")   #, required=True)