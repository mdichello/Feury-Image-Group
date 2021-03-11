# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MaterialColor(models.Model):
    _name = 'embellishment'
    _description = 'embellishment'

    sale_order_line_id = fields.Many2one(
        string='Sale order line',
        comodel_name='sale.order.line'
    )

    line_ids = fields.One2many(
        string="Embellishment Composition",
        comodel_name="embellishment.composition",
        inverse_name="embellishment_id"
    )

    clothing_type = fields.Selection(
        string='Clothing type',
        related='sale_order_line_id.clothing_type',
        store=True
    )

    hem_length = fields.Integer(
        string='Hem lenght',
        default=0
    )

    material_color_id = fields.Many2one(
        string='Material Color',
        comodel_name='material.color',
    )

    material_type_id = fields.Many2one(
        string='Material Type',
        comodel_name='material.type',
    )

    material_size_id = fields.Many2one(
        string='Material size',
        comodel_name='material.size',
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

    def action_save(self):
        pass

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
