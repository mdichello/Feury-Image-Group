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
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/sale_order.xml',
        'views/embellishment.xml',
        'views/clothes_location.xml',
        'views/clothes_type.xml',
        'views/res_partner.xml',
        'views/menu.xml',
        'data/clothes_location.xml',
        'data/clothes_type.xml',
    ],
}
