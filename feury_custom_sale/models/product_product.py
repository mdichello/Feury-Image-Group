from odoo import api, fields, models,_


class ProductProduct(models.Model):
    _inherit = "product.product"

    embellishment_id = fields.Many2one(
        string="Embellishment", 
        comodel_name="embellishment", 
        compute='_compute_embellishment',
        inverse='_inverse_embellishment',
        readonly=True
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

    def _inverse_embellishment(self):
        for product in self:
            product.product_tmpl_id.embellishment_id = product.embellishment_id

    def _compute_embellishment(self):
        for product in self:
            product.embellishment_id = product.product_tmpl_id.embellishment_id

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

    # ----------------------------------------------------------------------------------------------------
    # 8- Overridden methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------