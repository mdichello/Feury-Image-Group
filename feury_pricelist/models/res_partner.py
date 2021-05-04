from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    margin = fields.Float(
        string="Margin",
        default=100
    )

    is_locked_pricelist = fields.Boolean(
        string='Locked pricelist',
        default=False
    )

    # def _get_partner_pricelist_multi(self, partner_ids, company_id=None):
    #     results = super(ResPartner, self)._get_partner_pricelist_multi(
    #         self, 
    #         partner_ids, 
    #         company_id=company_id
    #     )
    #     return results

    # property_product_pricelist = fields.Many2one(
    #     string='Pricelist',
    #     comodel_name='product.pricelist',
    #     compute='_compute_product_pricelist',
    #     inverse='_inverse_product_pricelist',
    #     company_dependent=False,
    #     help='This pricelist will be used, instead of the default one, for sales to the current partner',
    # )

    # @api.depends('country_id')
    # @api.depends_context('force_company')
    # def _compute_product_pricelist(self):
    #     PRODUCT_PRICELIST = self.env['product.pricelist']
    #     company = self.env.context.get('force_company', False)
    #     res = PRODUCT_PRICELIST._get_partner_pricelist_multi(
    #         self.ids, 
    #         company_id=company
    #     )
    #     for p in self:

    #         p.property_product_pricelist = res.get(p.id)

    # def _inverse_product_pricelist(self):
    #     for partner in self:
    #         if partner.is_locked_pricelist:
    #             continue
    #         super(ResPartner, partner)._inverse_product_pricelist()

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
