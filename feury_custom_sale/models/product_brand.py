# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product brand'

    _sql_constraints = [
        ('product_brand_name_uniq', 'unique(name)', 'Duplicate are not allowed for product brand names.')
    ]

    name = fields.Char(
        string='Name',
        required=True,
        index=True
    )

    image = fields.Image(
        string='Image',
        required=False
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

    @property
    def is_other_location(self):
        self.ensure_one()
        return self == self.env.ref('feury_custom_sale.clothes_location_other')
