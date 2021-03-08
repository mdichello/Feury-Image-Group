# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Customer artwork",
    'version': '1.0',
    'depends': ['sale_management'],
    'author': 'Business Software Development Solutions',
    'license': 'AGPL-3',
    'mainainer': 'Business Software Development Solutions',
    'category': 'Customization',
    'description': "Customer artwork",
    'data': [
        'security/ir.model.access.csv',
        'views/artwork.xml',
        'views/menu.xml',
    ],
}
