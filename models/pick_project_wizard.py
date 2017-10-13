# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class PickProjectWizard(models.TransientModel):
    _name = 'pick.project.wizard'
    _description = "Pick the helpdesk project"

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
        # make a new helpdesk_budget object
        so = self.env["sale.order"].search([('id','=', self._context['sale_order_id'])])
        hbo = self.env["helpdesk.budget"]
        hbo_to_write = {
            "sale_order_id": self._context['sale_order_id'],
            "project_id": self.project_selection,
            "amount_remaining": so.amount_untaxed,
        }

        chbo = hbo.create(hbo_to_write)
