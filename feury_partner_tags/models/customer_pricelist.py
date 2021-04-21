# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CustomerPricelist(models.Model):
    _inherit = 'customer.pricelist'

    def action_send(self):
        action_data = super(CustomerPricelist, self).action_send()
        action_data['context'].update({'change_partners': True})
        return action_data
