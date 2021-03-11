from odoo import api, fields, models,_


class ProductTemplate(models.Model):
    _inherit = "product.product"

    is_composite_product = fields.Boolean(
        comodel_name='product.template',
        related='product_tmpl_id.is_composite_product',
        readonly=True
    )
