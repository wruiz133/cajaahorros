# -*- encoding: utf-8 -*-
##############################################################################

{
    "name": "Loan Management EC",
    "depends": [
        "base",
        "account",
        "product",
        "hr"
    ],
    "author": "Cesar Rodriguez, David Jacobo Romero Calderon",
    "category": "Sale",
    "description": """Loan Management EC""",
    'data': [
        "wizard/wizard_generate_detail.xml",
        "views/loan_management_menu.xml",
        "views/loan_type_view.xml",
        "views/loan_plazo_view.xml",
        "views/loan_interes_view.xml",
        "views/loan_view .xml",
        "views/loan_cuota_view.xml",
        "views/loan_docs_view.xml",
        "views/contracto_sale_sequence.xml",
        "views/aportacion_view.xml",
        "views/aportaciones.xml",
        "views/cliente_view.xml",
        "wizard/wizard_status_cuotas_view.xml",
        "views/mora_view.xml",
        "views/generate_detail_batch.xml",
        
    ],
    #'update_xml' : [
     #       'security/groups.xml',
      #      'security/ir.model.access.csv'
    #],
    'demo': [],
    'installable': True,
}
