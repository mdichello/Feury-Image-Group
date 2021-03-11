# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class EmbellishmentComposition(models.Model):
    _name = 'embellishment.composition'
    _description = 'Embellishment composition'

    _sql_constraints = [
        ('embellishment_composition_location_uniq', 'unique(embellishment_id, location)', 'No duplicate location are allowed within the same embellishment.')
    ]

    embellishment_id = fields.Many2one(
        string='Embellishment',
        comodel_name='embellishment',
    )

    clothing_type = fields.Selection(
        string='Clothing type',
        related='embellishment_id.clothing_type',
        store=True
    )

    is_other_location = fields.Boolean(
        string='IS other location',
        compute='_compute_is_other_location',
        store=True
    )

    type = fields.Selection(
        string='Type',
        related='artwork_id.type',
        store=True
    )

    location = fields.Char(
        compute='_compute_location',
        string='Location',
        store=True
    )

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
    )

    other_location = fields.Selection(
        selection=[
            ('other', 'Other'),
        ],
        string='Other locations',
    )

    pant_location = fields.Selection(
        selection=[
            ('left_cargo_pocket', 'Left Cargo Pocket'),
            ('right_cargo_pocket', 'Right Cargo Pocket'),
            ('left_back_pocket', 'Left Back Pocket'),
            ('right_back_pocket', 'Right Back Pocket'),
            ('left_side_leg', 'Left Side Leg'),
            ('right_side_leg', 'Right Side Leg'),
            ('booty', 'Booty'),
            ('back Yoke', 'Back Yoke'),
        ],
        string='Pant location',
    )

    top_location = fields.Selection(
        selection=[
            ('left_chest', 'Left Chest'),
            ('right_chest', 'Right Chest'),
            ('left_shoulder', 'Left Shoulder'),
            ('right_shoulder', 'Right Shoulder'),
            ('left_cuff', 'Left Cuff'),
            ('right_cuff', 'Right Cuff'),
            ('left_sleeve', 'Left Sleeve'),
            ('right_sleeve', 'Right Sleeve'),
            ('full_back', 'Full back'),
            ('yoke', 'Yoke'),
            ('other', 'Other'),
        ],
        string='Top location',
    )

    hat_location = fields.Selection(
        selection=[
            ('full_center_front', 'Full Center Front'),
            ('left_waist_apron', 'Left Waist Apron'),
            ('right_waist_apron', 'Right Waist Apron'),
            ('front_center', 'Front Center'),
            ('front_left', 'Front Left'),
            ('front_right', 'Front Right'),
            ('brim', 'Brim'),
            ('side_left', 'Side Left'),
            ('side_right', 'Side Right'),
            ('back', 'Back'),
        ],
        string='Apron location',
    )

    coverall_location = fields.Selection(
        selection=[
            ('left_cargo_pocket', 'Left Cargo Pocket'),
            ('right_cargo_pocket', 'Right Cargo Pocket'),
            ('left_back_pocket', 'Left Back Pocket'),
            ('right_back_pocket', 'Right Back Pocket'),
            ('left_side_leg', 'Left Side Leg'),
            ('right_side_leg', 'Right Side Leg'),
            ('booty', 'Booty'),
            ('back Yoke', 'Back Yoke'),

            ('left_chest', 'Left Chest'),
            ('right_chest', 'Right Chest'),
            ('left_shoulder', 'Left Shoulder'),
            ('right_shoulder', 'Right Shoulder'),
            ('left_cuff', 'Left Cuff'),
            ('right_cuff', 'Right Cuff'),
            ('left_sleeve', 'Left Sleeve'),
            ('right_sleeve', 'Right Sleeve'),
            ('full_back', 'Full back'),
            ('yoke', 'Yoke'),
            ('other', 'Other'),
        ],
        string='Apron location',
    )

    apron_location = fields.Selection(
        selection=[
            ('full_center_front', 'Full Center Front'),
            ('left_waist_apron', 'Left Waist Apron'),
            ('right_waist_apron', 'Right Waist Apron'),
        ],
        string='Apron location',
    )

    artwork_id = fields.Many2one(
        string='Artwork',
        comodel_name='artwork',
    )

    description = fields.Text(
        string='Description',
        required=False,
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

    @api.depends('clothing_type', 'pant_location', 'hat_location', 'top_location', 'hat_location')
    @api.onchange('clothing_type', 'pant_location', 'hat_location', 'top_location', 'hat_location')
    def _compute_location(self):
        for record in self:
            record.location = getattr('record', f'{record.clothing_type}_location', False) \
                if record.clothing_type \
                else False

    @api.depends('clothing_type')
    def _compute_is_other_location(self):
        for record in self:
            record.is_other_location = False \
                if record.clothing_type in ('pant', 'top', 'hat', 'coverall', 'apron')\
                else False

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
