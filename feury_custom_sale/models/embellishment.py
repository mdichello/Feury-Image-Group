# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import chain

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Embellishment(models.Model):
    _name = 'embellishment'
    _description = 'embellishment'

    sale_order_line_id = fields.Many2one(
        string='Sale order line',
        comodel_name='sale.order.line'
    )

    embroider_ids = fields.One2many(
        string="Embroider",
        comodel_name="embroider",
        inverse_name="embellishment_id"
    )

    sew_patch_ids = fields.One2many(
        string="Sew Patch",
        comodel_name="sew.patch",
        inverse_name="embellishment_id"
    )

    sew_stripe_ids = fields.One2many(
        string="Sew Stripe",
        comodel_name="sew.stripe",
        inverse_name="embellishment_id"
    )

    heat_seal_ids = fields.One2many(
        string="Heat Seal",
        comodel_name="heat.seal",
        inverse_name="embellishment_id"
    )

    screen_print_ids = fields.One2many(
        string="Screen Print",
        comodel_name="screen.print",
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
            ('screen_print', 'Screen Print'),
            ('heat_seal', 'Heat Seal'),
            ('sew_patch', 'Sew Patch'),
            ('sew_stripe', 'Sew Stripe'),
            ('hem_pants', 'Hem Pants'),
        ],
        required=True,
        string='Type',
        default='embroider'
    )

    hem_length = fields.Integer(
        string='Length',
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
            if not (22 <= record.hem_length <= 65):
                raise ValidationError(_("Please choose a hem length between 22 and 65."))

    @api.constrains(
        'embroider_ids', 
        'sew_patch_ids', 
        'sew_stripe_ids', 
        'heat_seal_ids', 
        'screen_print_ids'
    )
    def _check_duplicate_locations(self):
        for record in self:
            locations = set()
            duplicate_locations = set()

            for item in chain(
                record.embroider_ids,
                record.sew_patch_ids,
                record.sew_stripe_ids,
                record.heat_seal_ids,
                record.screen_print_ids
            ):
                if item.location_id.is_other_location:
                    continue

                elif item.location_id in locations:
                    duplicate_locations.add(item.location_id)
                
                else:
                    locations.add(item.location_id)

            if duplicate_locations:

                raise ValidationError(_(
                    'No duplicate location is allowed within the same '
                    'embellishment. \nFound duplicates: \n%s' % (
                        '\n'.join(location.name for location in duplicate_locations)
                    )
                ))

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    @api.depends('embroider_ids.location_id')
    def onchange_embroiders_location(self):
        pass

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
