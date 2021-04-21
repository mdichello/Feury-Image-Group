# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii
from datetime import date

from odoo import fields, http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.osv import expression


class CustomerPortal(CustomerPortal):
    # TODO format code.

    def _prepare_home_portal_values(self):
        values = super(CustomerPortal, self)._prepare_home_portal_values()
        partner = request.env.user.partner_id

        CustomerPricelist = request.env['customer.pricelist']
        pricelist_count = CustomerPricelist.search_count([
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sent', 'signed', 'approved', 'cancel'])
        ])

        values.update({
            'pricelist_count': pricelist_count,
        })
        return values

    @http.route(['/my/pricelists', '/my/pricelist/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_pricelists(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        CUSTOMER_PRICELIST = request.env['customer.pricelist']
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sent', 'signed', 'approved', 'cancel'])
        ]

        searchbar_sortings = {
            'date': {'label': _('Approved Date'), 'order': 'approved_date desc'},
            'reference': {'label': _('Reference'), 'order': 'reference'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }
        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('customer.pricelist', domain) if values.get('my_details') else []
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        order_count = CUSTOMER_PRICELIST.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/pricelist",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=order_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        pricelists = CUSTOMER_PRICELIST.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_pricelist_history'] = pricelists.ids[:100]

        values.update({
            'date': date_begin,
            'pricelists': pricelists.sudo(),
            'page_name': 'pricelist',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/pricelists',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("feury_pricelist.portal_my_pricelists", values)

    @http.route(['/my/pricelists/<int:pricelist_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, pricelist_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            pricelist_sudo = self._document_check_access(
                'customer.pricelist', 
                pricelist_id, 
                access_token=access_token
            )
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=pricelist_sudo, 
                report_type=report_type, 
                report_ref='feury_pricelist.action_report_pricelist', 
                download=download
            )

        # use sudo to allow accessing/viewing pricelists for public user
        # only if he knows the private token
        # Log only once a day
        if pricelist_sudo:
            now = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_pricelist_%s' % pricelist_sudo.id)
            if isinstance(session_obj_date, date):
                session_obj_date = session_obj_date.isoformat()
            if session_obj_date != now and request.env.user.share and access_token:
                request.session['view_pricelist_%s' % pricelist_sudo.id] = now
                body = _('Pricelist viewed by customer %s') % pricelist_sudo.partner_id.name
                _message_post_helper(
                    "customer.pricelist",
                    pricelist_sudo.id,
                    body,
                    token=pricelist_sudo.access_token,
                    message_type="notification",
                    subtype="mail.mt_note",
                    partner_ids=pricelist_sudo.user_id.sudo().partner_id.ids,
                )

        values = {
            'pricelist': pricelist_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'partner_id': pricelist_sudo.partner_id.id,
            'report_type': 'html',
            'action': pricelist_sudo._get_portal_return_action(),
        }
        if pricelist_sudo.company_id:
            values['res_company'] = pricelist_sudo.company_id

        history = request.session.get('my_pricelists_history', [])
        values.update(get_records_pager(history, pricelist_sudo))

        return request.render('feury_pricelist.pricelist_portal_template', values)

    @http.route(['/my/pricelists/<int:pricelist_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, pricelist_id, access_token=None, name=None, signature=None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            pricelist_sudo = self._document_check_access('customer.pricelist', pricelist_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid pricelist.')}

        if not pricelist_sudo.has_to_be_signed():
            return {'error': _('The pricelist is not in a state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            pricelist_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error):
            return {'error': _('Invalid signature data.')}

        pricelist_sudo.action_approve()
        pricelist_sudo._send_pricelist_approval_mail()

        pdf = request.env.ref('feury_pricelist.action_report_pricelist').sudo().render_qweb_pdf([pricelist_sudo.id])[0]

        _message_post_helper(
            'customer.pricelist', pricelist_sudo.id, _('Pricelist signed by %s') % (name,),
            attachments=[('%s.pdf' % pricelist_sudo.reference, pdf)],
            **({'token': access_token} if access_token else {}))

        query_string = '&message=sign_ok'
        return {
            'force_refresh': True,
            'redirect_url': pricelist_sudo.get_portal_url(query_string=query_string),
        }

    @http.route(['/my/pricelists/<int:pricelist_id>/decline'], type='http', auth="public", methods=['POST'], website=True)
    def decline(self, pricelist_id, access_token=None, **post):
        try:
            pricelist_sudo = self._document_check_access('customer.pricelist', pricelist_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        message = post.get('decline_message')

        query_string = False
        if pricelist_sudo.has_to_be_signed() and message:
            pricelist_sudo.action_cancel()
            _message_post_helper('customer.pricelist', pricelist_id, message, **{'token': access_token} if access_token else {})
        else:
            query_string = "&message=cant_reject"

        return request.redirect(pricelist_sudo.get_portal_url(query_string=query_string))
