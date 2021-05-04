# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    _sql_constraints = [
        (
            'check_pricelist_validity_days', 
            'CHECK(pricelist_validity_days > 0)', 
            'Pricelist Validity is required and must be greater than 0.'
        )
    ]

    pricelist_validity_days = fields.Integer(
        default=30,
        string="Default Pricelist Validity (Days)"
    )

    def _get_default_pricelist_catalog_cover_page(self):
        pdf_path = get_resource_path('feury_pricelist', 'static/src/pdf/catalog_cover_page.pdf')
        pdf = False
        
        with open(pdf_path, 'rb') as f:
            pdf = f.read()

        return base64.encodestring(pdf)

    pricelist_catalog_cover_page = fields.Binary(
        string='Pricelist Catalog cover page',
        required=True,
        default=_get_default_pricelist_catalog_cover_page
    )
