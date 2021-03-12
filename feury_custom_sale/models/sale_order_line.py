# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MaterialColor(models.Model):
    _inherit = 'sale.order.line'

    clothing_type = fields.Selection(
        selection=[
            ('top', 'Top'),
            ('pant', 'Pant'),
            ('apron', 'Apron'),
            ('hat', 'Hat'),
            ('coverall', 'Coverall'),
            ('scarf', 'Scarf'),
            ('sock', 'Sock'),
            ('bag', 'Bag'),
            ('other', 'Other'),
        ],
        required=False,
        string='Clothing Type',
    )

    embellishment_id = fields.One2many(
        string='Embellishment',
        comodel_name='embellishment',
        inverse_name="sale_order_line_id"
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
            "is_pant": self.clothing_type == 'pant',
            "is_hat": self.clothing_type == 'hat',
            "is_apron": self.clothing_type == 'apron',
            "is_top": self.clothing_type == 'top',
            "is_coverall": self.clothing_type == 'coverall',
            "is_other": self.clothing_type not in ('pant', 'hat', 'apron', 'top', 'coverall'),
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
