# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import float_compare


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_hold = fields.Boolean(compute='_compute_credit_hold')

    def _compute_credit_hold(self):
        for partner in self:
            partner.credit_hold = False
            if float_compare(self.total_due, self.credit_limit,
                             precision_rounding=self.currency_id.rounding) > 0:
                partner.credit_hold = True


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mfg_ids = fields.One2many(comodel_name='mrp.production', inverse_name='order_id', string='production orders')
    mfg_count = fields.Integer(string='Production orders', compute='_compute_mrp_order_ids')
    credit_hold = fields.Boolean(related='partner_id.credit_hold')
    show_confirm = fields.Boolean(compute='_compute_show_confirm')

    def _compute_show_confirm(self):
        for order in self:
            order.show_confirm = False if order.credit_hold else True
            if self.env.user.has_group('base.group_system') or self.env.user.has_group('sales_team.group_sale_manager'):
                order.show_confirm = True

    def _compute_mrp_order_ids(self):
        for order in self:
            order.mfg_count = len(order.mfg_ids)

    def action_view_manufacturing_orders(self):
        action_data = self.env.ref('mrp.mrp_production_action').read()[0]
        if len(self.mfg_ids) > 1:
            action_data['domain'] = [('id', 'in', self.mfg_ids.ids)]
        else:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action_data['views'] = form_view
            action_data['res_id'] = self.mfg_ids[0].id
        action_data['context'] = {'default_company_id': self.env.user.company_ids.ids[0]}
        return action_data

    def action_confirm(self):
        if self.partner_id.credit_hold and not (self.env.user.has_group('base.group_system') or self.env.user.has_group('sales_team.group_sale_manager')):
            message = "Customer is past credit limit. Please check with administrator to confirm this sales order."
            self.on_hold = True
            msg_wizard = self.env['sale.order.wizard'].create({'message': message, 'sale_id': self.id})
            return {
                'name': _("Warning"),
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.wizard',
                'res_id': msg_wizard.id,
                'view_mode': 'form',
                'view_id': self.env.ref('feury_mrp_sale.sale_order_wizard_view_form').id,
                'target': 'new',
            }
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_notes = fields.Text()


