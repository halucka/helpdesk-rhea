# -*- coding: utf-8 -*-

from odoo import fields, models, api, _



class Project(models.Model):
    """Extends Project with attribute is_servicedesk and allows to associate budgets with Projects"""
    _inherit = 'project.project'
    is_servicedesk = fields.Boolean('Is a servicedesk')
    ticketprice = fields.Float('Helpdesk Ticket Price', default="25.0")
    tickettime = fields.Float('Helpdesk Ticket Time Unit in Minutes', default="15.0")
    budget_ids = fields.One2many(
               'helpdesk.budget', 'project_id',
               string='Budget ids'
           )

    budget_count = fields.Integer(string='Budgets', compute='_compute_budget_count')

    @api.multi
    def budget_tree_view(self):

        context = self._context.copy()
        return {
            'name': _('Budgets'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'helpdesk.budget',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': context,
            'domain':[["project_id","=",self.id]],
        }



    @api.multi
    def _compute_budget_count(self):
        for project in self:
            project.budget_count = len(project.budget_ids)

    @api.multi
    def debit_timesheet_on_budget(self):
        # run a wizard to select which project should new budget go to

        return {
            'name': _('Select dates: '),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pick.budget.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'key2': 'client_action_multi',
            'context': {'project_id': self.id,},  #'sale_order_id': self.id},
        }
