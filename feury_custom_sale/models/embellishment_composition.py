# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import image_process
from odoo.exceptions import UserError, ValidationError


class EmbellishmentComposition(models.Model):
    _name = 'embellishment.composition'
    _description = 'Embellishment composition'

    # TODO beautify error message (UX).
    _sql_constraints = [
        ('embellishment_composition_location_uniq', 'unique(embellishment_id, location_id)', 'No duplicate location is allowed within the same embellishment.')
    ]

    embellishment_id = fields.Many2one(
        string='Embellishment',
        comodel_name='embellishment',
    )

    location_id = fields.Many2one(
        string='Location',
        comodel_name='clothes.location',
    )

    clothing_type_id = fields.Many2one(
        string='Clothing type',
        related='embellishment_id.clothing_type_id',
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

    embellishment_type = fields.Selection(
        string='Type',
        related='embellishment_id.type',
        store=True
    )

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
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

    # TODO ask mike about https://apps.odoo.com/apps/modules/13.0/image_preview_knk/.
    thumbnail = fields.Binary(
        readonly=1, 
        store=True, 
        attachment=True, 
        compute='_compute_thumbnail'
    )

    per_print_file = fields.Binary(
        string='Per Print',
        attachment=True,
    )

    description = fields.Text(
        string='Description',
        required=False,
    )

    text = fields.Text(
        string='Text',
        required=False,
    )

    # TODO if sew (both strip and patch) is choosen, the text option is disabled.

    # TODO "sew stripe", location if fixed into ("other", "Per Print") and artwork becomes invisible
    # TODO if "Per print" is choosen the user neeed to uploda an attachment.
    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    @api.constrains('artwork_id', 'text')
    def _check_either_artwork_id_or_text(self):
        for record in self:
            if record.artwork_id and record.text:
                raise ValidationError(_('You can set both the artwork and text at the same time.'))

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    @api.depends('artwork_image')
    def _compute_thumbnail(self):
        for record in self:
            try:
                record.thumbnail = image_process(record.artwork_image, size=(30, 30), crop='center')
            except UserError:
                record.thumbnail = False

    @api.depends('location_id')
    def _compute_is_other_location(self):
        other_location = self.env.ref('feury_custom_sale.clothes_location_other')
        for record in self:
            record.is_other_location = True if record.location_id == other_location else False

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
