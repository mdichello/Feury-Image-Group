#  -*- coding: utf-8 -*-

import base64
import binascii

from werkzeug.exceptions import NotFound
from odoo import http, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.mail import _message_post_helper


class PricelistPortal(CustomerPortal):

    @http.route('/my/pricelist/<int:pricelist_id>/<string:uuid>/signature', type='json', auth="public", website=True)
    def signature(self, subscription_id, uuid='', name=None, signature=None):
        SUBSCRIPTION = request.env['sale.subscription']

        if not signature:
            return {'error': _('Signature is missing.')}

        if uuid:
            subscription = SUBSCRIPTION.sudo().browse(subscription_id)
            if uuid != subscription.uuid:
                raise NotFound()
        else:
            subscription = SUBSCRIPTION.browse(subscription_id)

        try:
            subscription.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error):
            return {'error': _('Invalid signature data.')}

        if subscription:
            pdf = request.env.ref(
                'neosoft_customization.action_report_salesubscription').sudo(
            ).render_qweb_pdf([subscription_id])[0]

            _message_post_helper(
                'sale.subscription', subscription_id,
                _('Subscription signed by %s') % name,
                attachments=[('%s.pdf' % subscription.code, pdf)],
            )
            return {
                'force_refresh': True,
                'redirect_url': '/my/subscription/%s/%s' % (subscription.id, subscription.uuid)
            }

        return {
            'force_refresh': True,
            'redirect_url': '/my/subscription'
        }
