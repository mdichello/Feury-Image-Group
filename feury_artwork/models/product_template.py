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

    def migrate_studio_fields(self):
        """
        Temporary method
        """

        PRODUCT_SIZE = self.env['product.size']
        COLOR = self.env['color']

        # TODO optimize performance, fetch all colors and sizes once.
        for record in self:
            values = {
                'style_code': record.x_studio_product_style_code
            }

            if not record.color_id and record.x_studio_color_code:
                color = COLOR.search([
                    ('code', 'ilike', record.x_studio_color_code)
                ], limit=1)

                if not color:
                    color = COLOR.create({
                        'code': record.x_studio_color_code,
                        'name': record.x_studio_color_code,
                        'hex_code': '#FFFFF'
                    })

                values['color_id'] = color.id
            
            if not record.size_id and record.x_studio_size_code:
                size = PRODUCT_SIZE.search([
                    ('code', 'ilike', record.x_studio_size_code)
                ], limit=1)

                if not size:
                    size = PRODUCT_SIZE.create({
                        'code': record.x_studio_size_code,
                    })

                values['size_id'] = size.id

            record.write(values)
            self.env.cr.commit()
