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
    def prepare_product_values(self, catalog, external_product):
        PRODUCT_SUPPLIER_INFO = self.env['product.supplierinfo']
        PRODUCT_BRAND = self.env['product.brand']
        PRODUCT_CATEGORY = self.env['product.category']
        PRODUCT_IMAGE = self.env['product.image']

        # Image processing.
        images = [
            download_image(image_url, encode_base64=True) 
            for image_url in external_product.images
        ]
        main_image = images[0] if images else False

        # Brand processing.
        brand = PRODUCT_BRAND.search([
            ('name', '=', external_product.brandName)
        ], limit=1)

        if not brand:
            brand = PRODUCT_BRAND.create({
                'name': external_product.brandName,
                'image': download_image(
                    external_product.brandImage,
                    encode_base64=True
                )
            })

        # Prepare image values and conserve the sequence number.
        image_values = [
            {
                'name': external_product.productName,
                'image_1920': image,
                'sequence': index + 10
            }
            for index, image in enumerate(images)
            if image
        ]

        images = PRODUCT_IMAGE.create(image_values) \
            if image_values \
            else PRODUCT_IMAGE

        # Supplier pricelist.
        supplier_info = PRODUCT_SUPPLIER_INFO.create({
            'name': catalog.partner_id.id,
            'product_name': external_product.productName,
            'product_code': external_product.productCode,
            'price': external_product.costPrice,
            'min_qty': 0,
            'company_id': False
        })

        # Product categories.
        categories = PRODUCT_CATEGORY
        for external_category in external_product.categories:
            category = PRODUCT_CATEGORY.search([
                '|',
                ('name', '=', external_category.name),
                ('external_id', '=', external_category.id)
            ])
            if not category:
                category = PRODUCT_CATEGORY.create({
                    'name': external_category.name,
                    'external_id': external_category.id,
                })
            categories += category

        # Prepare values.
        values = {
            'name': external_product.productName,
            'type': 'product',
            'catalog_id': catalog.id,
            'external_id': external_product.id,
            'brand_id': brand.id,
            'msrp': external_product.msrp,
            'map': external_product.map,
            'standard_price': external_product.costPrice,
            'list_price': external_product.msrp,
            'width': external_product.width,
            'height': external_product.height,
            'length': external_product.length,
            'size_chart': download_image(external_product.sizeChart, encode_base64=True),
            'description_html': external_product.description,
            'hash': external_product.hash,
            'image_1920': main_image,
            'image_ids': [(6, 0, images.ids)],
            'seller_ids': [(6, 0, supplier_info.ids)],
            'category_ids': [(6, 0, categories.ids)],
            'categ_id': categories[0].id if categories else False
        }

        return values

    @api.model
    def api_product_sync(self):
        # TODO add thread fork.
        PRODUCT_TEMPLATE = self.env['product.template']

        api = self.get_api_connection()
        catalogs = self.search([])

        for catalog in catalogs:
            external_products = api.products(
                catalog.external_id, 
                catalog.product_count
            )

            for external_product in external_products:
                try:
                    external_id = int(external_product.id)
                    domain = [
                        ('external_id', '=', external_id),
                        ('catalog_id', '=', catalog.id)
                    ]
                    product = PRODUCT_TEMPLATE.search(domain, limit=1)

                    # Already exists and changed on the API.
                    if product and product.hash != external_product.hash:
                        values = self.prepare_product_values(
                            catalog, 
                            external_product
                        )
                        product.write(values)

                    # Is not synced yet.
                    elif not product:
                        values = self.prepare_product_values(
                            catalog, 
                            external_product
                        )
                        product = PRODUCT_TEMPLATE.create(values)
                        log.info(f'A new product is synced id {product.id}')

                except Exception as e:
                    log.error('Unexpected error', e)

                else:
                    self.env.cr.commit()

    @api.model
    def api_data_sync(self):
        # TODO start a new thread.
        #self.api_catalog_sync()
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
