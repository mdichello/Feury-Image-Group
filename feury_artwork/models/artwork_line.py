# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ArtworkLine(models.Model):
    _name = 'artwork.line'
    _description = 'Artwork Line'

    # TODO ask mike!
    # _sql_constraints = [
    #     ('artwork_number_uniq', 'unique(number)', 'An artwork number should be unique.')
    # ]

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
    )

    artwork_id = fields.Many2one(
        string="Artwork",
        comodel_name="artwork"
    )

    name = fields.Char(
        string='Name',
        required=True,
        unique=True
    )

    color_code = fields.Char(
        string='Color code',
        required=False,
        unique=True
    )

    color = fields.Char(
        string='Color',
        required=False,
        unique=True,
        default="#875a7b"
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
