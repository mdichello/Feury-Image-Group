# -*- coding: utf-8 -*-

import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource


class CustomerPricelistLine(models.Model):
    _name = 'customer.pricelist.line'
    _description = 'Customer Pricelist Line'
    _order = "sequence, id"

    sequence = fields.Integer(
        string='Sequence',
        default=1,
        index=True,
    )

    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="customer.pricelist"
    )

    embellishment_id = fields.One2many(
        string='Embellishment',
        comodel_name='embellishment',
        inverse_name="customer_pricelist_line_id"
    )

    clothing_type_id = fields.Many2one(
        string='Clothing type',
        comodel_name='clothes.type',
        required=False
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='pricelist_id.currency_id'
    )

    style_id = fields.Many2one(
        string="Style Code",
        comodel_name="product.style",
        ondelete='cascade',
        index=True,
        required=True
    )

    color_ids = fields.Many2many(
        comodel_name='color', 
        relation='color_customer_pricelist_line_rel', 
        column1='customer_pricelist_line_id', 
        column2='color_id', 
        string="Colors"
    )

    size_ids = fields.Many2many(
        comodel_name='product.size', 
        relation='size_customer_pricelist_line_rel', 
        column1='customer_pricelist_line_id', 
        column2='size_id', 
        string="Sizes"
    )

    product_ids = fields.Many2many(
        comodel_name='product.template', 
        relation='product_template_customer_pricelist_line_rel', 
        column1='customer_pricelist_line_id', 
        column2='product_template_id', 
        string="Products"
    )

    thumbnail = fields.Image(
        string="Thumbnail",
        readonly=True,
    )

    margin = fields.Float(
        string='Margin',
    )

    is_personalizable = fields.Boolean(
        string="Personalizable",
        default=False
    )

    cost = fields.Monetary(
        string='Cost', 
        readonly=True,
        default=0
    )

    is_atomic = fields.Boolean(
        string='Is atomic',
        default=False,
        help='Is atomic, meaning degrouping is needed'
    )

    sale_price = fields.Monetary(
        string='Sale Price', 
        default=0
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    @api.model
    def _default_image(self):
        image_path = get_module_resource(
            'feury_pricelist',
            'static/src/img',
            'image_not_available.png'
        )
        return base64.b64encode(open(image_path, 'rb').read())

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    # @api.depends('product_ids')
    # def _compute_thumbnail(self):
    #     for record in self:
    #         products_with_images = record.product_ids.filtered(
    #             lambda p: p.image_1920
    #         )
    #         record.thumbnail = products_with_images[0].image_1920 \
    #             if products_with_images \
    #             else record._default_image()

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    @api.onchange('margin')
    def onchange_margin(self):
        if not self.cost:
            return
        
        self.sale_price = self.cost * (1 + self.margin/100)

    @api.onchange('sale_price')
    def onchange_sale_price(self):
        if not self.cost:
            return

        if self.sale_price < self.cost:
            raise UserError(_(
                "Sale price can not be less than the product's cost"
            ))

        self.margin = (self.sale_price - self.cost) * 100 / self.cost

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    def action_open_embellishment_wizard(self):
        wizard_view_id = self.env.ref('feury_custom_sale.embellishment_form').id

        context = dict(self._context)
        context.update({
            "default_customer_pricelist_line_id": self.id,
            "partner_id": self.pricelist_id.partner_id.id,
            "location_ids": self.clothing_type_id.location_ids.ids,
        })

        result = {
            'type': 'ir.actions.act_window',
            'name': 'Embellishment',
            'res_model': 'embellishment',
            'view_mode': 'form',
            'target': 'new',
            'view_id': wizard_view_id,
            'context': context,
        }

        if self.embellishment_id:
            result.update({
                'res_id': self.embellishment_id[0].id
            })

        return result

    def action_open_image_wizard(self):
        wizard_view_id = self.env.ref('feury_pricelist.customer_pricelist_product_image_wizard').id

        context = dict(self._context)
        context.update({
            "default_customer_pricelist_line_id": self.id,
        })

        result = {
            'type': 'ir.actions.act_window',
            'name': 'Select Picture',
            'res_model': 'customer.pricelist.wizard',
            'view_mode': 'form',
            'target': 'new',
            'view_id': wizard_view_id,
            'context': context,
        }

        if self.embellishment_id:
            result.update({
                'res_id': self.embellishment_id[0].id
            })

        return result

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
