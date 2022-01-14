# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import os
import csv

from odoo import api, fields, models
from odoo.modules import get_resource_path, get_module_path


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_parent_company_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Parent Company', 
        index=True, 
        domain="[('is_company', '=', True)]"
    )

    x_studio_customervendor = fields.Selection(
        selection=[
            ('Vendor', 'Vendor'),
            ('Customer', 'Customer'),
            ('Contacts', 'Contacts'),
        ],
        string='is customer / vendor',
        required=True,
        default='Contact'
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

    @api.model
    def _migrate_partner_relationships(self):
        RES_COUNTRY_STATE = self.env['res.country.state']
        RES_PARTNER = self.env['res.partner']

        module_name = 'feury_custom_sale'
        csv_path = os.path.join(
            get_module_path(module_name),
            'static', 'src', 'csv', 'customer_relationships.csv'
        )

        usa_country = self.env.ref('base.us')

        with open(csv_path, 'r') as f:
            csv_reader = csv.DictReader(f)

            for row in csv_reader:
                parent_name = row['Belongs To']
                x_studio_fax = row['Fax']
                child_name = row['Last']
                street2 = row['Address2']
                street = row['Address']
                phone = row['Phone']
                email = row['Email']
                state_name = row['State']
                city = row['City']

                # No parent and neither a child is found.
                if not parent_name and not child_name:
                    continue
                
                # State processing.
                state = RES_COUNTRY_STATE
                if state_name:
                    state = RES_COUNTRY_STATE.search([
                        '|',
                        ('name', '=ilike', state_name),
                        ('code', '=ilike', state_name)
                    ], limit=1)

                    if not state:
                        state = RES_COUNTRY_STATE.create({
                            'country_id': usa_country.id,
                            'name': state_name,
                            'code': state_name.upper()[:3]
                        })

                # Case 1: we have only child name.
                if child_name and not parent_name:
                    child = RES_PARTNER.search([('name', '=ilike', child_name)])

                    if not child:
                        child = RES_PARTNER.create({
                            'name': child_name,
                            'company_type': 'company', 
                            'x_studio_is_a_customer': True,
                            'is_company': True,
                            'country_id': usa_country.id,
                            'x_studio_fax': x_studio_fax,
                            'state_id': state and state.id or False,
                            'street2': street2,
                            'street': street,
                            'phone': phone,
                            'email': email,
                            'city': city,
                        })
                    self.env.cr.commit()
                    continue

                # Case 2: child name and parent one are equal (same partner).
                if parent_name.lower() == child_name.lower():
                    parent = RES_PARTNER.search([('name', '=ilike', parent_name)])

                    if not parent:
                        parent = RES_PARTNER.create({
                            'name': parent_name,
                            'company_type': 'company', 
                            'x_studio_is_a_customer': True,
                            'is_company': True,
                            'country_id': usa_country.id,
                            'x_studio_fax': x_studio_fax,
                            'state_id': state and state.id or False,
                            'street2': street2,
                            'street': street,
                            'phone': phone,
                            'email': email,
                            'city': city,
                        })
                        self.env.cr.commit()

                    continue
                
                # Case 3: both exist and they are different.
                child = RES_PARTNER.search([('name', '=ilike', child_name)], limit=1)
                parent = RES_PARTNER.search([('name', '=ilike', parent_name)], limit=1)

                if not parent:
                    parent = RES_PARTNER.create({
                        'name': parent_name,
                        'company_type': 'company', 
                        'x_studio_is_a_customer': True,
                        'is_company': True,
                        'country_id': usa_country.id
                    })

                if not child:
                    child = RES_PARTNER.create({
                        'name': child_name,
                        'company_type': 'company', 
                        'x_studio_is_a_customer': True,
                        'is_company': True,
                        'country_id': usa_country.id,
                        'x_studio_fax': x_studio_fax,
                        'state_id': state and state.id or False,
                        'street2': street2,
                        'street': street,
                        'phone': phone,
                        'email': email,
                        'city': city,
                    })
                
                child.partner_parent_company_id = parent.id
                self.env.cr.commit()

    @api.model
    def _fix_partner_name(self, old='Yale New Hampshire', new='Yale New Haven'):
        partners = self.search([])

        for partner in partners:
            if old in partner.name:
                partner.name = partner.name.replace(old, new)
