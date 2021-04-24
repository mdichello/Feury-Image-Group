from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'


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

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.pricelist_id = self.partner_id.with_context(force_company=self.company_id.id).property_product_pricelist.id
        if self.partner_id.user_id:
            self.user_id = self.partner_id.user_id

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------

    def _get_default_pricelist(self):
        """
        Return a system pricelist if found otherwise return system default one.
        """
        PRODUCT_PRICELIST = self.env['product.pricelist']
        customer_pricelist = PRODUCT_PRICELIST.search([
            ('partner_id', '=', self.partner_id),
            ('company_id', '=', self.env.company.id),
        ], limit=1)
        return (customer_pricelist and customer_pricelist.id) or PRODUCT_PRICELIST.search([
            ('currency_id', '=', self.env.company.currency_id.id
        )], limit=1).id
