# -*- encoding: utf-8 -*-
##############################################################################

{
    "name": "Loan Catalogues",
    "depends": [
        "base",
        "account",
        "product",
        "hr",
        "loan_management-master",
    ],
    "author": "Lead Solutions",
    "category": "Sale",
    "description": """Loan Catalogues """,
    'data': [
        "views/loan_reliquidaciones.xml",
        "views/cuota_payment.xml",
        "views/loan_report.xml",
        "views/loan_report_template.xml",
        "views/portfolio.xml",
        "views/catalogues.xml",
        "views/loan_aportaciones.xml",
        "views/cliente_view.xml",
        "data/loan_catalogues_data.xml",
    ],
    # 'update_xml' : [
    #       'security/groups.xml',
    #      'security/ir.model.access.csv'
    # ],
    'demo': [],
    'installable': True,
}
