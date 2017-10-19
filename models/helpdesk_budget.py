from odoo import models, fields, api

class HelpdeskBudget(models.Model):
    _name = "helpdesk.budget"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    project_id = fields.Many2one('project.project', string='Project')

    sale_order_date = fields.Datetime('Order Date', related='sale_order_id.date_order')
    amount = fields.Float('Total Amount', compute='_compute_amount')
    amount_remaining = fields.Float('Amount Remaining')


    @api.multi
    def _compute_amount(self):
        for budget in self:
            budget.amount = budget.sale_order_id.amount_untaxed

    
