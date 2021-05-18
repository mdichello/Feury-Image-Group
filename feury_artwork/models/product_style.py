# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductStyle(models.Model):
    _name = 'product.style'
    _description = 'Product style'

    _sql_constraints = [
        ('product_style_vendor_code_uniq', 'unique(code, vendor_code)', 'A product style code / vendor code should be unique.')
    ]

    code = fields.Char(
        string='Style Code',
        required=True
    )

    vendor_code = fields.Char(
        string='Vendor Code',
        required=False
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    def name_get(self):
        return [
            (
                record.id, 
                f'{record.vendor_code}-{record.code}' if record.vendor_code else f'{record.code}'
            )
            for record in self
        ]

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
