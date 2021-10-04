# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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

    def action_confirm(self):
        MRP = self.env['mrp.bom']

        for order in self:
            order_lines = order.order_line.filtered(lambda l: not l.display_type)
            manufacturing_route = self.env.ref('mrp.route_warehouse0_manufacture')
            mto_route = self.env.ref('stock.route_warehouse0_mto')
    
            for line in order_lines:
                product = line.product_id.product_tmpl_id
                # Add non copy fields.
                style_id = line.product_id.style_id and line.product_id.style_id.id
                embellished_product = product.sudo().copy({
                    'name': f'{line.product_id.name}-embellished',
                    'embellishment_id': line.embellishment_id.id,
                    'x_studio_vendor_sku': line.product_id.x_studio_vendor_sku,
                    'default_code': line.product_id.default_code,
                    # 'barcode': line.product_id.barcode,
                    'style_id': style_id,
                    'route_ids': [(6, 0, (manufacturing_route.id, mto_route.id))]
                })

                # Create bill of materials.
                bom  = MRP.sudo().create({
                    'product_tmpl_id': embellished_product.id,
                    'type': 'normal',
                    'product_qty': 1,
                    'bom_line_ids': [(
                        0, 0, {
                            'routing_id': False,
                            'sequence': 1,
                            'product_id': line.product_id.id,
                            'product_qty': 1
                        }
                    )]
                })

                line.write({
                    'product_id': embellished_product.product_variant_id.id,
                    'price_subtotal': line.price_subtotal,
                    'price_total': line.price_total,
                    'price_tax': line.price_tax,
                })

        res = super(SaleOrder, self).action_confirm()
        return res

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
