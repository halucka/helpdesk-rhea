# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class Project(models.Model):
    """Extends Project with attribute is_servicedesk and allows to associate budgets with Projects"""
    _inherit = 'project.project'
    is_servicedesk = fields.Boolean('Is a servicedesk')
    budget_ids = fields.One2many(
               'helpdesk.budget', 'project_id',
               string='Budget ids'
           )

    @api.multi
    def budget_tree_view(self):
        print "budget_tree_view"
        view_id = self.env.ref('helpdesk_rhea.helpdesk_budget_view_tree').id
        context = self._context.copy()
        return {
            'name': _('Budgets'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'helpdesk.budget',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': context,
        }

    budget_button_field = fields.Integer(string='Budgets')


