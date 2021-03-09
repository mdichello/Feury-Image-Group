# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
# TODO ask mike about security group!


class Artwork(models.Model):
    _name = 'artwork'
    _description = 'Artwork'
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('artwork_reference_uniq', 'unique(reference, partner_id)', 'An artwork reference should be unique per partner.')
    ]

    # TODO ask mike about default value.
    type = fields.Selection(
        selection=[
            ('embroider', 'Embroider'),
            ('screen_print', 'Screen Print'),
            ('heat_seal', 'Heat Seal'),
            ('sew_patch', 'Sew Patch'),
            ('sew_stripe', 'Sew Stripe'),
            ('hem_pants', 'Hem Pants'),
        ],
        string='Type',
        required=True,
        default='heat_seal'
    )

    name = fields.Char(
        string='Name',
        required=True,
        unique=True
    )

    reference = fields.Char(
        string='Logo Number',
        required=True,
        unique=True
    )

    # TODO ask mike about required!
    image = fields.Image(
        string='Thumb Print',
        required=False
    )

    line_ids = fields.One2many(
        string="Artwork Lines",
        comodel_name="artwork.line",
        inverse_name="artwork_id"
    )

    stitch_count = fields.Integer(
        string='Stitch count',
        required=False,
        default=0
    )

    color_wave = fields.Char(
        string='Color wave',
        required=False,
    )

    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner', 
        ondelete='cascade', 
        index=True,
        domain=['&', ('parent_id', '=', False), ('is_customer', '=', True)], 
        required=False
    )

    company_id = fields.Many2one(
        comodel_name='res.company', 
        required=False,
        default=lambda self: self.env.company
    )

    is_default = fields.Boolean(
        string = 'Is default',
        default = False
    )

    active = fields.Boolean(
        string='Active',
        default=True
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

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
