
from odoo import api, fields, models


class LoanReport(models.TransientModel):
    _name = "loan.report"
    _description = "Loan Report"

    @api.model
    def _get_account_report(self):
        reports = []
        if self._context.get('active_id'):
            menu = self.env['ir.ui.menu'].browse(self._context.get('active_id')).name
            reports = self.env['account.financial.report'].search([('name', 'ilike', menu)])
        return reports and reports[0] or False

    partner_id = fields.Many2one('res.partner', string='Partner',domain="[('is_bank_customer','=','-1')]")
    loan_no  =fields.Many2one('loan.application',string='Loan No.' , domain="[('partner_id', '=', partner_id)]")
    account_report_id = fields.Selection([
                            ('rptdetailalloc', 'Detailed Pmt Allocation'),('rptdetailschd','Detailed Schd Allocation')
                    ],string='Report Type',required=True)
    
    def _lines(self):
        full_account = []
        query = """
            SELECT 
                    account_move_line.amount_residual as amount_residual, 
                    account_move_line.date as payment_date, 
                    loan_payments.schddate as schddate, 
                    loan_payments.prinnotdue as prinnotdue, 
                    loan_payments.prindue as prindue, 
                    loan_payments.intdue as intdue, 
                    loan_payments.penpaid as penpaid, 
                    loan_payments.ovdintacc as ovdintacc, 
                    loan_payments.feesdue as feesdue
            FROM 
                    public.loan_payments, 
                    public.account_move_line
            WHERE                       
                    loan_payments.pmtid = account_move_line.payment_id and account_move_line.amount_residual<>0"""
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        sum = 0.0
        
        for r in res:
            r['schddate'] = datetime.strptime(r['schddate'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            r['payment_date'] = datetime.strptime(r['payment_date'], DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            full_account.append(r)
            full_account = [1, 2, 3]
        return full_account

    def _get_periods (self):
        array_period =[]
        
        array_period.append({'name': Alban, 'date': 2017-01-01})
        array_period.append({'name': Alban1, 'date': 2017-02-01})
        periods=list(set(array_period))
        return periods

    def _build_comparison_context(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        if data['form']['filter_cmp'] == 'filter_date':
            result['date_from'] = data['form']['date_from_cmp']
            result['date_to'] = data['form']['date_to_cmp']
            result['strict_range'] = True
        return result

    @api.multi
    def check_report(self):
        res = super(LoanReport, self).check_report()
        data = {}
        data['form'] = self.read(['partner_id'])[0]

        #for field in ['account_report_id']:
            #if isinstance(data['form'][field], tuple):
               # data['form'][field] = data['form'][field][0]
        #comparison_context = self._build_comparison_context(data)
        #res['data']['form']['comparison_context'] = comparison_context
        return res

    def print_report(self, data):
        #data['form'].update(self.read(['partner_id'])[0])
        data['form']= self.read(['partner_id','account_report_id','loan_no'])[0]
        

        #print data
        #print data['form']['partner_id'][0],data['form']['account_report_id']

        if self.account_report_id=='rptdetailalloc':
            report_data=self.env['report'].get_action(self, 'alban_loan_application.report_invoice_my', data=data)
        
        if self.account_report_id=='rptdetailschd':
            report_data=self.env['report'].get_action(self, 'alban_loan_application.days_late_schedule', data=data)
        
        return report_data


    
    def _get_account_move_lines(self, partner_ids):
        res = dict(map(lambda x:(x,[]), partner_ids))
        self.env.cr.execute("SELECT m.name AS move_id, l.date, l.name, l.ref, l.date_maturity, l.partner_id, l.blocked, l.amount_currency, l.currency_id, "
            "CASE WHEN at.type = 'receivable' "
                "THEN SUM(l.debit) "
                "ELSE SUM(l.credit * -1) "
            "END AS debit, "
            "CASE WHEN at.type = 'receivable' "
                "THEN SUM(l.credit) "
                "ELSE SUM(l.debit * -1) "
            "END AS credit, "
            "CASE WHEN l.date_maturity < %s "
                "THEN SUM(l.debit - l.credit) "
                "ELSE 0 "
            "END AS mat "
            "FROM account_move_line l "
            "JOIN account_account_type at ON (l.user_type_id = at.id) "
            "JOIN account_move m ON (l.move_id = m.id) "
            "WHERE l.partner_id IN %s AND at.type IN ('receivable', 'payable') AND NOT l.reconciled GROUP BY l.date, l.name, l.ref, l.date_maturity, l.partner_id, at.type, l.blocked, l.amount_currency, l.currency_id, l.move_id, m.name", (((fields.date.today(), ) + (tuple(partner_ids),))))
        for row in self.env.cr.dictfetchall():
            res[row.pop('partner_id')].append(row)
        return res

    @api.model
    def render_html(self, docids, data=None):
        totals = {}
        lines = self._get_account_move_lines(docids)
        lines_to_display = {}
        company_currency = self.env.user.company_id.currency_id
        for partner_id in docids:
            lines_to_display[partner_id] = {}
            totals[partner_id] = {}
            for line_tmp in lines[partner_id]:
                line = line_tmp.copy()
                currency = line['currency_id'] and self.env['res.currency'].browse(line['currency_id']) or company_currency
                if currency not in lines_to_display[partner_id]:
                    lines_to_display[partner_id][currency] = []
                    totals[partner_id][currency] = dict((fn, 0.0) for fn in ['due', 'paid', 'mat', 'total'])
                if line['debit'] and line['currency_id']:
                    line['debit'] = line['amount_currency']
                if line['credit'] and line['currency_id']:
                    line['credit'] = line['amount_currency']
                if line['mat'] and line['currency_id']:
                    line['mat'] = line['amount_currency']
                lines_to_display[partner_id][currency].append(line)
                if not line['blocked']:
                    totals[partner_id][currency]['due'] += line['debit']
                    totals[partner_id][currency]['paid'] += line['credit']
                    totals[partner_id][currency]['mat'] += line['mat']
                    totals[partner_id][currency]['total'] += line['debit'] - line['credit']
        docargs = {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': self.env['res.partner'].browse(docids),
            'time': time,
            'Lines': lines_to_display,
            'Totals': totals,
            'Date': fields.date.today(),
        }
        return self.env['report'].render('alban_loan_application.report_invoice_my', values=docargs)
