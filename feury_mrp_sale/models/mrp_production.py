# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_line_id = fields.Many2one(comodel_name='sale.order.line', string="Sale order line", copy=False)
    order_id = fields.Many2one(related='sale_line_id.order_id')
    order_description = fields.Text(related='sale_line_id.name', string='Order Description')
    custom_notes = fields.Text(related='sale_line_id.custom_notes')