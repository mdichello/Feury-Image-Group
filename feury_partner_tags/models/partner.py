# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class RasPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    trigger_model = fields.Many2one(comodel_name='ir.model', copy=False)
    trigger_model_name = fields.Char(related='trigger_model.model')
