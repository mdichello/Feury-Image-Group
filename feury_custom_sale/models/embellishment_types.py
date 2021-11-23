# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import mimetypes

from odoo import api, fields, models, _
from odoo.tools import image_process
from odoo.exceptions import ValidationError, UserError
from odoo.tools.mimetypes import guess_mimetype


class HemPants(models.Model):
    _name = 'hem.pant'
    _description = 'Hem Pant'

    embellishment_id = fields.Many2one(
        string='Embellishment',
        comodel_name='embellishment',
    )

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
    )

    length = fields.Integer(
        string='Length',
        default=22
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    @api.constrains('length')
    @api.onchange('length')
    def _check_hem_lenght(self):
        for record in self:
            if not (22 <= record.length <= 65):
                raise ValidationError(_("Please choose a hem length between 22 and 65."))

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

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


class Embroider(models.Model):
    _name = 'embroider'
    _description = 'Embroider'

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

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
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

    type = fields.Char(
        string='Type',
        required=True,
        default='embroider',
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
        vals = super(Embroider, self).default_get(fields)
        if 'location_id' in fields:
            vals['location_id'] = self.env.ref('feury_custom_sale.clothes_location_other').id
        
        if 'artwork_id' in fields and self._context.get('partner_id'):
            default_artwork = ARTWORK.search(
                [
                    ('partner_id', '=', self._context.get('partner_id')),
                    ('is_default', '=', True),
                    ('type', '=', 'embroider'),
                ], 
                limit=1
            )
            vals['artwork_id'] = default_artwork.id

        return vals

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # TODO fix this constraint.
    # @api.constrains('artwork_id', 'text')
    # def _check_either_artwork_id_or_text(self):
    #     for record in self:
    #         if record.artwork_id and record.text:
    #             raise ValidationError(_('You can set both the artwork and text at the same time.'))

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

            if record.artwork_id:
                record.artwork_id = False

            lines = record.text.split('\n')
    
            line_count = len(lines) if record.text else 0
            if line_count > 4:
                raise UserError(_('You can not have more than four lines in text.'))

            if any(len(line) > 22 for line in lines):
                raise UserError(_('Each line is limited to only 22 characters'))
            
    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------


class SewPatch(models.Model):
    _name = 'sew.patch'
    _description = 'Sew Patch'

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

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
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

    type = fields.Char(
        string='Type',
        required=True,
        default='sew_patch',
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
        vals = super(SewPatch, self).default_get(fields)
        if 'location_id' in fields:
            vals['location_id'] = self.env.ref('feury_custom_sale.clothes_location_other').id
        
        if 'artwork_id' in fields and self._context.get('partner_id'):
            default_artwork = ARTWORK.search(
                [
                    ('partner_id', '=', self._context.get('partner_id')),
                    ('is_default', '=', True),
                    ('type', '=', 'sew_patch'),
                ], 
                limit=1
            )
            vals['artwork_id'] = default_artwork.id

        return vals

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # TODO fix this constraint.
    # @api.constrains('artwork_id', 'text')
    # def _check_either_artwork_id_or_text(self):
    #     for record in self:
    #         if record.artwork_id and record.text:
    #             raise ValidationError(_('You can set both the artwork and text at the same time.'))

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
            
    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------


class SewStripe(models.Model):
    _name = 'sew.stripe'
    _description = 'Sew Stripe'

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
    
    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
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

    type = fields.Char(
        string='Type',
        required=True,
        default='sew_patch',
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

    @api.model
    def default_get(self, fields):
        ARTWORK = self.env['artwork']
        vals = super(SewStripe, self).default_get(fields)
        if 'location_id' in fields:
            vals['location_id'] = self.env.ref('feury_custom_sale.clothes_location_other').id
        
        if 'artwork_id' in fields and self._context.get('partner_id'):
            default_artwork = ARTWORK.search(
                [
                    ('partner_id', '=', self._context.get('partner_id')),
                    ('is_default', '=', True),
                    ('type', '=', 'sew_stripe'),
                ], 
                limit=1
            )
            vals['artwork_id'] = default_artwork.id

        return vals

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # TODO fix this constraint.
    # @api.constrains('artwork_id', 'text')
    # def _check_either_artwork_id_or_text(self):
    #     for record in self:
    #         if record.artwork_id and record.text:
    #             raise ValidationError(_('You can set both the artwork and text at the same time.'))

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

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------


class HeatSeal(models.Model):
    _name = 'heat.seal'
    _description = 'Heat Seal'

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

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
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

    type = fields.Char(
        string='Type',
        required=True,
        default='embroider',
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
        vals = super(HeatSeal, self).default_get(fields)
        if 'location_id' in fields:
            vals['location_id'] = self.env.ref('feury_custom_sale.clothes_location_other').id
        
        if 'artwork_id' in fields and self._context.get('partner_id'):
            default_artwork = ARTWORK.search(
                [
                    ('partner_id', '=', self._context.get('partner_id')),
                    ('is_default', '=', True),
                    ('type', '=', 'heat_seal'),
                ], 
                limit=1
            )
            vals['artwork_id'] = default_artwork.id

        return vals

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # TODO fix this constraint.
    # @api.constrains('artwork_id', 'text')
    # def _check_either_artwork_id_or_text(self):
    #     for record in self:
    #         if record.artwork_id and record.text:
    #             raise ValidationError(_('You can set both the artwork and text at the same time.'))

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
            
    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------


class ScreenPrint(models.Model):
    _name = 'screen.print'
    _description = 'Sreen Print'

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

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
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

    type = fields.Char(
        string='Type',
        required=True,
        default='screenp_print',
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
        vals = super(ScreenPrint, self).default_get(fields)
        if 'location_id' in fields:
            vals['location_id'] = self.env.ref('feury_custom_sale.clothes_location_other').id
        
        if 'artwork_id' in fields and self._context.get('partner_id'):
            default_artwork = ARTWORK.search(
                [
                    ('partner_id', '=', self._context.get('partner_id')),
                    ('is_default', '=', True),
                    ('type', '=', 'screen_print'),
                ], 
                limit=1
            )
            vals['artwork_id'] = default_artwork.id

        return vals

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # TODO fix this constraint.
    # @api.constrains('artwork_id', 'text')
    # def _check_either_artwork_id_or_text(self):
    #     for record in self:
    #         if record.artwork_id and record.text:
    #             raise ValidationError(_('You can set both the artwork and text at the same time.'))

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
            
    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
