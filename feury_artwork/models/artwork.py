# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Artwork(models.Model):
    _name = 'artwork'
    _description = 'Artwork'
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('artwork_number_uniq', 'unique(number)', 'An artwork number should be unique.')
    ]

    reference = fields.Char(
        string='Logo Number',
        required=True,
        unique=True
    )

    image = fields.Image(
        string='Logo',
        max_width=350, 
        max_height=200,
        required=False
    )

    line_ids = fields.One2many(
        string="Artwork Lines",
        comodel_name="artwork.line",
        inverse_name="artwork_id"
    )

    partner_id = fields.Many2one(
        string='Partner', 
        comodel_name='res.partner', 
        ondelete='cascade', 
        index=True,
        domain=[('parent_id', '=', False)], 
        required=False
    )

    company_id = fields.Many2one(
        comodel_name='res.company', 
        required=False,
        default=lambda self: self.env.company
    )

    name = fields.Char(
        string='Name',
        required=True,
        unique=True
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
