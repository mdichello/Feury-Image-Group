# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _


log  = logging.getLogger(__name__)

class SellersCommerceProductSyncWorkUnit(models.Model):
    _name = 'sellerscommerce.product.sync.work.unit'
    _description = 'Product Sync unit of work'
    _order = 'id'

    catalog_id = fields.Many2one(
        string='Catalog',
        comodel_name='sellerscommerce.product.catalog',
        required=True
    )

    reference = fields.Char(
        string="Reference", 
        readonly=False, 
        required=True,
        copy=False, 
        default=_('New')
    )

    vendor_code = fields.Char(
        string="Vendor Code", 
        compute='_compute_vendor_code',
        store=True
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

    @api.model
    def create(self, values):
        IR_SEQUENCE = self.env['ir.sequence']
        if values.get('reference', 'New') == 'New':
            values['reference'] = IR_SEQUENCE.next_by_code('sellerscommerce.sync.iteration') or _('New')
        result = super(SellersCommerceProductSyncWorkUnit, self).create(values)
        return result

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    @api.depends('catalog_id')
    def _compute_vendor_code(self):
        for record in self:
            record.vendor_code = record.catalog_id \
                and record.catalog_id.partner_id \
                and record.catalog_id.partner_id.x_studio_vendor_code \
                or ''

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    def action_start(self):
        self.ensure_one()
        self.write({
            'start_time': fields.Datetime.now(),
            'state': 'pending'
        })
        log.info(f'API sync work unit {self.id} started')

    def action_end(self):
        self.ensure_one()
        self.write({
            'end_time': fields.Datetime.now(),
            'state': 'done'
        })
        log.info(f'API sync work unit {self.id} completed')

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
