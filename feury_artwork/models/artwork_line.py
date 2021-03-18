# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ArtworkLine(models.Model):
    _name = 'artwork.line'
    _description = 'Artwork Line'

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
    )

    order = fields.Integer(
        string='Order',
        default=1
    )

    artwork_id = fields.Many2one(
        string="Artwork",
        comodel_name="artwork"
    )

    name = fields.Char(
        string='Name',
        related="color_id.name",
        required=True,
        readonly=False,
        unique=True
    )

    color_id = fields.Many2one(
        string="Code",
        comodel_name="color",
        required=True
    )

    color_hex_code = fields.Char(
        string="Hex Code",
        related="color_id.hex_code",
        readonly=False,
        store=True
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
