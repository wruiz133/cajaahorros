# -*- coding: utf-8 -*-
{
    'name': "Loan Aportes",

    #'summary': """
    #    Short (1 phrase/line) summary of the module's purpose, used as
     #   subtitle on modules listing or apps.openerp.com""",

    'description': """
        1-- Crea las lineas de aportes ordinarios y valida la transacción
        2.- Permite carga de aportes especiales vesion inical de aportes
    """,

    'author': "LeadSolutions",
    'website': "http://www.leadsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    #'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'loan_management-master',
                'loan_catalogues', ],

    # always loaded
    'data': [

        # 'security/ir.model.access.csv',
        'wizard/cartera_test_wizard_view.xml',
        'wizard/wizar_aportes.xml',
        'views/aportaciones_especial_view.xml',
        'views/test_cartera_aporte_views.xml',
        #'wizard/wizard_aportaciones_esp.xml',
        #'views/aportaciones_cash_view.xml',
        #'wizard/cartera_test_wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
