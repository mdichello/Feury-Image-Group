# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CustomerPricelistLine(models.Model):
    _name = 'customer.pricelist.line'
    _description = 'Customer Pricelist Line'

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

    margin = fields.Float(
        string='Margin',
        default=50
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

    sale_price = fields.Monetary(
        string='Sale Price', 
        default=0
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    @api.model
    def default_get(self, fields):
        values = super(CustomerPricelistLine, self).default_get(fields)

        # TODO temporary code.
        values['cost'] = 12
        return values

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

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

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------
