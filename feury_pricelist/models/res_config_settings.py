# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pricelist_validity_days = fields.Integer(
        related='company_id.pricelist_validity_days', 
        string="Default Pricelist Validity (Days)", 
        readonly=False
    )
    use_pricelist_validity_days = fields.Boolean(
        "Default Pricelist Validity", 
        config_parameter='feury_pricelist.use_pricelist_validity_days'
    )

    @api.onchange('use_pricelist_validity_days')
    def _onchange_use_pricelist_validity_days(self):
        RES_COMPANY = self.env['res.company']
        if self.pricelist_validity_days <= 0:
            self.pricelist_validity_days = RES_COMPANY.default_get(
                ['pricelist_validity_days']
            )['pricelist_validity_days']

    @api.onchange('pricelist_validity_days')
    def _onchange_pricelist_validity_days(self):
        RES_COMPANY = self.env['res.company']
        if self.pricelist_validity_days <= 0:
            self.pricelist_validity_days = RES_COMPANY.default_get(
                ['pricelist_validity_days']
            )['pricelist_validity_days']
            return {
                'warning': {
                    'title': "Warning", 
                    'message': "Pricelist Validity is required and must be greater than 0."
                },
            }
