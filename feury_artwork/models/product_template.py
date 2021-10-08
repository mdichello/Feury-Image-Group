import logging

from odoo import api, fields, models, _


log = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    style_id = fields.Many2one(
        string="Style Code",
        comodel_name="product.style",
        required=False
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

    vendor_code = fields.Char(
        string='Vendor Code',
        required=False,
        readonly=False,
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
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

        PRODUCT_TEMPLATE = self.env['product.template']
        PRODUCT_STYLE = self.env['product.style']
        PRODUCT_SIZE = self.env['product.size']
        COLOR = self.env['color']


        if complete_migration:
            # Clean existins records.
            sql = """
                delete from customer_pricelist;
                update product_template set style_id = null;
                update product_template set color_id = null;
                update product_template set size_id = null;
                delete from product_style;
                delete from product_size;
            """

            self.env.cr.execute(sql)
            self.env.cr.commit()

        products = PRODUCT_TEMPLATE.search([])

        for record in products:
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
                    ('code', 'ilike', record.x_studio_size_code),
                ], limit=1)

                if not size:
                    size = PRODUCT_SIZE.create({
                        'code': record.x_studio_size_code,
                        'name': record.x_studio_size_code,
                    })

                values['size_id'] = size.id

            vendor_code = record.x_studio_vendor_code
            style_code = record.x_studio_product_style_code
            if (complete_migration or not record.style_id) and style_code:
                try:
                    domain = [
                        ('code', 'ilike', style_code)
                    ]

                    if vendor_code:
                        domain.append(('vendor_code', 'ilike', vendor_code))

                    style = PRODUCT_STYLE.search(domain, limit=1)

                    if not style:
                        style = PRODUCT_STYLE.search([
                            ('code', 'ilike', style_code)
                        ], limit=1)

                    if not style:
                        style = PRODUCT_STYLE.create({
                            'code': style_code,
                            'vendor_code': vendor_code
                        })

                    values['style_id'] = style.id
                except:
                    log.error(f'Found duplicate key in style module {vendor_code}:{style_code}')
                    continue

            if values:
                record.write(values)
                self.env.cr.commit()
