# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class ProductSize(models.Model):
    _name = 'product.size'
    _description = 'Product size'
    _rec_name = 'code'

    _sql_constraints = [
        ('product_size_code_uniq', 'unique(code)', 'A product size code should be unique.')
    ]

    name = fields.Char(
        string='Name',
        required=True,
        unique=True
    )

    code = fields.Char(
        string='Code',
        required=True,
        unique=True,
        index=True,
    )

    code_components = fields.Char(
        string='Code component(s)',
        required=False,
        default='Size'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    @api.model
    @tools.ormcache('name')
    def _search_or_create_by_name(self, name, compenents='Size'):
        if not name:
            return False

        domain = [('name', 'ilike', name)]

        if compenents:
            domain.append(('code_components', 'ilike', compenents))
    
        size = self.search(domain, limit=1)

        if not size:
            size = self.create({
                'name': name,
                'code': name,
                'code_components': compenents,
            })

        return size.id

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
