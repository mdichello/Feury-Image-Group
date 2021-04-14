# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Feury Pricelist",
    'version': '1.0',
    'depends': [
        'feury_artwork',
        'widget_badge',
    ],
    'author': 'Business Software Development Solutions',
    'license': 'AGPL-3',
    'mainainer': 'Business Software Development Solutions',
    'category': 'sales',
    'description': "Pricelist",
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/res_partner.xml',
        'views/customer_pricelist.xml',
        'views/menus.xml',
        'data/ir_sequence.xml',
    ],
}
