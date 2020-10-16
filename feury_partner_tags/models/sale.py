# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_quotation_send(self):
        action_data = super(SaleOrder, self).action_quotation_send()
        action_data['context'].update({'change_partners': True})
        return action_data
