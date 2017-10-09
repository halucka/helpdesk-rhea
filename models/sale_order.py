# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class SaleOrderInherited(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def book_budget_on_project(self):
        # run a wizard to select which project should new budget go to
        print self.name
        print self.amount_untaxed
        print self.partner_id

        return {
            'name': _('Pick Project Wizard'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pick.project.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'key2': 'client_action_multi',
        }
