# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging
import requests
import hashlib
import json

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from odoo.addons.feury_custom_sale.api.sellerscommerce import API as SellersCommerceConnector


log = logging.getLogger(__name__)


API_USERNAME_KEY = 'feury_custom_sale.sellerscommerce_username'
API_PASSWORD_KEY = 'feury_custom_sale.sellerscommerce_password'


# TODO Re-locate function to tools model!.
def download_image(url, encode_base64=False):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        
        if encode_base64:
            return base64.b64encode(response.content)
        
        return response.content
    except:
        return False


class ProductCatalog(models.Model):
    _name = 'sellerscommerce.product.catalog'
    _description = 'Sellerscommerce Product Catalog'
    _inherit = ['mail.thread']
    _check_company_auto = True

    _sql_constraints = [
        (
            'product_catalog_external_id_uniq', 
            'unique(external_id, company_id)', 
            'A product catalog external Id should be unique per company.'
        )
    ]

    name = fields.Char(
        string='Name',
        required=True,
        unique=True
    )

    logo = fields.Image(
        string='Logo',
        required=False
    )

    external_id = fields.Integer(
        string='External ID',
        required=True,
        index=True
    )

    approval_status = fields.Integer(
        string='Approval Status',
    )

    catalog_account_id = fields.Char(
        string='Catalog Account ID'
    )

    product_count = fields.Integer(
        string='Product Count',
        required=True
    )

    sku_count = fields.Integer(
        string='SKU Count',
        required=True
    )

    last_update_timestamp = fields.Datetime(
        string='Last update timestamp',
        required=True
    )

    has_inventory = fields.Boolean(
        string='Has Inventory',
        required=True,
    )

    has_dropship = fields.Boolean(
        string='Has dropship',
        required=True,
    )

    partner_id = fields.Many2one(
        string='Partner',
        comodel_name='res.partner', 
        ondelete='cascade', 
        index=True,
        domain=['&', ('parent_id', '=', False), ('is_vendor', '=', True)], 
        required=False
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        required=False,
        default=lambda self: self.env.company
    )

    hash = fields.Char(
        string='Hash',
        required=True
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    @api.model
    def get_api_connection(self):
        CONFIG_PARAMETER = self.env['ir.config_parameter']

        log.info('Started sellerscommerce product catalog synchronization')
        get_param = CONFIG_PARAMETER.sudo().get_param

        api_username = get_param(API_USERNAME_KEY, default=False)
        api_password = get_param(API_PASSWORD_KEY, default=False)

        if not api_username or not api_password:
            log.info('Credentials not set, skip sellerscommerce catalog sync')

        api = SellersCommerceConnector(
            username=api_username, 
            password=api_password
        )

        return api

    @api.model
    def api_catalog_sync(self):
        api = self.get_api_connection()
        external_catalogs = api.catalogs()

        # Archive all catalogs before sync.
        catalogs = self.search([])
        catalogs.write({'active': False})

        for external_catalog in external_catalogs:
            try:
                external_id = int(external_catalog.id)
                domain = [
                    ('external_id', '=', external_id),
                    ('active', '=', False),
                ]
                catalog = self.search(domain, limit=1)

                # Prepare values.
                values = {
                    'name': external_catalog.name,
                    'logo': download_image(external_catalog.logo, encode_base64=True),
                    'external_id': external_catalog.id,
                    'approval_status': external_catalog.approvalStatus,
                    'catalog_account_id': external_catalog.catalogAccountID,
                    'product_count': external_catalog.productCount,
                    'sku_count': external_catalog.skuCount,
                    'last_update_timestamp': external_catalog.lastPublishedDate,
                    'has_inventory': external_catalog.hasInventory,
                    'has_dropship': external_catalog.hasDropship,
                    'hash': external_catalog.hash,
                    'company_id': False,
                    'active': True
                }

                # Already exists and changed on the API.
                if catalog and catalog.hash != external_catalog.hash:
                    catalog.write(values)

                # Is not synced yet.
                else:
                    catalog = self.create(values)
                    log.info(f'A new product catalog is synced id {catalog.id}')

            except Exception as e:
                log.error('Unexpected error', e)

            else:
                self.env.cr.commit()

    @api.model
    def api_product_sync(self):
        pass

    @api.model
    def api_data_sync(self):
        # TODO start a new thread.
        self.api_catalog_sync()
        self.api_product_sync()

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    @api.model
    def create(self, values):
        PARTNER = self.env['res.partner']

        if not values.get('partner_id', False):
            partner = PARTNER.create({
                'name': values.get('name'),
                'is_vendor': True,
                'is_customer': False
            })
            values['partner_id'] = partner.id
        return super(ProductCatalog, self).create(values)

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
