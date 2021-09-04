# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64

from odoo import api, fields, models, tools
from odoo.modules.module import get_module_resource


class Color(models.Model):
    _name = 'color'
    _description = 'Color'
    _rec_name = 'code'

    _sql_constraints = [
        ('color_code_uniq', 'unique(code)', 'A color code should be unique.')
    ]

    image = fields.Image(
        string="Image",
        max_width=128, 
        max_height=128,
        required=False
    )

    code = fields.Char(
        string='Code',
        required=True,
        unique=True
    )

    name = fields.Char(
        string='Name',
        required=False,
    )

    hex_code = fields.Char(
        string='Hex Code',
        required=False,
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

    @api.model
    @tools.ormcache('name')
    def _search_or_create_by_name(self, name):
        if not name:
            return False
    
        color = self.search([('name', 'ilike', name)], limit=1)

        if not color:
            color = self.create({
                'name': name,
                'code': name,
                'hex_code': 'FFFFF',
            })

        return color.id
