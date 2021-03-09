from odoo import api, fields, models, _


class Res_Partner(models.Model):
	_inherit = 'res.partner'

	artwork_ids = fields.One2many(
        string="Artworks",
        comodel_name="artwork",
        inverse_name="partner_id"
    )
