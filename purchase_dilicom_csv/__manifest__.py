# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Dilicom CSV',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Cash CSV Report',
    'summary': "Generate CSV files to order on the Dilicom website",
    'description': """
    
Purchase Dilicom CSV
====================

Dilicom is a French book distributor (https://dilicom-prod.centprod.com/)

This module adds a report *Dilicom CSV Order* on purchase orders. It
generates a CSV file that can be uploaded on the Dilicom website to
generate an order.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['loan_management-master', 'report_qweb_txt'],
    'data': [
        
	    'views/loan_pagos_compras_template.xml',
        'views/loan_pagos_ventas_template.xml',	
	    'report/report_cash_issfa.xml',
        'report/report_cash_ruminahui.xml',
        'report/report_cash_pichincha.xml',
        'report/report_cash_produbanco.xml',       
        #'report/dilicom_purchase_order_csv_1.xml'
        'report.xml',
        ],
    'installable': True,
}
