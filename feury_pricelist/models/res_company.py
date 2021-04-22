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
