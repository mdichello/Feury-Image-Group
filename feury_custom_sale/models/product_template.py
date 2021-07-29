# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    category_ids = fields.Many2many(
        comodel_name='product.category', 
        relation='product_category_product_template_rel', 
        column1='product_category_id', 
        column2='product_template_id', 
        string="Categories"
    )

    image_ids = fields.One2many(
        comodel_name='product.image', 
        inverse_name='product_tmpl_id', 
        string="Product Image", 
        copy=True
    )

    skus = fields.One2many(
        comodel_name='sellerscommerce.product.virtual.inventory', 
        inverse_name='product_id', 
        string="SKUs", 
        copy=False
    )

    brand_id = fields.Many2one(
        string='Brand',
        comodel_name='product.brand',
    )

    catalog_id = fields.Many2one(
        string='Catalog',
        comodel_name='sellerscommerce.product.catalog',
    )

    external_id = fields.Integer(
        string='External ID',
        required=True,
        index=True
    )

    msrp = fields.Monetary(
        string='MSRP',
        default=0
    )

    description_html = fields.Html(
        string="Description HTML"
    )

    map = fields.Monetary(
        string='MAP',
        default=0
    )

    height = fields.Float(
        string='Height (inch)',
        default=0.0
    )

    width = fields.Float(
        string='Width (inch)',
        default=0.0
    )

    length = fields.Float(
        string='Length (inch)',
        default=0.0
    )

    size_chart = fields.Image(
        string='Size chart'
    )

    hash = fields.Char(
        string='Hash',
        required=True
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
