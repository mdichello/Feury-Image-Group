# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import image_process
from odoo.exceptions import UserError, ValidationError


class EmbellishmentComposition(models.Model):
    _name = 'embellishment.composition'
    _description = 'Embellishment composition'

    embellishment_id = fields.Many2one(
        string='Embellishment',
        comodel_name='embellishment',
        copy=False
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

    is_per_print_location = fields.Boolean(
        string='IS other location',
        compute='_compute_is_per_print_location',
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
        readonly=True,
        domain=[('type', '=', False)], 
    )

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
        string='Personalization',
        required=False,
    )

    font = fields.Selection(
        string='Font',
        selection=[
            ('block', 'Block'),
            ('script', 'Script'),
        ],
        required=False,
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    @api.model
    def default_get(self, fields):
        ARTWORK = self.env['artwork']
        vals = super(EmbellishmentComposition, self).default_get(fields)
        if 'location_id' in fields:
            vals['location_id'] = self.env.ref('feury_custom_sale.clothes_location_other').id
        
        if 'artwork_id' in fields and self._context.get('partner_id'):
            default_artwork = ARTWORK.search(
                [
                    ('partner_id', '=', self._context.get('partner_id')),
                    ('is_default', '=', True),
                    ('type', '=', self._context.get('default_type')),
                ], 
                limit=1
            )
            vals['artwork_id'] = default_artwork.id

        return vals

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
        per_print_location = self.env.ref('feury_custom_sale.clothes_location_per_print')

        for record in self:
            is_other_location = True if record.location_id == other_location else False
            is_per_print_location = True if record.location_id == per_print_location else False

            record.write({
                'is_other_location': is_other_location,
                'is_per_print_location': is_per_print_location
            })


    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    @api.onchange('text')
    def onchnage_text(self):
        for record in self:
            if not record.text:
                continue

            lines = record.text.split('\n')
    
            line_count = len(lines) if record.text else 0
            if line_count > 4:
                raise UserError(_('You can not have more than four lines in text.'))

            if any(len(line) > 22 for line in lines):
                raise UserError(_('Each line is limited to only 22 characters'))

    @api.onchange('type')
    def onchnage_type(self):
        for record in self:
            if not record.type:
                continue

            record.write({
                'location_id': False,
                'artwork_id': False,
                'artwork_image': False,
                'thumbnail': False,
                'per_print_file': False,
                'text': False,
                'font': False,
            })
            
    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
