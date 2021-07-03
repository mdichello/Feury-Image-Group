# -*- coding: utf-8 -*-
# License AGPL-3
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sellerscommerce_username = fields.Char(
        string='Sellerscommerce Username',
        config_parameter='feury_custom_sale.sellerscommerce_username'
    )

    sellerscommerce_password = fields.Char(
        string='ellerscommerce Password',
        config_parameter='feury_custom_sale.sellerscommerce_password'
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    def set_values(self):
        CONFIG_PARAMETER = self.env['ir.config_parameter']

        res = super(ResConfigSettings, self).set_values()
        CONFIG_PARAMETER.set_param('feury_custom_sale.sellerscommerce_username', self.sellerscommerce_username)
        CONFIG_PARAMETER.set_param('feury_custom_sale.sellerscommerce_password', self.sellerscommerce_password)
        return res

    @api.model
    def get_values(self):
        CONFIG_PARAMETER = self.env['ir.config_parameter']

        res = super(ResConfigSettings, self).get_values()
        PARAMETER = self.env['ir.config_parameter'].sudo()
        sellerscommerce_username = PARAMETER.get_param('feury_custom_sale.sellerscommerce_username')
        sellerscommerce_password = PARAMETER.get_param('feury_custom_sale.sellerscommerce_password')
        res.update(
            sellerscommerce_username=sellerscommerce_username,
            sellerscommerce_password=sellerscommerce_password
        )
        return res

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
