
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


# TODO make margin alterable (do not alter the one on the customer sheet)
class CustomerPricelist(models.Model):
    _name = 'customer.pricelist'
    _description = 'Customer Pricelist'
    _inherit = ['mail.thread']
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

    # ----------------------------------------------------------------------------------------------------
    # 2- Constraints methods (_check_***)
    # ----------------------------------------------------------------------------------------------------

    @api.constrains('line_ids')
    def _check_lines(self):
        for record in self:
            if not record.line_ids:
                raise ValidationError(_('You must have at least one operation.'))

    # ----------------------------------------------------------------------------------------------------
    # 3- Compute methods (namely _compute_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 4- Onchange methods (namely onchange_***)
    # ----------------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------------
    # 5- Actions methods (namely action_***)
    # ----------------------------------------------------------------------------------------------------

    def action_send(self):
        self.state = 'sent'

    def action_approve(self):
        self.state = 'approved'

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
