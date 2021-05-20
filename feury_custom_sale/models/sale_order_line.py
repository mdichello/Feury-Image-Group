# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MaterialColor(models.Model):
    _inherit = 'sale.order.line'

    embellishment_id = fields.One2many(
        string='Embellishment',
        comodel_name='embellishment',
        inverse_name="sale_order_line_id"
    )

    clothing_type_id = fields.Many2one(
        string='Clothing type',
        comodel_name='clothes.type',
        required=False
    )

    embellishment_cost = fields.Monetary(
        string='Embellishment Cost', 
        readonly=False,
        default=0
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

    def action_open_embellishment_wizard(self):
        wizard_view_id = self.env.ref('feury_custom_sale.embellishment_form').id

        context = dict(self._context)
        context.update({
            "default_sale_order_line_id": self.id,
            "partner_id": self.order_id.partner_id.id,
            "location_ids": self.clothing_type_id.location_ids.ids,
        })

        result = {
            'type': 'ir.actions.act_window',
            'name': 'Embellishment',
            'res_model': 'embellishment',
            'view_mode': 'form',
            'target': 'new',
            'view_id': wizard_view_id,
            'context': context,
        }

        if self.embellishment_id:
            result.update({
                'res_id': self.embellishment_id[0].id
            })

        return result

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
