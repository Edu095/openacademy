# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """
        Openacademy module. Test module to try things.
        Ñeee ee.""",

    'description': """
        Long description of module's purpose.Hercle, bubo grandis!.A falsis, imber magnum lactea.
    """,

    'author': "Eduard Ojer",
    'website': "http://www.bitmodules.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Pruebas',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'website', 'mail', 'website_sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        # 'views/session_workflow.xml',
        'reports.xml',
        'views/session_board.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}