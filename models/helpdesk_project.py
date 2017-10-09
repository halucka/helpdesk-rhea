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
        # self.ensure_one()
        # domain = [
        #     '|',
        #     '&', ('res_model', '=', 'project.project'), ('res_id', 'in', self.ids),
        #     '&', ('res_model', '=', 'project.task'), ('res_id', 'in', self.task_ids.ids)]
        return {
            'name': _('Budgets'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pick.project.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'key2': 'client_action_multi',
        }

    budget_button_field = fields.Integer(string='ATC')


    # class ProductTemplate(models.Model):
    #     _inherit = 'product.template'
    #
    #     is_contract = fields.Boolean('Is a contract')
    #     contract_template_id = fields.Many2one(
    #         comodel_name='account.analytic.contract',
    #         string='Contract Template',
    #     )
    #
    #     @api.onchange('is_contract')
    #     def _change_is_contract(self):
    #         """ Clear the relation to contract_template_id when downgrading
    #         product from contract
    #         """
    #         if not self.is_contract:
    #             self.contract_template_id = False