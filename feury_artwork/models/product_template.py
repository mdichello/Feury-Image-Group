from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    style_id = fields.Many2one(
        string="Style Code",
        comodel_name="product.style",
        required=True
    )

    color_id = fields.Many2one(
        string="Color",
        comodel_name="color",
        required=False
    )

    size_id = fields.Many2one(
        string="Size",
        comodel_name="product.size",
        required=False
    )

    # ----------------------------------------------------------------------------------------------------
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

    def migrate_studio_fields(self, complete_migration=False):
        """
        Temporary method
        """

        PRODUCT_STYLE = self.env['product.style']
        PRODUCT_SIZE = self.env['product.size']
        COLOR = self.env['color']

        # TODO optimize performance, fetch all colors and sizes once.
        for record in self:
            values = {
            }

            if (complete_migration or not record.color_id) and record.x_studio_color_code:
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
            
            if (complete_migration or not record.size_id) and record.x_studio_size_code:
                size = PRODUCT_SIZE.search([
                    ('code', 'ilike', record.x_studio_size_code)
                ], limit=1)

                if not size:
                    size = PRODUCT_SIZE.create({
                        'code': record.x_studio_size_code,
                    })

                values['size_id'] = size.id

            if (complete_migration or not record.style_id) and record.x_studio_product_style_code:
                style = PRODUCT_STYLE.search([
                    ('code', 'ilike', record.x_studio_product_style_code)
                ], limit=1)

                if not style:
                    style = PRODUCT_STYLE.create({
                        'code': record.x_studio_product_style_code,
                    })

                values['style_id'] = style.id

            if values:
                record.write(values)
                self.env.cr.commit()