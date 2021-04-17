
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from collections import defaultdict


# TODO add a thumbnail (search if we can have a selection from available ones)
# TODO add constraint to not allow lines with zero cost.
# TODO add button called "refresh", actions: update the cost of each group.
# TODO restrict extra types on the line to (heat_seal, sew_patch, embroider).
# TODO check duplicated values in lines!
class CustomerPricelist(models.Model):
    _name = 'customer.pricelist'
    _description = 'Customer Pricelist'
    _inherit = ['portal.mixin', 'mail.thread']
    _check_company_auto = True
    _rec_name = 'reference'

    _sql_constraints = [
        ('customer_pricelist_reference_uniq', 'unique(reference)', 'A Pricelist reference should be unique.')
    ]

    reference = fields.Char(
        string="Refrence", 
        readonly=True, 
        required=True, 
        copy=False, 
        default=_('New')
    )

    company_id = fields.Many2one(
        comodel_name='res.company', 
        required=False,
        default=lambda self: self.env.company
    )

    currency_id = fields.Many2one(
        string='Currency',
        comodel_name='res.currency', 
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )

    partner_id = fields.Many2one(
        string='Customer',
        comodel_name='res.partner',
        ondelete='cascade', 
        index=True,
        domain=['&', ('parent_id', '=', False), ('is_customer', '=', True)], 
        required=False
    )

    date = fields.Date(
        string='Date created',
        required=True,
        readonly=True,
        default=lambda l: fields.Date.today()
    )

    approved_date = fields.Date(
        string='Date Approved',
        readonly=True
    )

    start_date = fields.Date(
        string='Start date',
        required=True,
        default=lambda l: fields.Date.today()
    )
    
    end_date = fields.Date(
        string='End date',
        default=lambda l: fields.Date.today() + relativedelta(years=1)
    )

    margin = fields.Float(
        string='Margin',
        related='partner_id.margin'
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'), 
            ('sent', 'Sent'),
            ('signed', 'Signed'),
            ('approved', 'Approved'),
            ('cancel', 'Cancel'),
        ], 
        string='Status', 
        required=True, 
        readonly=True, 
        copy=False,
        default='draft'
    )

    line_ids = fields.One2many(
        string="Lines",
        comodel_name="customer.pricelist.line",
        inverse_name="pricelist_id"
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    signature = fields.Image(
        string='Signature',
        help='Signature received through the portal.',
        copy=False,
        attachment=True,
        max_width=1024,
        max_height=1024
    )

    signed_by = fields.Char(
        string='Signed By',
        help='Name of the person that signed.',
        copy=False
    )

    signed_on = fields.Datetime(
        string='Signed On',
        help='Date of the signature.',
        copy=False
    )

    # ----------------------------------------------------------------------------------------------------
    # 1- ORM Methods (create, write, unlink)
    # ----------------------------------------------------------------------------------------------------

    @api.model
    def create(self, vals):
        IR_SEQUENCE = self.env['ir.sequence']
        if vals.get('reference', 'New') == 'New':
            vals['reference'] = IR_SEQUENCE.next_by_code('customer.pricelist') or _('New')
        result = super(CustomerPricelist, self).create(vals)
        return result

    def unlink(self):
        for pricelist in self:
            if pricelist.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete a sent pricelist or a confirmed one. You must first cancel it.'))
        return super(CustomerPricelist, self).unlink()

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    @api.constrains('line_ids')
    def _check_lines(self):
        for record in self:
            # We should have at least one line
            if not record.line_ids:
                raise ValidationError(_('You must have at least one item in the pricelist.'))

            # Check if we have a zero cost line.
            if record.state in ('sent', 'signed', 'approved'):
                costs = record.line_ids.mapped('cost')
                if any(cost <= 0 for cost in costs):
                    raise ValidationError(_('You can not have a zero cost line in the state.'))

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    @api.onchange('line_ids')
    def onchange_line_ids(self):
        """
        Ungroup lines according to the cost (standard price).
        """

        PRICELIST_LINE = self.env['customer.pricelist.line']
        PRODUCT_TEMPLATE = self.env['product.template']

        for record in self:
            non_atomic_lines = record.line_ids.filtered(
                lambda l: not l.is_atomic
            )

            for line in non_atomic_lines:
                if not line.style_id:
                    continue

                groups = defaultdict(lambda : PRODUCT_TEMPLATE)
                products = PRODUCT_TEMPLATE.search([
                    ('style_id', '=', line.style_id.id)
                ])

                for product in products:
                    groups[product.standard_price] += product

                if not groups:
                    continue

                cost, products = groups.popitem()
                colors = products.mapped('color_id')
                sizes = products.mapped('size_id')
                line.write({
                    'color_ids': [(6, 0, colors.ids)],
                    'size_ids': [(6, 0, sizes.ids)],
                    'cost': cost,
                    'sale_price': cost * (1 + self.margin/100),
                    'is_atomic': True
                })

                for cost, products in groups.items():
                    colors = products.mapped('color_id')
                    sizes = products.mapped('size_id')

                    PRICELIST_LINE.new({
                        'pricelist_id': self.id,
                        'style_id': line.style_id.id,
                        'color_ids': [(6, 0, colors.ids)],
                        'size_ids': [(6, 0, sizes.ids)],
                        'cost': cost,
                        'sale_price': cost * (1 + line.margin/100),
                        'is_atomic': True
                    })

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.mail_template_sale_confirmation', raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.email_template_edi_sale', raise_if_not_found=False)

        return template_id

    def action_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_template(template.lang, 'sale.order', self.ids[0])
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_approve(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to approve a pricelist in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for pricelist in self.filtered(lambda pricelist: pricelist.partner_id not in pricelist.message_partner_ids):
            pricelist.message_subscribe([pricelist.partner_id.id])

        self.write({
            'state': 'approved',
            'approved_date': fields.Datetime.now()
        })
        return True

    def action_cancel(self):
        self.state = 'cancel'

    def action_sign(self):
        self.state = 'signed'

    def action_draft(self):
        self.state = 'draft'

    # ----------------------------------------------------------------------------------------------------
    # 6- CRONs methods
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 7- Technical methods (name must reflect the use)
    # ----------------------------------------------------------------------------------------------------

    def _get_forbidden_state_confirm(self):
        return {'approved', 'cancel'}

    def preview_pricelist(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    def _compute_access_url(self):
        super(CustomerPricelist, self)._compute_access_url()
        for pricelist in self:
            pricelist.access_url = '/my/pricelist/%s' % (pricelist.id)
