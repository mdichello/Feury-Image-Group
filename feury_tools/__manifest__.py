# -*- coding: utf-8 -*-
{
    'name': 'Feury tools',
    'version': '0.1',
    'category': 'tools',
    'summary': 'Generic function helpers',
    'author': 'Business Software Development Solutions',
    'description': """
This module contains all the helpers for Feury Group Image custom built ERP.
    """,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'web'
    ],
    'application': False,
    'auto_install': True,
    # always loaded
    'data': [
        'views/assets.xml',
    ]
}
