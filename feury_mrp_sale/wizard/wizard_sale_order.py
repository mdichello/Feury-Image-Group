# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import  api, fields, models
from odoo.tools import float_compare


class WizardSaleOrder(models.TransientModel):
    _name = 'sale.order.wizard'
    _description = 'Sale Order Confirmation'

    sale_id = fields.Many2one(comodel_name='sale.order')
    message = fields.Text()

    def btn_response_ok(self):
        self.sale_id.on_hold = True
