from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    margin = fields.Float(
        string="Margin",
        default=100
    )

    # TODO add trigger to change value, for example once we disable the pricelist, then it should be unlocked.
    is_locked_pricelist = fields.Boolean(
        string='Locked pricelist',
        company_dependent=True,
        default=False
    )

    @property
    def has_custom_pricelist(self):
        PRODUCT_PRICELIST = self.env['product.pricelist']
        self.ensure_one()
        return self.property_product_pricelist.partner_id == self

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
