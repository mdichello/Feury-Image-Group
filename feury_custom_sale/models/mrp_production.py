# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    embellishment_id = fields.Many2one(
        string="Embellishment", 
        comodel_name="embellishment", 
        related="product_id.embellishment_id",
        required=False,
        copy=False,
        readonly=True
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    def action_replenish(self):
        PRODUCT_REPLENISH = self.env['product.replenish']

        self.ensure_one()

        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy')

        for move in self.move_raw_ids:
            replenishment = PRODUCT_REPLENISH.create({
                'product_id': move.product_id.id,
                'product_tmpl_id': move.product_id.product_tmpl_id.id,
                'product_uom_id': move.product_id.uom_id.id,
                'quantity': move.product_uom_qty,
                'route_ids': [(6, 0, (buy_route.id, ))]
            })
            replenishment.launch_replenishment()

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
