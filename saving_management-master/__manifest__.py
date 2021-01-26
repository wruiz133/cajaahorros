# -*- encoding: utf-8 -*-
##############################################################################

{
    "name": "Saving Management EC",
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
        "views/saving_management_menu.xml",
        "views/saving_type_view.xml",
        "views/saving_plazo_view.xml",
        "views/saving_interes_view.xml",
        "views/saving_cuota_view.xml",
        "wizard/wizard_status_cuotas_view.xml",
        "views/saving_view.xml",
        "views/saving_docs_view.xml",
        "views/contracto_sale_sequence.xml",
        "views/aportacion_view.xml",
        "views/aportaciones.xml",
        "views/cliente_view.xml",
        "views/mora_view.xml",
        #"views/generate_detail_batch.xml",
        
    ],
    #'update_xml' : [
     #       'security/groups.xml',
      #      'security/ir.model.access.csv'
    #],
    'demo': [],
    'installable': True,
}
