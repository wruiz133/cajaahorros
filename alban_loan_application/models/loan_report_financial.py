# -*- coding: utf-8 -*-

from datetime import datetime
import time
from odoo import api, models,fields
import dateutil.parser
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
#from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class ReportFinancialDaysLate(models.AbstractModel):
    _name = 'report.alban_loan_application.days_late_schedule'

    
    def _lines(self,data,id_idx,payment_id):
        full_account = []
        
        if data['partner_id'][0]!=None:
            
        #### Report no2

            if data['account_report_id']=='rptdetailschd':

                query = """
                        SELECT customer_acc_id || '-' || appln_no as id_loan
                        FROM public.loan_application
                        WHERE loan_application.id = """ + str(data['loan_no'][0]) 
                            
                self.env.cr.execute(query)
                #id_loan=self.env.cr.fetchone() (u'0000018-001',)
                query_results = self.env.cr.dictfetchall()
                if query_results[0].get('id_loan') != None:
                        id_loan=query_results[0].get('id_loan')
                else:
                        id_loan='Null'


                if id_idx == 1:
                    print "here1"
                    query = """
                        SELECT  transdate,'' as  installment,'' as days_late, schdid, schddate,   COALESCE(pmtid,0) as pmtid,     prindue,        
                                        intdue,     feesdue, transtypeid
                                        from loan_payments
                            where transtypeid in (4,5) and COALESCE(schdid,0) > 0  and loanid = '""" + str(id_loan) + """'
                            order by schddate asc,transtypeid,transdate asc,intdue desc,prindue desc
                            """

                    self.env.cr.execute(query)
                    res = self.env.cr.dictfetchall()
                    #contemp = self.env.cr.fetchone()
                    sum = 0.0
                    lang_code = self.env.context.get('lang') or 'en_US'
                    lang = self.env['res.lang']
                    lang_id = lang._lang_get(lang_code)
                    date_format = lang_id.date_format

                    memory_variable=0L
                    count=0L
                    total_prindue=0.0000
                    total_intdue=0.0000
                    total_feesdue=0.0000
                    
                    memory_date='1900-01-01'
                    

                    for r in res:
                        if r['transtypeid']==4:
                            memory_date=dateutil.parser.parse(r['transdate']).date()
                            total_prindue=0.0000
                            total_intdue=0.0000
                            total_feesdue=0.0000
                            if count>=1:
                                full_account.append(p)
                        
                        count =count + 1        
                        
                        total_prindue =total_prindue + r['prindue']
                        total_intdue = total_intdue + r['intdue']
                        total_feesdue = total_feesdue + r['feesdue']
                        

                        
                        
                        r['installment']=str(format(r['prindue']+r['intdue']+r['feesdue'],'.2f'))
                        r['prindue'] = str(format(r['prindue'],'.2f'))
                        r['intdue'] = str(format(r['intdue'],'.2f'))
                        r['feesdue'] = str(format(r['feesdue'],'.2f'))

                        if r['transtypeid']==5:
                            r['days_late']=str((dateutil.parser.parse(r['transdate']).date()  - memory_date).days)

                        if r['transdate'] != None:        
                            r['transdate'] = datetime.strptime(r['transdate'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                        else:
                            r['transdate'] = 'error'

                        if r['schddate'] != None:        
                            r['schddate'] = datetime.strptime(r['schddate'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                        else:
                            r['schddate'] = 'error'

                        p = {
                                'transdate': 'Still Due',
                                'transtypeid': 55,
                                'days_late':'-',
                                'installment':str(format(total_prindue+total_intdue+total_feesdue,'.2f')),
                                'prindue': str(format(total_prindue,'.2f')),
                                'intdue': str(format(total_intdue,'.2f')),
                                'feesdue': str(format(total_feesdue,'.2f')),
                                
                            }
                          
                        full_account.append(r)

               
                

        return full_account

    

    @api.model
    def render_html(self, docids, data):
        print data
        print data['form']['account_report_id'],data['form']['partner_id'][0]
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'lines':self._lines,
        }
        if data['form']['account_report_id']=='rptdetailalloc':
            report_name=self.env['report'].render('alban_loan_application.report_invoice_my', docargs)
        else:
            report_name=self.env['report'].render('alban_loan_application.days_late_schedule', docargs)
        
        return report_name




class ReportFinancial(models.AbstractModel):
    _name = 'report.alban_loan_application.report_invoice_my'

    
    def _lines(self,data,id_idx,payment_id):
        full_account = []
        
        if data['partner_id'][0]!=None:
            if data['account_report_id']=='rptdetailalloc':

                query = """
                        SELECT customer_acc_id || '-' || appln_no as id_loan
                        FROM public.loan_application
                        WHERE loan_application.id = """ + str(data['loan_no'][0]) 
                            
                self.env.cr.execute(query)
                #id_loan=self.env.cr.fetchone() (u'0000018-001',)
                query_results = self.env.cr.dictfetchall()
                if query_results[0].get('id_loan') != None:
                        id_loan=query_results[0].get('id_loan')
                else:
                        id_loan='Null'


                if id_idx == 1:
                    print "here1"
                    query = """
                        SELECT distinct
                                account_move_line.amount_residual as amount_residual, 
                                account_move_line.date as payment_date, 
                                loan_payments.pmtid as payment_id,
                                tbltransactions.name as transtype
                        FROM 
                                public.loan_payments, 
                                public.account_move_line,
                                public.tbltransactions
                        WHERE                       
                                tbltransactions.id=loan_payments.transtypeid and
                                loan_payments.pmtid = account_move_line.payment_id and 
                                account_move_line.amount_residual <> 0 and
                                loan_payments.loanid = '""" + str(id_loan) + """' order by account_move_line.date """

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
                        r['payment_id'] = str(r['payment_id'])
                        r['transtype']="  " +str(r['transtype'])+ "  "

                        if r['payment_date'] != None:        
                            r['payment_date'] = datetime.strptime(r['payment_date'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                        else:
                            r['payment_date'] = 'error'
                        
                        full_account.append(r)

                if id_idx == 2:
                    print "here2"

                    query = """
                        SELECT 
                                loan_payments.schddate as schddate, 
                                loan_payments.prinnotdue as prinnotdue, 
                                loan_payments.prindue + loan_payments.prinnotdue as prindue, 
                                loan_payments.intdue as intdue, 
                                loan_payments.penpaid as penpaid, 
                                loan_payments.ovdintacc as ovdintacc, 
                                loan_payments.feesdue as feesdue
                                
                        FROM 
                                public.loan_payments, 
                                public.account_move_line,
                                public.tbltransactions
                        WHERE                       
                                tbltransactions.id=loan_payments.transtypeid and
                                loan_payments.pmtid = account_move_line.payment_id and 
                                loan_payments.pmtid = """+ str(payment_id) + """ and
                                account_move_line.amount_residual <> 0 and
                                loan_payments.loanid = '""" + str(id_loan) + """' order by loan_payments.schddate """

                    self.env.cr.execute(query)
                    res = self.env.cr.dictfetchall()
                    #contemp = self.env.cr.fetchone()
                    sum = 0.0
                    lang_code = self.env.context.get('lang') or 'en_US'
                    lang = self.env['res.lang']
                    lang_id = lang._lang_get(lang_code)
                    date_format = lang_id.date_format
                    
                    for r in res:
                        
                        r['prinnotdue'] = str(format(r['prinnotdue'],'.2f'))
                        r['prindue'] = str(format(r['prindue'],'.2f'))
                        r['intdue'] = str(format(r['intdue'],'.2f'))
                        r['penpaid'] = str(format(r['penpaid'],'.2f'))
                        r['ovdintacc'] = str(format(r['ovdintacc'],'.2f'))
                        r['feesdue'] = str(format(r['feesdue'],'.2f'))
                        

                        if r['schddate'] != None:
                            r['schddate'] = datetime.strptime(r['schddate'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                        else:
                            r['schddate'] = '--'
                        
                        
                        full_account.append(r)       
                

        return full_account

    

    @api.model
    def render_html(self, docids, data):
        print data
        print data['form']['account_report_id'],data['form']['partner_id'][0]
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'lines':self._lines,
        }

        if data['form']['account_report_id']=='rptdetailalloc':
            report_name=self.env['report'].render('alban_loan_application.report_invoice_my', docargs)
        else:
            report_name=self.env['report'].render('alban_loan_application.days_late_schedule', docargs)
        
        return report_name


class LoanReport(models.TransientModel):
    _name = "loan.report"
    _description = "Loan Report"

    partner_id = fields.Many2one('res.partner', string='Partner',domain="[('is_bank_customer','=','-1')]")
    loan_no  =fields.Many2one('loan.application',string='Loan No.' , domain="[('partner_id', '=', partner_id)]")
    account_report_id = fields.Selection([
                            ('rptdetailalloc', 'Detailed Pmt Allocation'),('rptdetailschd','Detailed Schd Allocation')
                    ],string='Report Type',required=True)
    
    
    def print_report(self, data):
        #data['form'].update(self.read(['partner_id'])[0])
        data['form']= self.read(['partner_id','account_report_id','loan_no'])[0]
        

        #print data
        #print data['form']['partner_id'][0],data['form']['account_report_id']

        if self.account_report_id=='rptdetailalloc':
            report_data=self.env['report'].get_action(self, 'alban_loan_application.report_invoice_my', data=data)
        
        if self.account_report_id=='rptdetailschd':
            print "here here"
            report_data=self.env['report'].get_action(self, 'alban_loan_application.days_late_schedule', data=data)
        
        return report_data        
   