# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class ProductStyle(models.Model):
    _name = 'product.style'
    _description = 'Product style'

    _sql_constraints = [
        ('product_style_vendor_code_uniq', 'unique(code, vendor_code)', 'A product style code / vendor code should be unique.'),
        ('product_style_code_uniq', 'check(1=1)', 'A product style code should be unique.'),
    ]

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True
    )

    code = fields.Char(
        string='Style Code',
        required=True,
        unique=False
    )

    vendor_code = fields.Char(
        string='Vendor Code',
        required=True
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

    @api.depends('code', 'vendor_code')
    def _compute_name(self):
        for record in self:
            vendor_code = record.vendor_code or ''
            code = record.code or ''
            record.name = f'{vendor_code}-{code}'

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
    def _search_or_create_by_name(self, code, vendor_code):
        if not code or not vendor_code:
            return False
    
        style = self.search([
            ('code', '=', code),
            ('vendor_code', '=', vendor_code),
        ], limit=1)

        if not style:
            style = self.create({
                'code': code,
                'vendor_code': vendor_code
            })

        return style.id

    def name_get(self):
        return [(record.id, record.code) for record in self]
