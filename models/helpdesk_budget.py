from odoo import models, fields, api

class HelpdeskBudget(models.Model):
    _name = "helpdesk.budget"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    project_id = fields.Many2one('project.project', string='Project')

    sale_order_date = fields.Datetime('Order Date', related='sale_order_id.date_order')
    amount = fields.Float('Total Amount', compute='_compute_amount')
    amount_remaining = fields.Float('Amount Remaining')

    def set_budget(self, sale_order_id, project_id):
        self.sale_order_id = sale_order_id
        self.sale_order_date = self.sale_order_id.date_order
        self.project_id = project_id
        #self.amount = self.sale_order_id.amount_untaxed
        #self.amount_remaining = self.amount
        return self


    def update_amount(self, spent_budget):
        self.amount_remaining = self.amount_remaining - spent_budget
        return self


    @api.multi
    def _compute_amount(self):
        for budget in self:
            budget.amount = budget.sale_order_id.amount_untaxed

    @api.multi
    def _get_default_amount_remaining(self):
        output = 0
        for budget in self:
            output = output+ budget.sale_order_id.amount_untaxed
        print output
        return output