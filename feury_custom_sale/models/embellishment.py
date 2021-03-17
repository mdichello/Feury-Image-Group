# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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

    clothing_type_id = fields.Many2one(
        string='Clothing type',
        related='sale_order_line_id.clothing_type_id',
        store=True
    )

    type = fields.Selection(
        selection=[
            ('embroider', 'Embroider'),
            ('screenp_print', 'Screen Print'),
            ('heat_seal', 'Heat Seal'),
            ('sew_patch', 'Sew Patch'),
            ('sew_stripe', 'Sew Stripe'),
            ('hem_pants', 'Hem Pants'),
        ],
        required=True,
        string='Type',
    )

    hem_length = fields.Integer(
        string='Hem lenght',
        default=22
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

    @api.constrains('hem_length')
    @api.onchange('hem_length')
    def _check_hem_lenght(self):
        for record in self:
            if record.type == 'hem_pants' and not (22 < record.hem_length < 65):
                raise ValidationError(_("Please choose a hem length between 22 and 65."))

    @api.constrains('line_ids')
    def _check_line_ids(self):
        for record in self:
            location_ids = [line.location_id.id for line in record.line_ids]

            if len(set(location_ids)) != len(location_ids):
                raise ValidationError(_('No duplicate location is allowed within the same embellishment.'))

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
