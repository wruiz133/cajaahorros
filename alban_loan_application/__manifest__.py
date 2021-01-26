# -*- coding: utf-8 -*-
{
    'name': "BankPro-Ent",

    'summary': """
        Fully Integrated Microbanking/Banking/Factoring/Leasing/MFI/Non-Bank Solution based on oDoo technology""",

    'description': """
        This is a fully intergrated GUI-based Software Solution based oDoo, from iCom, that caters to a wide spectrum of banking/micro-banking operations, including diverse lending methodologies & institutional models, interest calculation & repayment schedules amongst others.
        Integrating Loans, Savings, and Financial Accounting and MIS applications. The BankPro today, caters to the micro-banking activities of various types / sizes of MFIs, rural banks and Non-bank financial companies. It blends financial accounting with member accounting, loan
        management and socio-economic information.
        - Accounting
        - Loan Origination
        - Leasing
        - Factoring
        - Savings
        - CRM
        - Collections
        - Risk
        - Legal handle
        - Branchless
        - Quality Reports
        - Business Intelligence
    """,

    'author': "ICOM Shpk, Tirane, Albania +355692087330, info@icom-al.com",
    'website': "http://www.icom-al.com",
    'category': 'Microbanking/Banking/Factoring/Leasing/MFI/Non-Bank',
    'version': '0.1',
    'depends': ['base','account', 'sale', 'purchase',],
    #'depends': ['base','account','accounting',],
    'images': ['static/description/icon.png'],

    'data': [
        'security/alban_security.xml',
        'security/ir.model.access.csv',
        'views/prelim_app_view.xml',
        'views/res_partner_view.xml',
        'views/prospect_menu_main.xml',
        'views/base_number_view.xml',
        'views/loan_application_main.xml',
        'views/collateral_main.xml',
        'views/details_form_view.xml',
        'views/application_no_sequence.xml',
        'reports/reports_main.xml',
        'reports/reports_view.xml',
        'reports/report_invoice_my.xml',
        #'views/account_view_inherited.xml',
        #'views/report_generalledger.xml',
        #'report/inherited_layouts.xml',

    #   from aban_three
        'views/admin_branch.xml',
        'views/import_village_view.xml',
    #   from alban_four
        'views/loan_directory_data.xml',
        'views/collateral_type.xml',
        'views/loan_config_settings_views.xml',
    #    'views/generate_report_wiz_view.xml'

        

    ],
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
