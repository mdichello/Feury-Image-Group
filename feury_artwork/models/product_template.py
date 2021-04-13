from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    style_code = fields.Char(
        string='Style Code',
        required=True,
        unique=True
    )

    color_id  = fields.Many2one(
        string="Color",
        comodel_name="color",
        required=True
    )

    size_id  = fields.Many2one(
        string="Size",
        comodel_name="product.size",
        required=True
    )
