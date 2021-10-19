# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging
import requests

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
from odoo.addons.feury_custom_sale.api.sellerscommerce import API as SellersCommerceConnector


log = logging.getLogger(__name__)


API_USERNAME_KEY = 'feury_custom_sale.sellerscommerce_username'
API_PASSWORD_KEY = 'feury_custom_sale.sellerscommerce_password'
API_PROCESSING_BATCH_SIZE = 'feury_custom_sale.sellerscommerce_batch_size'

WORK_UNIT_MODEL = 'sellerscommerce.product.sync.work.unit'


# TODO make cron to unlock pending work units (after 5 hours for example)
# TODO Re-locate function to tools model!.
# TODO set a reasonable timeout.
def download_image(url, encode_base64=False):
    try:
        response = requests.get(url, allow_redirects=True, timeout=4)
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
        unique=True,
        index=True
    )

    approval_status = fields.Integer(
        string='Approval Status',
    )

    catalog_account_id = fields.Char(
        string='Catalog Account ID'
    )

    item_count = fields.Integer(
        string='Item Count',
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

    product_ids = fields.One2many(
        string='Products',
        comodel_name='product.template',
        inverse_name='catalog_id',
    )

    product_count = fields.Integer(
        compute='_compute_product_count',
    )

    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.product_ids)

    def action_view_products(self):
        return {
            'name': _('Products'),
            'res_model': 'product.template',
            'view_mode': 'kanban,tree,form',
            'type': 'ir.actions.act_window',
            'domain': [('catalog_id', 'in', self.ids)]
        }

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
                    '|',
                    ('active', '=', False),
                    ('active', '=', True),
                ]
                catalog = self.search(domain, limit=1)

                # Catalog did not change (hash).
                if catalog and catalog.hash == external_catalog.hash:
                    catalog.active = True
                    continue

                # Prepare values.
                values = {
                    'name': external_catalog.name,
                    'logo': download_image(external_catalog.logo, encode_base64=True),
                    'external_id': external_catalog.id,
                    'approval_status': external_catalog.approvalStatus,
                    'catalog_account_id': external_catalog.catalogAccountID,
                    'item_count': external_catalog.productCount,
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
    def _prepare_product_values(self, catalog, external_product):
        PRODUCT_SUPPLIER_INFO = self.env['product.supplierinfo']
        PRODUCT_BRAND = self.env['product.brand']
        PRODUCT_CATEGORY = self.env['product.category']

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
            'seller_ids': [(6, 0, supplier_info.ids)],
            'category_ids': [(6, 0, categories.ids)],
            'categ_id': categories[0].id if categories else False,
            'vendor_code': catalog.name,
            'x_studio_vendor_sku': False,
            'default_code': False,
            'barcode': False,
            'style_id': False,
            'color_id': False,
            'size_id': False,
            'active': True
        }

        return values

    @api.model
    def _prepare_image_values(self, image_urls, name):
        PRODUCT_IMAGE = self.env['product.image']

        images = [
            download_image(image_url, encode_base64=True) 
            for image_url in image_urls
        ]
        main_image = images[0] if images else False

        # Prepare image values and conserve the sequence number.
        image_values = [
            {
                'name': name,
                'image_1920': image,
                'sequence': index + 10
            }
            for index, image in enumerate(images)
            if image
        ]

        images = PRODUCT_IMAGE.create(image_values) \
            if image_values \
            else PRODUCT_IMAGE

        return images.ids, main_image

    @api.model
    def api_product_sync(self, work_unit):
        PRODUCT_SKU = self.env['sellerscommerce.product.virtual.inventory']
        PRODUCT_TEMPLATE = self.env['product.template']
        PRODUCT_STYLE = self.env['product.style']
        PRODUCT_SIZE = self.env['product.size']
        COLOR = self.env['color']

        api = self.get_api_connection()

        external_products = api.products(
            work_unit.catalog_id.external_id, 
            work_unit.start_index,
            work_unit.end_index,
        )

        vendor_code = work_unit.vendor_code

        for external_product in self.web_progress_iter(external_products, msg='Synching products'):
            try:
                external_id = int(external_product.id)

                # SKU processing.
                skus = api.product_sku(
                    work_unit.catalog_id.external_id,
                    external_id
                )

                sku_values = []

                # Style processing.
                style_code = external_product.productCode
                style_id = PRODUCT_STYLE._search_or_create_by_name(style_code, vendor_code)

                for sku in self.web_progress_iter(skus, msg='Synching SKU'):
                    # Missing data in the sku unit.
                    if not (sku.color and sku.size):
                        log.warning(f'product skipped: missing size of color {sku}')
                        continue
                    
                    size_id = PRODUCT_SIZE._search_or_create_by_name(sku.size)
                    color_id = COLOR._search_or_create_by_name(sku.color)
                    product = PRODUCT_TEMPLATE

                    # First search using the UPC.
                    if sku.upc:
                        domain = [
                            ('barcode', '=', sku.upc),
                            '|',
                            ('active', '=', True),
                            ('active', '=', False)
                        ]
                        product = PRODUCT_TEMPLATE.search(domain, limit=1)
                    
                    elif not product:
                        domain = [
                            ('catalog_id', '=', work_unit.catalog_id.id),
                            ('external_id', '=', external_id),
                            ('style_id', '=', style_id),
                            ('color_id', '=', color_id),
                            ('size_id', '=', size_id),
                            '|',
                            ('active', '=', True),
                            ('active', '=', False)
                        ]
                        product = PRODUCT_TEMPLATE.search(domain, limit=1)

                    # Product does not yet exists or changed on the API.
                    if not product or product.hash != external_product.hash:
                        values = self._prepare_product_values(
                            work_unit.catalog_id, 
                            external_product,
                        )

                        x_studio_vendor_sku = f'{style_code}-{sku.color}-{sku.size}'
                        default_code = f'{vendor_code}-{x_studio_vendor_sku}'

                        # Image processing.
                        image_ids, main_image = self._prepare_image_values(
                            sku.bigImages.split('|'), 
                            external_product.productName
                        )

                        cost, msrp, map = sku.costPrice, sku.msrp, sku.map

                        # MSRP is equal to the COST, leave the msrp and the map and the cost as zero.
                        if msrp == cost:
                            map = cost = 0

                        values.update({
                            'color_id': color_id,
                            'style_id': style_id,
                            'size_id': size_id,
                            'weight': sku.weight,
                            'barcode': sku.upc,
                            'msrp': msrp,
                            'map': map,
                            'list_price': msrp,
                            'vendor_code': vendor_code,
                            'x_studio_vendor_sku': x_studio_vendor_sku.upper(),
                            'default_code': default_code.upper(),
                            'image_1920': main_image,
                            'image_ids': [(6, 0, image_ids)],
                            'last_api_sync_reference': work_unit.reference
                        })

                        # Already exists and changed on the API.
                        if product:
                            product.write(values)

                        # Is not synced yet.
                        else:
                            product = PRODUCT_TEMPLATE.create(values)
                            log.info(f'A new product is synced id {product.id}')
                        
                        # Check SKU exist.
                        if product.exists():
                            # Change the cost value of the product.
                            product.product_variant_ids._change_standard_price(
                                cost
                            )
                            sku_values.append({
                                'product_id': product.id,
                                'availability_date': sku.skuAvailableDate,
                                'quantity': sku.stock,
                                'external_id': sku.id
                            })

                    else:
                        # Update reference to the last API sync operation.
                        product.write({
                            'active': True,
                            'last_api_sync_reference': work_unit.reference
                        })
                        log.info(f'Skipped product {product.id} [No change detected]')
                    
                    # Save changes.
                    self.env.cr.commit()

                if sku_values:
                    PRODUCT_SKU.create(sku_values)
                    # Save changes.
                    self.env.cr.commit()

            except Exception as e:
                log.error('Unexpected error', e)

    @api.model
    def _get_last_sync_operation_reference(self):
        query =  """
            SELECT reference 
            FROM sellerscommerce_product_sync_work_unit 
            WHERE id = (
                SELECT MAX(id) 
                FROM sellerscommerce_product_sync_work_unit 
                WHERE state = 'done'
            )
        """
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()
        return result[0] if result else False

    @api.model
    def create_product_sync_work_units(self, archive_discontinued_products):
        PRODUCT_SYNC_WORK_UNIT = self.env['sellerscommerce.product.sync.work.unit']
        CONFIG_PARAMETER = self.env['ir.config_parameter']
        PRODUCT_TEMPLATE = self.env['product.template']
        IR_SEQUENCE = self.env['ir.sequence']

        log.info('Started sellerscommerce product sync work unit creation')
        get_param = CONFIG_PARAMETER.sudo().get_param

        batch_size = int(get_param(API_PROCESSING_BATCH_SIZE, default=100))
        catalogs = self.search([])

        # Unblock pending work units (e.g: due to a CRON timeout the operation did not complete)
        stuck_work_units = PRODUCT_SYNC_WORK_UNIT.search([
            ('state', '=', 'pending')
        ])

        if stuck_work_units:
            stuck_work_units.state = 'waiting'

        waiting_work_units = PRODUCT_SYNC_WORK_UNIT.search([
            ('state', '=', 'waiting')
        ])

        # Sync iteration did not finish yet.
        if waiting_work_units:
            pervious_operations = set(waiting_work_units.mapped('reference'))
            references = ','.join(pervious_operations)
            message = f'Planning for a sync operation is skipped since '
            f'the previous one "{references}" did not complete yet'
            log.info(message)

            for catalog in catalogs:
                catalog.message_post(body=message)

            return None
        
        # Previous sync operation completed.
        else:
            # Fetch previous sync operation reference.
            last_sync_reference = self._get_last_sync_operation_reference()

            # Update directly using SQL!
            if archive_discontinued_products and last_sync_reference:
                domain = [
                    ('external_id', '!=', False),
                    ('last_api_sync_reference', '!=', last_sync_reference)
                ]
                products = PRODUCT_TEMPLATE.search(domain)
                products.active = False

        # Get a sequence for the current sync operation.
        reference = IR_SEQUENCE.next_by_code('sellerscommerce.sync.iteration') or _('New')
        message = f'A new SellersCommerce sync operation {reference} is planned'
        for catalog in catalogs:
            catalog.message_post(body=message)

        for catalog in catalogs:
            product_count = catalog.item_count

            upper_bound = product_count \
                if product_count % batch_size == 0 \
                else product_count + batch_size

            for start_index in range(0, upper_bound, batch_size):
                if start_index + batch_size > product_count:
                    end_index = product_count - 1
                else:
                    end_index = start_index + batch_size - 1

                unit = PRODUCT_SYNC_WORK_UNIT.search([
                    ('catalog_id', '=', catalog.id),
                    ('start_index', '<=', start_index),
                    ('end_index', '>=', end_index),
                    ('state', 'in', ('pending', 'waiting'))
                ])

                if unit:
                    log.info(f'Work unit id={unit.id} already exist and not done yet.')
                    continue

                unit = PRODUCT_SYNC_WORK_UNIT.create({
                    'catalog_id': catalog.id,
                    'start_index': start_index,
                    'end_index': end_index,
                    'state': 'waiting',
                    'active': True,
                    'reference': reference
                })

    @api.model
    def lunch_api_data_sync_planning(self,archive_discontinued_products=True):
        self.api_catalog_sync()
        self.create_product_sync_work_units(archive_discontinued_products)

    @api.model
    def api_batch_product_sync(self):
        self = self.sudo()
        PRODUCT_SYNC_WORK_UNIT = self.env[WORK_UNIT_MODEL]

        # Pick a unit of work (ordered by create data).
        work_unit = PRODUCT_SYNC_WORK_UNIT.next_work_unit()

        if not work_unit:
            log.info('No pending work unit is found.')
            return

        # Start work unit.
        work_unit.action_start()

        # Process the products in this unit of work.
        self.api_product_sync(work_unit)

        # End work unit.
        work_unit.action_end()

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

    def action_sync_next_products_bacth(self):
        """
        Force sync operation within a catalog.
        """
        self = self.sudo()
        PRODUCT_SYNC_WORK_UNIT = self.env[WORK_UNIT_MODEL]

        self.ensure_one()

        # Pick a unit of work (ordered by create data).
        work_unit = PRODUCT_SYNC_WORK_UNIT.next_work_unit(catalog_id=self.id)

        if not work_unit:
            raise ValidationError(_('No pending Sync job is found, please re-launch sync planning CRON'))
    
        # Start work unit.
        work_unit.action_start()

        # Process the products in this unit of work.
        self.api_product_sync(work_unit)

        # End work unit.
        work_unit.action_end()

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
