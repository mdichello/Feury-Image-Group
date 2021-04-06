# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _send_confirmation_email(self):
        self = self.with_context(change_partners=True)
        return super(StockPicking, self)._send_confirmation_email()
