from odoo import api, fields, models, _


class Res_Partner(models.Model):
	_inherit = 'res.partner'

	is_customer = fields.Boolean(
		string="Is a Customer",
		default=True
	)

	is_vendor = fields.Boolean(
		string="Is a Vendor",
		default=False
	)
