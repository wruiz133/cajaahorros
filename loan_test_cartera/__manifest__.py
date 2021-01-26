# -*- coding: utf-8 -*-

{
    'name': "Loan Cartera Aporte",
 
    'depends': [
        "base",
        "loan_management-master",
	"loan_aportes",
	"loan_catalogues",
        "loan_aportes",
        ],

    "author": "Lead Solutions",
    "category": "Cash",
    "description": """Loan Cash """,

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/cartera_test_wizard_view.xml',
        'views/test_cartera_aporte_views.xml',
            ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,

}
