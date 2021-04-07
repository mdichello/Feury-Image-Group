# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Email Grouping by tags",
    'version': '1.0',
    'depends': ['sale'],
    'author': 'Odoo Inc',
    'license': 'OEEL-1',
    'mainainer': 'Odoo Inc',
    'category': 'Category',
    'description': """
Email Grouping by tags
======================
- Partner grouping based on tags when sending records(sale order / invoice) via email.
    """,
    # data files always loaded at installation
    'data': [
        'views/partner_views.xml',
        'data/res_partner_category_data.xml',
    ],
}