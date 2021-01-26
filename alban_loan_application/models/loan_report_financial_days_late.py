# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import api, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class ReportFinancial(models.AbstractModel):
    _name = 'report.alban_loan_application.days_late_schedule'

    
    def _lines(self,data):
        full_account = []

        if data['form']['partner_id'][0]!=None:
            if data['form']['account_report_id']=='rptdetailalloc':

                query = """
                    SELECT 
                            account_move_line.amount_residual as amount_residual, 
                            account_move_line.date as payment_date, 
                            loan_payments.schddate as schddate, 
                            loan_payments.prinnotdue as prinnotdue, 
                            loan_payments.prindue + loan_payments.prinnotdue as prindue, 
                            loan_payments.intdue as intdue, 
                            loan_payments.penpaid as penpaid, 
                            loan_payments.ovdintacc as ovdintacc, 
                            loan_payments.feesdue as feesdue,
                            tbltransactions.name as transtype
                    FROM 
                            public.loan_payments, 
                            public.account_move_line,
                            public.tbltransactions
                    WHERE                       
                            tbltransactions.id=loan_payments.transtypeid and
                            loan_payments.pmtid = account_move_line.payment_id and 
                            account_move_line.amount_residual<>0

                    order by account_move_line.date
                            """
                self.env.cr.execute(query)
                res = self.env.cr.dictfetchall()
                #contemp = self.env.cr.fetchone()
                sum = 0.0
                lang_code = self.env.context.get('lang') or 'en_US'
                lang = self.env['res.lang']
                lang_id = lang._lang_get(lang_code)
                date_format = lang_id.date_format
                
                for r in res:
                    r['amount_residual'] = str(format(r['amount_residual'],'.2f'))
                    r['prinnotdue'] = str(format(r['prinnotdue'],'.2f'))
                    r['prindue'] = str(format(r['prindue'],'.2f'))
                    r['intdue'] = str(format(r['intdue'],'.2f'))
                    r['penpaid'] = str(format(r['penpaid'],'.2f'))
                    r['ovdintacc'] = str(format(r['ovdintacc'],'.2f'))
                    r['feesdue'] = str(format(r['feesdue'],'.2f'))
                    r['transtype']=str(r['transtype'])

                    if r['schddate'] != None:
                        r['schddate'] = datetime.strptime(r['schddate'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                    else:
                        r['schddate'] = '--'
                    
                    if r['payment_date'] != None:        
                        r['payment_date'] = datetime.strptime(r['payment_date'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                    else:
                        r['payment_date'] = 'error'
                    
                    full_account.append(r)

        return full_account

    

    @api.model
    def render_html(self, docids, data=None):
        print data
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        accounts_res = self._lines(data)
        
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'lines': accounts_res,
        }
        return self.env['report'].render('alban_loan_application.days_late_schedule', docargs)
   