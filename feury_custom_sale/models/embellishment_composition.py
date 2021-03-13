# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import image_process
from odoo.exceptions import UserError


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

    other_location_name = fields.Char(
        string='Other location',
        required=False
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
            ('back_yoke', 'Back Yoke'),
            ('other', 'Other'),
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
            ('front_center', 'Front Center'),
            ('front_left', 'Front Left'),
            ('front_right', 'Front Right'),
            ('brim', 'Brim'),
            ('side_left', 'Side Left'),
            ('side_right', 'Side Right'),
            ('back', 'Back'),
            ('other', 'Other'),
        ],
        string='Hat location',
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
            ('other', 'Other'),
        ],
        string='Apron location',
    )

    artwork_id = fields.Many2one(
        string='Artwork',
        comodel_name='artwork',
        required=False,
    )

    artwork_image = fields.Binary(
        related='artwork_id.image', 
        related_sudo=True, 
        readonly=True
    )

    thumbnail = fields.Binary(
        readonly=1, 
        store=True, 
        attachment=True, 
        compute='_compute_thumbnail'
    )

    description = fields.Text(
        string='Description',
        required=False,
    )

    text = fields.Text(
        string='Text',
        required=False,
    )

    # TODO add constraint, can't choose both artwork and text.
    # TODO if sew (both strip and patch) is choosen, the text option is disabled.
    # TODO add constraint,if text option is choosen (no more than 4 lines)
    # TODO add field "other location", put in readonly if type != 'other" 

    # TODO "sew stripe", location if fixed into ("other", "Per Print") and artwork becomes invisible
    # TODO if "Per print" is choosen the user neeed to uploda an attachment.
    # TODO add other values for material objects
    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    @api.constrains('artwork_id', 'text')
    def _check_either_artwork_id_or_text(self):
        for record in self:
            pass
            # if record.type == 'hem_pants' and not (22 < record.hem_length < 65):
            #     raise ValidationError(_("Please choose a hem length between 22 and 65."))

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    @api.depends('clothing_type', 'other_location', 'pant_location', 'top_location', 'hat_location', 'coverall_location', 'apron_location')
    @api.onchange('clothing_type', 'other_location', 'pant_location', 'top_location', 'hat_location', 'coverall_location', 'apron_location')
    def _compute_location(self):
        for record in self:
            record.location = getattr(record, f'{record.clothing_type}_location', False) \
                if record.clothing_type \
                else False

    @api.depends('clothing_type')
    def _compute_is_other_location(self):
        for record in self:
            record.is_other_location = False \
                if record.clothing_type in ('pant', 'top', 'hat', 'coverall', 'apron')\
                else False

    @api.depends('artwork_image')
    def _compute_thumbnail(self):
        for record in self:
            try:
                record.thumbnail = image_process(record.artwork_image, size=(50, 50), crop='center')
            except UserError:
                record.thumbnail = False

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    @api.onchange('text')
    def onchnage_text(self):
        for record in self:
            if not (record.text or record.artwork_id):
                continue
    
            line_count = len(record.text.split('\n')) if record.text else 0
            if line_count > 4:
                raise UserError(_('You can not have more than four lines in text.'))

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
