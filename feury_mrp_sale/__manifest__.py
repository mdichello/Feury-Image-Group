# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Link between SO and MO",
    'version': '1.0',
    'depends': ['sale_management', 'mrp', 'account_followup'],
    'author': 'Odoo Inc',
    'license': 'OEEL-1',
    'mainainer': 'Odoo Inc',
    'category': 'Customization',
    'description': """
Link between SO and MO
======================
- Multiple developments for Sales and Mrp.
1. Link between SOL and MO(Copy SOL description to MO).
2. MO(s) button on sale order.
3. Custom notes on the sale orderline to flow on MO.
4. ut a credit hold on Partner if total due is more then credit limit,
   block confirmation of order except for administrator.
    """,
    # data files always loaded at installation
    'data': [
        'views/sale_order_views.xml',
        'views/mrp_production_views.xml',
        'wizard/wizard_sale_order_views.xml',
    ],
}