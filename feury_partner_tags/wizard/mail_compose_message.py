# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def generate_email_for_composer(self, template_id, res_ids, fields=None):
        values = super(MailComposeMessage, self).generate_email_for_composer(template_id, res_ids, fields=None)
        if self.env.context.get('default_model') and \
            self.env.context['default_model'] in ['sale.order', 'account.move'] and \
            self.env.context.get('change_partners'):
            for res_id in res_ids:
                record = self.env[self.env.context['default_model']].browse(self.env.context['default_res_id'])
                partner_categories = self.env['res.partner.category'].search(
                    [('trigger_model_name', '=', self.env.context['default_model'])])
                if partner_categories and record.partner_id.child_ids:
                    partner_ids = record.partner_id.child_ids.filtered(
                        lambda c: any([categ in partner_categories for categ in c.category_id]))
                    values[res_id]['partner_ids'] = partner_ids or values[res_id]['partner_ids']
        return values
