import xlwt
import base64
import StringIO as str_io
from datetime import datetime
from odoo import models, fields,_,api
import dateutil.parser
import time
from cStringIO import StringIO
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
# import csv
import unicodecsv as csv

class finacial_report_wizard(models.TransientModel):

    _name = 'financial.report.wizard'
    Headers = ["Scheduled Installment Payment", "Days Late", "Total", "Principal", "Interest", "Fees"]#for scheduled installments
    Headers2 = ["Transaction Date","Type","Amount Installment Date", "Principal",
                "Interest","Penalties","Ovd Interest", "Fees"]#allocation of loan transaction

    @api.depends('customer_no')
    @api.onchange('customer_no')
    def _onchange_cust_no(self):
        appl_details_ids = self.env['applicant.details'].search([])
        loan_ids = []
        if self.customer_no:
            for appl_det_id in appl_details_ids:
                if self.customer_no == appl_det_id.customer_no1:
                    loan_ids.append(appl_det_id.applicant_id.id)

        return {'domain': {'loan_no': [('id', 'in', loan_ids)]}}

    partner_id = fields.Many2one('res.partner', string='Partner')
    customer_no = fields.Char(related='partner_id.account_id', string='Customer Number')
    loan_no = fields.Many2one('loan.application', string='Loan No.',)
    account_report_id = fields.Selection([('detail_pay_alloc', 'Detailed Payment Allocation'),
                                          ('detail_schd_alloc', 'Detailed Schedule Allocation')], string='Report Type')

    @api.multi
    def generate_fin_report_csv(self):
        # csvfile = StringIO.StringIO()
        csvfile = str_io.StringIO()
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')
        borders = xlwt.Borders()
        borders.right = xlwt.Borders.MEDIUM
        borders.left = xlwt.Borders.MEDIUM
        borders.top = xlwt.Borders.MEDIUM
        borders.bottom = xlwt.Borders.MEDIUM
        top_table = xlwt.easyxf('borders : top MEDIUM, bottom_color black; ')
        right_table = xlwt.easyxf('borders : right MEDIUM, bottom_color black; ')
        border_style = xlwt.XFStyle()  # Create Style
        border_style.borders = borders
        font = xlwt.Font()
        font.bold = True
        header1 = xlwt.easyxf('font: bold 1, height 230')
        style = xlwt.easyxf('align: wrap yes')
        worksheet.col(0).width = 5500
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 6000
        worksheet.col(4).width = 5000
        worksheet.row(0).height = 400
        worksheet.row(1).height = 500


        current_date = str(datetime.now().date())
        w = csv.writer(csvfile, delimiter='\t',quoting=csv.QUOTE_ALL)
        w.writerow(['Date',current_date])

        w.writerows(['','',''])
        w.writerow(["Schedule Client"])
        w.writerow([])
        w.writerow(["Client",self.partner_id.name,'','Date From','','','Target Moves'])
        w.writerow(["Loan Number",self.loan_no.appln_no,'','Date To','','','All Entries'])
        w.writerow(["",'','','','','','All Posted Entries'])
        w.writerow([])
        if self.account_report_id == 'detail_schd_alloc':
            # for header_row in self.Headers:
            #     print '======================header_row============',header_row
            #     worksheet.write(11, header_row, self.Headers[header_row])
            w.writerow(self.Headers)
            rows1 = self._lines()
            list = []
            for row_no in rows1:
                if row_no['transtypeid']==4:
                    list.append(row_no['transdate'])
                elif row_no['transtypeid']==55:
                    list.append(row_no['transdate'])
                list.append(row_no['days_late'])
                list.append(row_no['installment'])
                list.append(row_no['prindue'])
                list.append(row_no['intdue'])
                list.append(row_no['feesdue'])
                w.writerow(list)

                w.writerow([])
                list=[]

        else:
            w.writerow(self.Headers2)
            # for header_row in self.Headers2:
            #     worksheet.write(11, header_row, self.Headers2[header_row])
            rows2 =  self._lines_payment(1,0)

            list = []
            for row_no in rows2:
                list2 = []
                list.append(row_no['payment_date'])
                list.append(row_no['transtype'])
                list.append(row_no['amount_residual'])
                rows12 = self._lines_payment(2,row_no['payment_id'])
                w.writerow(list)

                for row_no2 in rows12:
                    list2.append('')
                    list2.append('')
                    list2.append(row_no2['schddate'])
                    list2.append(row_no2['prindue'])
                    list2.append(row_no2['intdue'])
                    list2.append(row_no2['penpaid'])
                    list2.append(row_no2['ovdintacc'])
                    list2.append(row_no2['feesdue'])
                    w.writerow(list2)
                    w.writerow([])
                    list2 = []
                w.writerow([])
                list = []


        csv_value = csvfile.getvalue()
        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        csvfile.close()
        # filename = str(datetime.date.today()).replace('-', '') + 'report.xls'
        filename = 'financial' + 'report.xls'
        picklist = self.env['generate.report'].create({'file': base64.encodestring(csv_value), 'filename': filename, })
        # picklist = self.env['generate.report'].create({'file': base64.encodestring(data), 'filename': filename, })
        action = {'name': 'Generated Picklist File', 'type': 'ir.actions.act_url',
                  'url': "web/content/?model=generate.report&id=" + str(
                      picklist.id) + "&filename_field=filename&field=file&download=true&filename=" + filename,
                  'target': 'self', }
        return action

    def _lines(self):
        full_account = []
        if self.partner_id != None:
            if self.account_report_id == 'detail_schd_alloc' and self.loan_no:
                query = """
                        SELECT customer_acc_id || '-' || appln_no as id_loan
                        FROM public.loan_application
                        WHERE loan_application.id = """ + str(self.loan_no[0].id)
                self.env.cr.execute(query)
                query_results = self.env.cr.dictfetchall()

                if query_results[0].get('id_loan') != None:
                    id_loan = query_results[0].get('id_loan')
                else:
                    id_loan = 'Null'

                query = """
                    SELECT  transdate,'' as  installment,'' as days_late, schdid, schddate,   COALESCE(pmtid,0) as pmtid,     prindue,        
                                    intdue,feesdue, transtypeid from loan_payments
                        where transtypeid in (4,5) and COALESCE(schdid,0) > 0  and loanid = '""" + str(
                    id_loan) + """'order by schddate asc,transtypeid,transdate asc,intdue desc,prindue desc
                        """
                self.env.cr.execute(query)
                res = self.env.cr.dictfetchall()
                sum = 0.0
                lang_code = self.env.context.get('lang') or 'en_US'
                lang = self.env['res.lang']
                lang_id = lang._lang_get(lang_code)
                date_format = lang_id.date_format

                memory_variable = 0L
                count = 0L
                total_prindue = 0.0000
                total_intdue = 0.0000
                total_feesdue = 0.0000

                memory_date = '1900-01-01'

                for r in res:
                    if r['transtypeid'] == 4:
                        memory_date = dateutil.parser.parse(r['transdate']).date()
                        total_prindue = 0.0000
                        total_intdue = 0.0000
                        total_feesdue = 0.0000
                        if count >= 1:
                            full_account.append(p)

                    count = count + 1

                    total_prindue = total_prindue + r['prindue']
                    total_intdue = total_intdue + r['intdue']
                    total_feesdue = total_feesdue + r['feesdue']

                    r['installment'] = str(format(r['prindue'] + r['intdue'] + r['feesdue'], '.2f'))
                    r['prindue'] = str(format(r['prindue'], '.2f'))
                    r['intdue'] = str(format(r['intdue'], '.2f'))
                    r['feesdue'] = str(format(r['feesdue'], '.2f'))

                    if r['transtypeid'] == 5:
                        r['days_late'] = str((dateutil.parser.parse(r['transdate']).date() - memory_date).days)

                    if r['transdate'] != None:
                        r['transdate'] = datetime.strptime(r['transdate'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                    else:
                        r['transdate'] = 'error'

                    if r['schddate'] != None:
                        r['schddate'] = datetime.strptime(r['schddate'], DEFAULT_SERVER_DATE_FORMAT).strftime(
                            date_format)
                    else:
                        r['schddate'] = 'error'

                    p = {
                        'transdate': 'Still Due',
                        'transtypeid': 55,
                        'days_late': '-',
                        'installment': str(format(total_prindue + total_intdue + total_feesdue, '.2f')),
                        'prindue': str(format(total_prindue, '.2f')),
                        'intdue': str(format(total_intdue, '.2f')),
                        'feesdue': str(format(total_feesdue, '.2f')),

                    }

                    full_account.append(r)

        return full_account

    def _lines_payment(self,id_idx,payment_id):
        full_account = []

        if self.partner_id != None:
            if self.account_report_id == 'detail_pay_alloc' and self.loan_no:
                query = """SELECT customer_acc_id || '-' || appln_no as id_loan
                        FROM public.loan_application WHERE loan_application.id = """ + str(self.loan_no[0].id)

                self.env.cr.execute(query)
                query_results = self.env.cr.dictfetchall()
                print 'query_results=========_lines_payment========',query_results
                if query_results[0]['id_loan'] != None:
                    id_loan = query_results[0]['id_loan']
                else:
                    id_loan = 'Null'

                if id_idx == 1:
                    query = """SELECT distinct account_move_line.amount_residual as amount_residual, 
                                account_move_line.date as payment_date, loan_payments.pmtid as payment_id,
                                tbltransactions.name as transtype FROM 
                                public.loan_payments, public.account_move_line,
                                public.tbltransactions WHERE                       
                                tbltransactions.id=loan_payments.transtypeid and
                                loan_payments.pmtid = account_move_line.payment_id and 
                                account_move_line.amount_residual <> 0 and
                                loan_payments.loanid = '""" + str(id_loan) + """' order by account_move_line.date """

                    self.env.cr.execute(query)
                    res = self.env.cr.dictfetchall()
                    print 'res===============_lines_payment====================',res
                    sum = 0.0
                    lang_code = self.env.context.get('lang') or 'en_US'
                    lang = self.env['res.lang']
                    lang_id = lang._lang_get(lang_code)
                    date_format = lang_id.date_format

                    for r in res:
                        r['amount_residual'] = str(format(r['amount_residual'], '.2f'))
                        r['payment_id'] = str(r['payment_id'])
                        r['transtype'] = "  " + str(r['transtype']) + "  "

                        if r['payment_date'] != None:
                            r['payment_date'] = datetime.strptime(r['payment_date'],
                                                                  DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
                        else:
                            r['payment_date'] = 'error'

                        full_account.append(r)
                if id_idx == 2:
                    query = """SELECT loan_payments.schddate as schddate,
                                                loan_payments.prinnotdue as prinnotdue,
                                                loan_payments.prindue + loan_payments.prinnotdue as prindue,
                                                loan_payments.intdue as intdue,loan_payments.penpaid as penpaid,
                                                loan_payments.ovdintacc as ovdintacc,loan_payments.feesdue as feesdue
                                        FROM public.loan_payments,public.account_move_line,public.tbltransactions WHERE
                                                tbltransactions.id=loan_payments.transtypeid and
                                                loan_payments.pmtid = account_move_line.payment_id and
                                                loan_payments.pmtid = """ + str(payment_id) + """ and
                                                account_move_line.amount_residual <> 0 and
                                                loan_payments.loanid = '""" + str(
                        id_loan) + """' order by loan_payments.schddate """

                    self.env.cr.execute(query)
                    res = self.env.cr.dictfetchall()
                    # contemp = self.env.cr.fetchone()
                    sum = 0.0
                    lang_code = self.env.context.get('lang') or 'en_US'
                    lang = self.env['res.lang']
                    lang_id = lang._lang_get(lang_code)
                    date_format = lang_id.date_format

                    for r in res:

                        r['prinnotdue'] = str(format(r['prinnotdue'], '.2f'))
                        r['prindue'] = str(format(r['prindue'], '.2f'))
                        r['intdue'] = str(format(r['intdue'], '.2f'))
                        r['penpaid'] = str(format(r['penpaid'], '.2f'))
                        r['ovdintacc'] = str(format(r['ovdintacc'], '.2f'))
                        r['feesdue'] = str(format(r['feesdue'], '.2f'))

                        if r['schddate'] != None:
                            r['schddate'] = datetime.strptime(r['schddate'], DEFAULT_SERVER_DATE_FORMAT).strftime(
                                date_format)
                        else:
                            r['schddate'] = '--'

                        full_account.append(r)
        return full_account

  

class generate_report(models.Model):
    _name = "generate.report"

    file = fields.Binary("Xls File")
    filename = fields.Char("Name", size=32)

