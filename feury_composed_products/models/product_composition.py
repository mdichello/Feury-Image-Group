# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ProductCompositionLine(models.Model):
    _name = 'composition.line'
    _description = 'Composition of a product template'
    _rec_name = 'product_id'

    product_tmpl_id = fields.Many2one(
        help='The current record will be a part of the components of this product',
        comodel_name='product.template',
        string='Product',
        ondelete='cascade',
        required=True,
        index=True
    )
    product_id = fields.Many2one(
        help='The component product',
        comodel_name='product.product',
        string='Product',
        ondelete='restrict',
        required=True,
        domain="[('is_composite_product','=', False)]",
        index=True
    )
    quantity = fields.Integer(
        help='The equivalent quantity for one unit of the composed product',
        string='Quantity',
        default=1,
        required=True
    )

    _sql_constraints = [
        ('quantity_positive', 'check (quantity > 0)', _('The quantity must be positive!'))
    ]

    # ----------------------------------------------------------------------------------------------------
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
    # 6- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
