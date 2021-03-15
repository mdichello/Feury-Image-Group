# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ClothesType(models.Model):
    _name = 'clothes.type'
    _description = 'Location Clothes'

    _sql_constraints = [
        ('clothes_type_name_uniq', 'unique(name)', 'Duplicate are not allowed for clothes type names.')
    ]

    name = fields.Char(
        string='Name',
        required=True
    )

    @api.model
    def get_default_locations(self):
        return  [self.env.ref('feury_custom_sale.clothes_location_other').id, ]

    location_ids = fields.Many2many(
        comodel_name='clothes.location', 
        relation='clothes_type_location_rel', 
        column1='clothes_type_id', 
        column2='clothes_location_id', 
        string="Locations",
        default=get_default_locations
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

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
