from odoo import api, fields, models, tools, _


class PricelistCustomerImageWizard(models.TransientModel):
    _name = 'customer.pricelist.wizard'
    _description = "customer Pricelist Wizard"

    def _get_default_pricelist_line_id(self):
        PRICELIST_LINE = self.env['customer.pricelist.line']
        active_id = self.env.context.get('active_id')
        return PRICELIST_LINE.browse(active_id)

    pricelist_line_id = fields.Many2one(
        comodel_name='customer.pricelist.line',
        string='Customer Pricelist line',
        default=_get_default_pricelist_line_id
    )

    image_ids = fields.One2many(
        string='Images',
        comodel_name='pricelist.product.image.wizard',
        inverse_name="pricelist_wizard_id"
    )

    uploaded_image = fields.Image(
        'Upload image',
        required=False
    )

    @api.model
    def default_get(self, fields):
        PRODUCT_IMAGE = self.env['pricelist.product.image.wizard']

        vals = super(PricelistCustomerImageWizard, self).default_get(fields)

        pricelist_line_id = self._get_default_pricelist_line_id()
        lines_values = []
        for index, product in enumerate(pricelist_line_id.product_ids):
            if not product.image_1920:
                continue
    
            values = {
                'product_id': product.id,
                'sequence': index+1,
            }
            lines_values.append(values)
        

        if lines_values:
            lines = PRODUCT_IMAGE.create(lines_values)
        
        else:
            lines = PRODUCT_IMAGE

        vals['image_ids'] = [(6, 0, lines.ids)]

        return vals

    def save_selection(self):
        selected_product = self.image_ids.filtered(lambda l: l.is_selected)

        if self.uploaded_image:
            image = self.uploaded_image

        elif selected_product:
            image = selected_product[0].product_id.image_1920

        if image:
            self.pricelist_line_id.thumbnail = image


class PricelistProductImage(models.TransientModel):
    _name = 'pricelist.product.image.wizard'
    _description = "Pricelist Product Image"
    _inherit = ['image.mixin']
    _order = 'sequence, id'

    pricelist_wizard_id = fields.Many2one(
        'customer.pricelist.wizard'
    )

    sequence = fields.Integer(
        default=1, 
        index=True
    )

    product_id = fields.Many2one(
        string='Product',
        comodel_name='product.template', 
        index=True, 
        ondelete='cascade'
    )

    color = fields.Integer(
        string='Kanban Color Index',
        default=11
    )

    is_selected = fields.Boolean(
        string='Is selected',
        default=False,
        required=True
    )

    def select(self):
        self.update({
            'is_selected': True,
            'color': 0
        })

        other_lines = self.search([
            ('pricelist_wizard_id', '=', self.pricelist_wizard_id.id),
            ('id', '!=', self.id)
        ])
        other_lines.write({
            'is_selected': False,
            'color': 11
        })

        wizard_view_id = self.env.ref('feury_pricelist.customer_pricelist_product_image_wizard').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Picture',
            'res_model': 'customer.pricelist.wizard',
            'res_id': self.pricelist_wizard_id.id,
            'view_mode': 'form',
            'target': 'new',
            'view_id': wizard_view_id,
        }

    def unselect(self):
        self.update({
            'is_selected': False,
            'color': 11
        })
        wizard_view_id = self.env.ref('feury_pricelist.customer_pricelist_product_image_wizard').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Picture',
            'res_model': 'customer.pricelist.wizard',
            'res_id': self.pricelist_wizard_id.id,
            'view_mode': 'form',
            'target': 'new',
            'view_id': wizard_view_id,
        }
