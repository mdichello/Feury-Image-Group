# -*- coding: utf-8 -*-
{
    'name': "Feury Composed products",

    'summary': """
        Composed products""",

    'description': """
        Composed products lets you define pack products that will be replaced by its content in sale order
    """,

    'author': 'Business Software Development Solutions',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customization',
    'version': '0.1',
    # always loaded
    'data': [
        'views/product_template.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
    "application": True,
    "depends": [
        "sale",
    ],
}
