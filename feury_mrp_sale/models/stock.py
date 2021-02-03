# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.utf

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_procurement_values(self):
        values = super(StockMove, self)._prepare_procurement_values()
        if self.sale_line_id:
            values.update({'sale_order_line': self.sale_line_id.id})
        if self.raw_material_production_id and self.raw_material_production_id.sale_line_id:
            values.update({'sale_order_line': self.raw_material_production_id.sale_line_id.id})
        return values


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values,
                         bom):
        mo_vals = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, company_id, values,
                         bom)
        if values.get('sale_order_line'):
            mo_vals.update({'sale_line_id': values.get('sale_order_line')})
        return mo_vals