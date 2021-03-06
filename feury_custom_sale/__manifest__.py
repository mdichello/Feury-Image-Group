# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Feury Custom Sale",
    'version': '1.0',
    'depends': [
        'feury_artwork',
    ],
    'author': 'Business Software Development Solutions',
    'license': 'AGPL-3',
    'mainainer': 'Business Software Development Solutions',
    'category': 'Customization',
    'description': "Sale customization",
    'data': [
        # 'security/groups.xml',
        'security/ir.model.access.csv',
        # 'security/ir_rule.xml',
        'views/sale_order.xml',
        'views/embellishment.xml',
        'views/clothes_location.xml',
        'views/clothes_type.xml',
        'views/menu.xml',
        'data/clothes_location.xml',
        'data/clothes_type.xml',
    ],
}
