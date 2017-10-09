from odoo import models, fields, api

class HelpdeskBudget(models.Model):
    _name = "helpdesk.budget"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    project_id = fields.Many2one('project.project', string='Project')

    #sale_order_name = fields.Char()
    sale_order_date = fields.Date()
    amount = fields.Float()
    amount_remaining = fields.Float()

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

