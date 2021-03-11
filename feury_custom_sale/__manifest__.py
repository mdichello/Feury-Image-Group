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
        'views/material_color.xml',
        'views/material_type.xml',
        'views/material_size.xml',
        'views/sale_order.xml',
        'views/embellishment.xml',
        'views/menu.xml',
        'data/material_color.xml',
        'data/material_type.xml',
        'data/material_size.xml',
    ],
}
