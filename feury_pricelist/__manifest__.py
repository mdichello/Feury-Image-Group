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
        'report/pricelist_report.xml',
        'report/pricelist_report_templates.xml',
        'data/mail_data.xml',
        'data/pricelist_data.xml',
        'views/res_partner.xml',
        'views/customer_pricelist.xml',
        'views/pricelist_portal_templates.xml',
        'views/product_pricelist.xml',
        'views/res_company.xml',
        'views/menus.xml',
        'views/res_config_settings_views.xml',
        'wizard/customer_pricelist_image.xml',
        'data/ir_sequence.xml',
    ],
}
