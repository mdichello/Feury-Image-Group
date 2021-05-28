# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


SUPPORTED_MODELS = (
    'sale.order', 
    'account.move', 
    'stock.picking',
    'customer.pricelist'
)


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        PARTNER_CATEGORY = self.env['res.partner.category']
        RES_PARTNER = self.env['res.partner']

        values = super(MailComposeMessage, self).generate_email_for_composer(template_id, res_ids, fields=None)
        add_partners = self.env.context.get('change_partners', False)
        active_model = self.env.context.get('default_model', False)
        res_id = self.env.context['default_res_id']
        is_batch = self.env.context.get('is_batch', False)

        if active_model and active_model in SUPPORTED_MODELS and add_partners:
            for res_id in res_ids:
                MODEL = self.env[active_model]
                record = MODEL.browse(res_id)
                partner_categories = PARTNER_CATEGORY.search(
                    [
                        ('trigger_model_name', '=', active_model)
                    ]
                )
                if partner_categories and is_batch:
                    partner_ids = record.partners_send_list()

                    children = partner_ids.mapped('child_ids').filtered(
                        lambda c: any(
                            category in partner_categories 
                            for category in c.category_id
                        )
                    )
                    
                    send_to_list = partner_ids + children
                    values[res_id]['partner_ids'] = send_to_list or values[res_id]['partner_ids']
                        
    
                elif partner_categories and record.partner_id.child_ids:
                    partner_ids = record.partner_id.child_ids.filtered(
                        lambda c: any(categ in partner_categories for categ in c.category_id)
                    )
                    values[res_id]['partner_ids'] = partner_ids or values[res_id]['partner_ids']
        return values
