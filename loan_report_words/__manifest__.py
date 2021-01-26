# -*- encoding: utf-8 -*-
##############################################################################

{
    "name": "Loan reports words",
    "depends": [
        "report",
        "base",
        "loan_management-master",
        "loan_catalogues",
    ],
    "author": "Lead Solutions",
    "category": "Sale",
    "description": """Loan reports words """,
    'data': [
        "views/external_layout_header.xml",
        "views/cron_words.xml",
        "views/loan_words_form.xml",
	    "views/loan_voucher.xml",
        "views/loan_voucher_template.xml",
    ],
    # 'update_xml' : [
    #       'security/groups.xml',
    #      'security/ir.model.access.csv'
    # ],
    'demo': [],
    'installable': True,
}
