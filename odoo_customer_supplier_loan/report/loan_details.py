# -*- coding: utf-8 -*-


import time
from openerp.osv import osv
from openerp.report import report_sxw

class loan_details(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(loan_details, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_lines':self._get_lines
        })

    def _get_lines(self, lines):
        res = []
        count = 1
        for line in lines:
            access = 0.0
            temp = {}
#             print line.install_no
            if count == 1 or line.install_no == 1:
                open_amt = line.loan_id.principal_amount
            temp['no'] = line.install_no
            temp['emi'] = line.total
            temp['principal'] = line.principal_amt
            temp['opening_bal'] = open_amt
            temp['interest'] = line.interest_amt
            access = round(line.total - (line.principal_amt + line.interest_amt), 2)
            temp['closing_bal'] = round(open_amt - line.principal_amt - access, 2)
            temp['state'] = line.state
            temp['date_from'] = line.date_from
            temp['date_to'] = line.date_to
            if temp['closing_bal'] < 0:temp['closing_bal'] = 0.0
            open_amt = temp['closing_bal']
            res.append(temp)
            count = count + 1 
#         print ">>>>>>>>>>>>>>>>>>>>>>>>>res>>>>>",res
        return res
    
class report_test(osv.AbstractModel):
    _name = "report.odoo_customer_supplier_loan.partner_loan_report_qweb"
    _inherit = "report.abstract_report"
    _template = "odoo_customer_supplier_loan.partner_loan_report_qweb"
    _wrapped_report_class = loan_details

#report_sxw.report_sxw('report.loan.details', 'employee.loan.details', 'addons/ng_loan_payroll/report/loan_details.rml', parser=loan_details)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

