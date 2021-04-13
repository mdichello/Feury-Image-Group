# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Customer artwork",
    'version': '1.0',
    'depends': [
        'sale_management', 
        'is_customer_is_supplier',
        'feury_tools'
    ],
    'author': 'Business Software Development Solutions',
    'license': 'AGPL-3',
    'mainainer': 'Business Software Development Solutions',
    'category': 'Customization',
    'description': "Customer artwork",
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/material_color.xml',
        'views/material_type.xml',
        'views/material_size.xml',
        'views/color.xml',
        'views/product_size.xml',
        'views/artwork.xml',
        'views/res_partner.xml',
        'views/menu.xml',
        'data/material_color.xml',
        'data/material_type.xml',
        'data/material_size.xml',
    ],
}
