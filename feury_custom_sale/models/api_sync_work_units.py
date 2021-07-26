# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SellersCommerceProductSyncWorkUnit(models.Model):
    _name = 'sellerscommerce.product.sync.work.unit'
    _description = 'Product Sync unit of work'
    _order = 'create_date'

    catalog_id = fields.Many2one(
        string='Catalog',
        comodel_name='sellerscommerce.product.catalog',
        required=True
    )

    start_index = fields.Integer(
        string='Start Index',
        required=True
    )

    end_index = fields.Integer(
        string='Start Index',
        required=True
    )

    start_time = fields.Datetime(
        string='Start time',
        required=False
    )

    end_time = fields.Datetime(
        string='End time',
        required=False
    )

    state = fields.Selection(
        [
            ('waiting', 'Waiting'), 
            ('pending', 'Pending'),
            ('done', 'Done'),
        ], 
        string='Status', 
        required=True,
        default='waiting'
    )

    active = fields.Boolean(
        string='Active',
        default=True
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

    @api.model
    def next_work_unit(self):
        domain = [
            ('state', '=', 'waiting')
        ]
        work_unit = self.search(domain, limit=1)
        return work_unit
