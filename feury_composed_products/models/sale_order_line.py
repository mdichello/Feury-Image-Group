# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    active = fields.Boolean(
        string='Active',
        default=True
    )
