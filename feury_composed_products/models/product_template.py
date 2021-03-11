from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    deployment = fields.Selection(
        selection=[
            ('auto', 'Automatic'),
            ('delayed', 'Delayed'),
        ],
        string='Deployement',
        required=True,
        default='auto'
    )

    is_composite_product = fields.Boolean(
        string='Is composite',
        default=False
    )

    composite_line_ids = fields.One2many(
        help='Composite lines',
        comodel_name='composition.line',
        inverse_name='product_tmpl_id',
        string="Product's composition"
    )

    def check_self_composite_reference(self):
        self.ensure_one()
        for line in self.composite_line_ids:
            if self.id == line.product_id.id:
                raise ValidationError("A product can't be composed of itself")

    def write(self, values):
        res = super(ProductTemplate, self).write(values)

        for record in self:
            record.check_self_composite_reference()

        return res
