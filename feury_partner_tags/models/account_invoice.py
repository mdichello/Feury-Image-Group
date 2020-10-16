# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_invoice_sent(self):
        action_data = super(AccountMove, self).action_invoice_sent()
        action_data['context'].update({'change_partners': True})
        return action_data
