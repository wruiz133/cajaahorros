# -*- coding: utf-8 -*-

from odoo import models, api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for rec in self:
            line = rec.line_ids.filtered(lambda l:l.salary_rule_id.is_loan_payment)
            if line:
                install_ids = self.get_loan_installment(rec.employee_id.id, rec.date_from, rec.date_to)
                if install_ids:
                    install_lines = self.env['loan.installment.details'].browse(install_ids)
                    install_lines.pay_installment()
        return res

    @api.model
    def get_loan_installment(self, emp_id, date_from, date_to=None):
            self._cr.execute("SELECT o.id, o.install_no from loan_installment_details as o where \
                                o.employee_id=%s \
                                AND to_char(o.date_from, 'YYYY-MM-DD') >= %s AND to_char(o.date_from, 'YYYY-MM-DD') <= %s ",
                                (emp_id, date_from, date_to))
            res = self._cr.dictfetchall()
            install_ids = []
            if res:
                install_ids = [r['id']for r in res]
            return install_ids
