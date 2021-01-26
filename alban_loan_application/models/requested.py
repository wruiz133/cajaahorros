from odoo import models, fields, api,_
import datetime
import math
import time
#from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import dateutil.parser
from odoo.exceptions import UserError,ValidationError
import filestore_generic
import dateutil
import exceptions
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class loan_application(models.Model):
    _inherit = "loan.application"

    currency = fields.Many2one('res.currency',string='Currency', help='Utility field to express amount currency')
    requested_amt = fields.Float(string='Requested Amount')
    tendor = fields.Integer(string='Tendor(In Months)')

    person_amt = fields.Float(string='Personal Amount')
    family_amt = fields.Float(string="Family Friend's Amount")
    specify_amt = fields.Float(string="Specify Purpose Investment")

    rate = fields.Integer(string='Rate')
    do_pay_amt = fields.Float(string="Down Payment Amount")
    type_payment = fields.Char(string='Type Of Payment',)
    # legal_status = fields.Selection(string='Legal Status',required=True)
    req_item_ids = fields.One2many('requested.item','req_item_id')
    doc_det_ids = fields.One2many('document.details','doc_det_id')#============for document details


#     ===============for company tab=============
    type_of =fields.Selection([('type1', 'Type 1'), ('type2', 'Type 2')],string='Type Of')


class requested_item(models.Model):
    _name = "requested.item"

    itemiztion = fields.Char(string='Itemiztion')
    requested_amt = fields.Float(string='Requested Amount')
    comments = fields.Char(string='Comments')

    req_item_id = fields.Many2one('loan.application',string='Requested Itemizations')

# =====================================for documents tab==========================

class document_details(models.Model):
    _name = "document.details"

    doc_title = fields.Char(string='Document Title',required=True)
    desc = fields.Text(string='Description')
    upload_date = fields.Datetime(' Date + Time' ,readonly=True)
    uploaded_by = fields.Many2one('res.users', string='User ',readonly=True)
    type = fields.Char(string='Type',compute='get_extension')
    doc_file = fields.Binary(string='Document*',required=True)

    filename = fields.Char(string='filename')

    static_test = fields.Char('Careful',default="""File types that can be charged:\
      .pdf,.jpeg,.jpg,.gif,.doc,.docx,.xls,.xlsx\
      .pdf files must have a maximum size of 3,000Kb\
      Other files must have a maximum size of 500Kb""")

    doc_det_id = fields.Many2one('loan.application',string='Document Upload')
    
    # to get the type of the file and write it into type field
    @api.one
    @api.depends('filename')
    def get_extension(self):
        filename = self.filename
        flag = False

        if filename:
            # flag = self.check_extension()
            flag = filestore_generic.FilestoreGeneric(filename).check_extension(filename)
            if not flag:
                extension = filename[filename.rfind('.'):]
                self.type = extension + " document"

    @api.model
    def create(self, vals):

        current_date = datetime.datetime.now()
        print 'in the create def============================'
        if self._uid:
            vals.update({'uploaded_by': self._uid, 'upload_date': current_date})

        res = super(document_details, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        current_date = datetime.datetime.now()
        if self._uid:
            # vals.update({'updated_by':self._uid,'id':res})
            vals.update({'uploaded_by': self._uid, 'upload_date': current_date, })
            print 'after vals getting updated============================'

        res = super(document_details, self).write(vals)
        return res

    # @api.one
    # @api.constrains('filename')
    # def _check_filename(self):
    #     if self.doc_file:
    #         if not self.filename:
    #             raise exceptions.ValidationError(_("There is no file"))
    #     else:
    #         # Check the file's extension
    #         tmp = self.filename.split('.')
    #         ext = tmp[len(tmp) - 1]
    #         file_ext = ['pdf','jpeg','jpg','gif','doc','docx','xls','xlsx']
    #         for f_ext in file_ext:
    #             if ext != f_ext:
    #                 raise exceptions.ValidationError(_("The file must be a %s file"+f_ext))


# ================================================================================

# ===========================for fields tab==================================
class loan_application(models.Model):
    _inherit = "loan.application"

    field1 = fields.Char(string=' ')
    field2 = fields.Char(string=' ')
    field3 = fields.Char(string=' ')
    field4 = fields.Char(string=' ')
    field5 = fields.Char(string=' ')
    field6 = fields.Char(string=' ')
    field7 = fields.Char(string=' ')
    field8 = fields.Char(string=' ')
    field9 = fields.Char(string=' ')
    field10 = fields.Char(string=' ')
    field11 = fields.Char(string=' ')
    field12 = fields.Char(string=' ')
    field13 = fields.Char(string=' ')
    field14 = fields.Char(string=' ')
    field15 = fields.Char(string=' ')
    field16 = fields.Char(string=' ')
    field17 = fields.Char(string=' ')
    field18 = fields.Char(string=' ')
    field19 = fields.Char(string=' ')
    field20 = fields.Char(string=' ')


    field_date_1 = fields.Date(string='field1')
    field_date_2 = fields.Date(string='field2')
    field_date_3 = fields.Date(string='field3')
    field_date_4 = fields.Date(string='field4')
    field_date_5 = fields.Date(string='field5')

    field_num_1 = fields.Integer(string='field6')
    field_num_2 = fields.Integer(string='field7')
    field_num_3 = fields.Integer(string='field8')
    field_num_4 = fields.Integer(string='field9')
    field_num_5 = fields.Integer(string='field10')
    field_num_6 = fields.Integer(string='field11')
    field_num_7 = fields.Integer(string='field12')
    field_num_8 = fields.Integer(string='field13')
    field_num_9 = fields.Integer(string='field14')
    field_num_10 = fields.Integer(string='field15')
    field_num_11 = fields.Integer(string='field16')
    field_num_12 = fields.Integer(string='field17')
    field_num_13 = fields.Integer(string='field18')
    field_num_14 = fields.Integer(string='field19')
    field_num_15 = fields.Integer(string='field20')

# =========================for additional fields in account payment==================
class account_payment(models.Model):
    _inherit = "account.payment"

    receipt_no = fields.Char(string='Receipt No.')
    loan_no  =fields.Many2one('loan.application',string='Loan No.' , domain="[('partner_id', '=', partner_id)]")
    bank_date = fields.Date(string='Bank Date')
    fund_src = fields.Char(string='Funding Source')
    trans_type = fields.Selection([('1','Disbursement'),
                                    ('2','Additional Disb.'),
                                    ('4','Scheduled Payment'),
                                    ('5','Repayment'),
                                    ('6','Buy Down'),
                                    ('7','Penalty Writeoff'),
                                    ('8','Interest Writeoff'),
                                    ('9','Total Writeoff'),
                                    ('10','Rescheduling'),
                                    ('12','Grace Period'),
                                    ('13','Penalty Stop'),
                                    ('14','Penalty Charge'),
                                    ('15','Overdue Int Writeoff'),
                                    ('16','Returned Principal'),
                                    ('17','Transfer In'),
                                    ('18','Transfer Out'),
                                    ('19','Recov Pen Pmt'),
                                    ('20','Recov Pen Rev'),
                                    ('21','Future Interest Writeoff'),
                                    ('90','Cash Over'),
                                    ('91','Cash Short'),
                                    ('92','Recovery'),
                                    ('101','Deposit'),
                                    ('105','Withdrawal'),
                                    ('109','Forfeit'),
                                    ('117','Transfer In Dpst'),
                                    ('118','Transfer Out Dpst'),
                                    ('120','IntPost'),
                                    ('121','TaxPost'),
                                    ('191','Cash Over Dpst'),
                                    ('200','Accrual')],string='Transaction Type')
    last_pmt_date =  fields.Date(string='Last Payment Date')
    pmtamt=fields.Float (string='Repayment amount in payment currency (usually local currency)')
    tot_close = fields.Float(string='Total to close')
    communication = fields.Text(string='Memo')
    created_by = fields.Many2one('res.partner',string='Created By')

    @api.model
    def create(self, vals):

        # print 'in the create def============================'
        if self._uid:
            vals.update({'created_by': self._uid,'pmtamt': -1, })

        # _logger.info('=====================vals %s======================' % vals)
        res = super(account_payment, self).create(vals)

        return res

    def _create_payment_entry(self, amount):
        """ Create a journal entry corresponding to a payment, if the payment references invoice(s) they are reconciled.
            Return the journal entry.
        """
        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        invoice_currency = False
        if self.invoice_ids and all([x.currency_id == self.invoice_ids[0].currency_id for x in self.invoice_ids]):
            #if all the invoices selected share the same currency, record the paiement in that currency too
            invoice_currency = self.invoice_ids[0].currency_id
        debit, credit, amount_currency, currency_id = aml_obj.with_context(date=self.payment_date).compute_amount_fields(amount, self.currency_id, self.company_id.currency_id, invoice_currency)

        move = self.env['account.move'].create(self._get_move_vals())

        #Write line corresponding to invoice payment
        counterpart_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, move.id, False)
        counterpart_aml_dict.update(self._get_counterpart_move_line_vals(self.invoice_ids))
        counterpart_aml_dict.update({'currency_id': currency_id})
        counterpart_aml_dict.update({'bank_date': self.bank_date})
        counterpart_aml_dict.update({'loan_no': self.loan_no})
        counterpart_aml_dict.update({'receipt_no': self.receipt_no})
        counterpart_aml_dict.update({'fund_src': self.fund_src or ''})

        # print 'counterpart_aml_dict=======================',counterpart_aml_dict
        _logger.info('=====================counterpart_aml_dict  %s======================' % counterpart_aml_dict)
        # vvvvv
        counterpart_aml = aml_obj.create(counterpart_aml_dict)

        #Reconcile with the invoices
        if self.payment_difference_handling == 'reconcile' and self.payment_difference:
            writeoff_line = self._get_shared_move_line_vals(0, 0, 0, move.id, False)
            debit_wo, credit_wo, amount_currency_wo, currency_id = aml_obj.with_context(date=self.payment_date).compute_amount_fields(self.payment_difference, self.currency_id, self.company_id.currency_id, invoice_currency)
            writeoff_line['name'] = _('Counterpart')
            writeoff_line['account_id'] = self.writeoff_account_id.id
            writeoff_line['debit'] = debit_wo
            writeoff_line['credit'] = credit_wo
            writeoff_line['amount_currency'] = amount_currency_wo
            writeoff_line['currency_id'] = currency_id
            writeoff_line = aml_obj.create(writeoff_line)
            if counterpart_aml['debit']:
                counterpart_aml['debit'] += credit_wo - debit_wo
            if counterpart_aml['credit']:
                counterpart_aml['credit'] += debit_wo - credit_wo
            counterpart_aml['amount_currency'] -= amount_currency_wo
        self.invoice_ids.register_payment(counterpart_aml)

        #Write counterpart lines
        if not self.currency_id != self.company_id.currency_id:
            amount_currency = 0
        liquidity_aml_dict = self._get_shared_move_line_vals(credit, debit, -amount_currency, move.id, False)
        liquidity_aml_dict.update(self._get_liquidity_move_line_vals(-amount))
        aml_obj.create(liquidity_aml_dict)
        print self._loan_calculator()

        move.post()
        return move

    def _get_shared_move_line_vals(self, debit, credit, amount_currency, move_id, invoice_id=False):
        """ Returns values common to both move lines (except for debit, credit and amount_currency which are reversed)
        """
        return {
            'partner_id': self.payment_type in ('inbound', 'outbound') and self.env['res.partner']._find_accounting_partner(self.partner_id).id or False,
            'invoice_id': invoice_id and invoice_id.id or False,
            'move_id': move_id,
            'debit': debit,
            'credit': credit,
            'receipt_no':self.receipt_no or '',
            'fund_src':self.fund_src or '',
            'loan_no':self.loan_no or '',
            'bank_date':self.bank_date,
            'amount_currency': amount_currency or False,
        }




    @api.model
    def _loan_calculator(self):
        query = ''
        #select_sql_clause = """delete from loan_payments_tmp where"""
        #query += ""+select_sql_clause+" schedule_id ='t100'"
        #self.env.cr.execute(query)


        #CREATE TABLE public.tbltransactions
        #(
          #id integer NOT NULL ,
          
          #name character varying, -- City Name:
          #active integer

        #);


        #insert into tbltransactions
        #(id,name,active)
        #values
        #(1, 'Disbursement', 1),
        #(2, 'Additional Disb',  1),
        #(4, 'Scheduled Payment',    1),
        #(5, 'Repayment',    1),
        #(6, 'Buy Down', 0),
        #(7, 'Penalty Writeoff', 1),
        #(8, 'Interest Writeoff',    1),
        #(9, 'Total Writeoff',   1),
        #(10,    'Rescheduling', 0),
        #(12,    'Grace Period', 0),
        #(13,    'Penalty Stop', 0),
        #(14,    'Penalty Charge',   1),
        #(15,    'Overdue Int Writeoff', 1),
        #(16,    'Returned Principal',   1),
        #(17,    'Transfer In',  1),
        #(18,    'Transfer Out', 1),
        #(19,    'Recov Pen Pmt',    1),
        #(20,    'Recov Pen Rev',    1),
        #(21,    'Future Interest Writeoff', 1),
        #(90,    'Cash Over',    1),
        #(91,    'Cash Short',   1),
        #(92,    'Recovery', 1),
        #(101,   'Deposit',  1),
        #(105,   'Withdrawal',   1),
        #(109,   'Forfeit',  1),
        #(117,   'Transfer In Dpst', 1),
        #(118,   'Transfer Out Dpst',    1),
        #(120,   'IntPost',  1),
        #(121,   'TaxPost',  1),
        #(191,   'Cash Over Dpst',   1),
        #(200,   'Accrual',  0);


        amount_paid=self.amount

        query = ''
        #select_sql_clause = """insert into loan_payments_tmp select * from loan_payments where """
        #query += ""+select_sql_clause+" schedule_id ='t100'"
        #self.env.cr.execute(query)

        #my_kest=(-self.financing_amt + (-self.financing_amt/(math.pow(((self.interest_rate/100/12)+1),self.install_count) -1)))*-(self.interest_rate/100/12)
        #my_kest=72388.44
        schedule_id = str(self.loan_no.id)
        select_sql_clause = """select customer_acc_id || '-' || appln_no as id_loan,financing_amt,interest_rate,install_count from loan_application where id = """+ str(self.loan_no.id)
        self.env.cr.execute(select_sql_clause)
        #id_loan=self.env.cr.fetchone() (u'0000018-001',)
        query_results = self.env.cr.dictfetchall()
        if query_results[0].get('id_loan') != None:
                id_loan=query_results[0].get('id_loan')
        else:
                id_loan='Null'

        if query_results[0].get('financing_amt') != None:
                financing_amt=query_results[0].get('financing_amt')
        else:
                financing_amt='Null'

        if query_results[0].get('interest_rate') != None:
                interest_rate=query_results[0].get('interest_rate')
        else:
                interest_rate='Null'

        if query_results[0].get('install_count') != None:
                install_count=query_results[0].get('install_count')
        else:
                install_count='Null'

        grace_penalty=0L
        penalty_rate = float(0.1)/100

        my_kest=(-financing_amt + (-financing_amt/(math.pow(((interest_rate/100/12)+1),install_count) -1)))*-(interest_rate/100/12)
        
        

        previous_date=dateutil.parser.parse(self.payment_date).date()
        

        
        #outstanding come from above

        #interest_calculated=outstanding*0.0403/100*days_late


        if self.payment_type == 'outbound':
            ##############################################################################
            ##############################################################################
            ##############################################################################
            ######################           Step 0            ###########################
            ######################  Insert of Fee/Disbursment  ###########################
            ######################                             ########################### 
            ##############################################################################
            ##############################################################################
            ##############################################################################
            select_sql_clause = """SELECT id,schddate from loan_schedule where schedule_id=""" + str(schedule_id) + """ and transtypeid=1"""
                
            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            
            if query_results[0].get('id') != None:
                schid=query_results[0].get('id')
            else:
                schid='Null'
                
            if query_results[0].get('schddate') != None:
                schddate=dateutil.parser.parse(query_results[0].get('schddate')).date()
            else:
                schddate='Null'

                        
            insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,            prinnotdue,        prindue,intnotdue,intdue,intcap,             intacc,penpaid,pencap,penacc,feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
            #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
            #on other products
            #insert_sql_clause += """ values  (     '0000018',1,          '"""+str(self.bank_date) +"""',"""+str(schid)+""",'"""+schddate+"""',   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
            #insert_sql_clause += """ values  (     '""" + id_loan + """',1,          '"""+str(self.payment_date) +"""',"""+str(schid)+""",'"""+schddate+"""',   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     0,     0,     0,      0,     0,     0,      0,         0,         0)"""
            
            insert_sql_clause += """ values  (     '""" + id_loan + """',1,          '"""+str(self.payment_date) +"""',"""+str(schid)+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     0,     0,     0,      0,     0,     0,      0,         0,         0)"""
                
            
            outstand_amt_amortized=self.amount
            

            self.env.cr.execute(insert_sql_clause)


            
            ### schedule insert
            select_sql_clause = """SELECT id,schddate from loan_schedule where schedule_id=""" + str(schedule_id) + """ and transtypeid=4 order by schdnr"""
                
            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()

            if query_results[0].get('id') != None:
                schid=query_results[0].get('id') 
            else:
                schid='Null'

            if query_results[0].get('schddate') != None:
                schddate=dateutil.parser.parse(query_results[0].get('schddate')).date()
            else:
                schddate='Null'

            
            end_of_month_date= schddate.replace(day=1)  
            #print end_of_month_date
            #200
            insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,            prinnotdue,        prindue,intnotdue,intdue,intcap,             intacc,                  penpaid,pencap,                         penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
            #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
            
            insert_sql_clause += """ values  (     '""" + id_loan + """',200,          '"""+str(end_of_month_date) +"""',Null,Null,   Null,0,0,      0,        0,                                            0,     0,        0, 0,     0,     0,      0,         0,         0)"""
            self.env.cr.execute(insert_sql_clause)
                    

            





        else:
            
            select_sql_clause = """SELECT max(schddate) as max_date 
                                   from loan_payments 
                                   where 
                                         loanid ='""" + id_loan + """' and
                                         transdate <='"""+ str(dateutil.parser.parse(self.payment_date).date()) + """' and 
                                         transtypeid=4"""
            max_date='1900-01-01'
            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            if query_results[0].get('max_date') !=None:
                max_date=dateutil.parser.parse(query_results[0].get('max_date')).date()


            select_sql_clause = """SELECT 
                                        sum(loan_payments.intdue) as total_interes_remain, 
                                        sum(loan_payments.prindue) as total_principal_remain
                                   FROM 
                                        loan_payments, 
                                        loan_schedule
                                   WHERE 
                                        loan_payments.schdid = loan_schedule.id and loan_payments.transtypeid in (4,5) and loan_payments.loanid ='""" + id_loan + """'
                                        and loan_schedule.schddate<='"""+ str(max_date) + """'
                                """


            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            
            total_principal_remain=0.0000
            prinnotdue=0.0000
            total_interes_remain=0.0000
            total_pen_to_pay = 0.00000
            corresponding_pen = 0.0000
            

            if query_results[0].get('total_interes_remain') != None:
                total_interes_remain=query_results[0].get('total_interes_remain') 
                  
            if query_results[0].get('total_principal_remain') != None:
                total_principal_remain=query_results[0].get('total_principal_remain')

            #Penalty from previous schedules    
                                                
            select_sql_clause = """SELECT 
                                        sum(loan_payments.penacc) + sum(loan_payments.penpaid) as total_pen_to_pay
                                   FROM 
                                        loan_payments
                                   WHERE 
                                        loan_payments.loanid ='""" + id_loan + """'
                                        and loan_payments.transdate<='"""+ str(dateutil.parser.parse(self.payment_date).date()) + """'
                                """


            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            if query_results[0].get('total_pen_to_pay') != None:
                total_pen_to_pay=query_results[0].get('total_pen_to_pay') 


            ###### The value from schedule Id to be calculated for Penalty
            if grace_penalty == 0:
                select_sql_clause = """SELECT 
                                            sum(loan_payments.pencap) as corresponding_pen
                                       FROM 
                                            loan_payments
                                            
                                       WHERE 
                                            loan_payments.transtypeid in (4,13)  and loan_payments.loanid ='""" + id_loan + """'
                                            and loan_payments.transdate<='"""+ str(dateutil.parser.parse(self.payment_date).date()) + """'
                                    """


            else:

                select_sql_clause = """SELECT 
                                            sum(loan_payments.pencap) as corresponding_pen
                                       FROM 
                                            loan_payments
                                            
                                       WHERE 
                                            loan_payments.transtypeid in (12,13)  and loan_payments.loanid ='""" + id_loan + """'
                                            and loan_payments.transdate<='"""+ str(dateutil.parser.parse(self.payment_date).date()) + """'
                                    """


            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            if query_results[0].get('corresponding_pen') != None:
                corresponding_pen=query_results[0].get('corresponding_pen') 


            select_sql_clause = """SELECT 
                                        max(loan_payments.transdate) as max_transdate
                                   FROM 
                                        loan_payments
                                        
                                   WHERE 
                                        loan_payments.loanid ='""" + id_loan + """'
                                        and loan_payments.transdate<='"""+ str(dateutil.parser.parse(self.payment_date).date()) + """'
                                """

                
            max_transdate='1900-01-01'
            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            if query_results[0].get('max_transdate') !=None:
                max_transdate=dateutil.parser.parse(query_results[0].get('max_transdate')).date()

            days_late = (dateutil.parser.parse(self.payment_date).date() - max_transdate).days
            if days_late <0:
                days_late =0
            
            ###############################################################################
            ###############################################################################
            ###############################################################################
            ###############################################################################
            penalty_amount_calculation = 0.00000
            penalty_amount_calculation = corresponding_pen*penalty_rate*days_late
            print corresponding_pen,days_late,total_pen_to_pay,penalty_amount_calculation

            penalty_to_be_paid=penalty_amount_calculation+total_pen_to_pay
            

            if penalty_to_be_paid>=amount_paid:
                penalty_to_be_paid=amount_paid
                amount_paid=0
            else:
                amount_paid=amount_paid-penalty_to_be_paid

           
            if amount_paid <= total_interes_remain:
                total_interes_remain=amount_paid
                amount_paid=0
            else:
                amount_paid=amount_paid-total_interes_remain

            if amount_paid  <= total_principal_remain:
                total_principal_remain=amount_paid
                amount_paid=0
            else:
                amount_paid=amount_paid-total_principal_remain
            
            #prinnotdue=amount_paid-total_interes_remain-total_principal_remain
            prinnotdue=amount_paid
            

            select_sql_clause = """SELECT 
                                        sum(loan_payments.intdue) as total_interes_due_monthly, 
                                        sum(loan_payments.prindue) as total_principal_due_monthly, 
                                        loan_schedule.id, 
                                        loan_schedule.schddate
                                   FROM 
                                        loan_payments, 
                                        loan_schedule
                                   WHERE 
                                        loan_payments.schdid = loan_schedule.id and loan_payments.transtypeid in (4,5) and loan_payments.loanid ='""" + id_loan + """'
                                   Group by
                                        loan_schedule.id, 
                                        loan_schedule.schddate
                                   order by
                                        loan_schedule.schdnr, 
                                        loan_schedule.schddate"""


            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            
            
            #index=0L
            for index in range(0, len(query_results)):
                
                schid=0L    
                schddate='1900-01-01'
                total_interes_due_monthly=0.00000
                total_principal_due_monthly=0.00000
                total_interes_due_monthly_index=0.0000
                total_principal_due_monthly_index=0.0000
                
                if query_results[index].get('id') != None:
                    schid=query_results[index].get('id') 
                    
                        

                if query_results[index].get('schddate') != None:                            
                    schddate=dateutil.parser.parse(query_results[index].get('schddate')).date()
                    
                    
                if query_results[index].get('total_interes_due_monthly') != None:
                    total_interes_due_monthly=query_results[index].get('total_interes_due_monthly')
                    
                        
                if query_results[index].get('total_principal_due_monthly') != None:
                    total_principal_due_monthly=query_results[index].get('total_principal_due_monthly')
                          
                
                if  total_interes_remain <= total_interes_due_monthly:
                    total_interes_due_monthly_index=total_interes_remain
                else:
                    total_interes_due_monthly_index=total_interes_due_monthly
                

                if total_principal_remain <= total_principal_due_monthly:
                    total_principal_due_monthly_index=total_principal_remain
                else:
                    total_principal_due_monthly_index=total_principal_due_monthly



                if total_interes_due_monthly_index == 0 and total_principal_due_monthly_index == 0 and (penalty_amount_calculation>0.00001 or penalty_to_be_paid>0.00001):
                    insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid, prinnotdue,               prindue,                   intnotdue,                           intdue,            intcap,intacc,  penpaid,pencap,penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                        #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                        #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                    insert_sql_clause += """ values  (     '""" + str(id_loan) + """',5,          '"""+str(self.payment_date) +"""',Null,Null, """+str(self.id)+""", 0 ,"""+str(-1*total_principal_due_monthly_index)+"""  ,  0, """+str(-1*(total_interes_due_monthly_index))+""",   0,     0, """ + str(-1*penalty_to_be_paid) + """,      0,""" + str(penalty_amount_calculation) + """,     0,      0,         0,         0) """
            
                    self.env.cr.execute(insert_sql_clause)
                
                elif total_interes_due_monthly_index > 0.00001 or total_principal_due_monthly_index > 0.00001 or penalty_amount_calculation>0.00001 or penalty_to_be_paid>0.00001:
                    insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid, prinnotdue,               prindue,                   intnotdue,                           intdue,            intcap,intacc,  penpaid,pencap,penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                        #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                        #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                    insert_sql_clause += """ values  (     '""" + str(id_loan) + """',5,          '"""+str(self.payment_date) +"""',"""+str(schid)+""",'"""+str(schddate)+"""', """+str(self.id)+""", 0 ,"""+str(-1*total_principal_due_monthly_index)+"""  ,  0, """+str(-1*(total_interes_due_monthly_index))+""",   0,     0, """ + str(-1*penalty_to_be_paid) + """,      0,""" + str(penalty_amount_calculation) + """,     0,      0,         0,         0) """
            
                    self.env.cr.execute(insert_sql_clause)


                penalty_amount_calculation = penalty_amount_calculation - penalty_amount_calculation
                penalty_to_be_paid = penalty_to_be_paid - penalty_to_be_paid
                total_interes_remain = total_interes_remain - total_interes_due_monthly_index
                total_principal_remain = total_principal_remain - total_principal_due_monthly_index

            if prinnotdue > 0.00009:
                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid, prinnotdue,               prindue,                   intnotdue,                           intdue,            intcap,intacc,  penpaid,pencap,penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                        #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                        #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                insert_sql_clause += """ values  (     '""" + str(id_loan) + """',5,          '"""+str(self.payment_date) +"""',Null,Null, """+str(self.id)+""","""+str(-1*prinnotdue)+""",0  ,  0,  0 ,   0,     0,     0,      0,     0,     0,      0,         0,         0) """
            
                self.env.cr.execute(insert_sql_clause)
        
            query = ''
            #Per rastin qe oustanding do dali nga skeduli ose pagesat e kryera faktike ketu behet ndryshimi;
            blnasfund = 1
            if blnasfund==1:
                query = """SELECT sum(schdprin) as outstanding 
                                        from loan_schedule 
                                       where schddate <='"""+ str(dateutil.parser.parse(self.payment_date).date()) + """' and 
                                             schedule_id = """ + str(schedule_id) + """ and transtypeid in (1,4)"""
                    
            else:
                select_sql_clause = """select sum(prinnotdue + prindue) as outstanding from loan_payments where """
                query +=  select_sql_clause+""" loanid  ='""" + str(id_loan) +"""'"""
                

            self.env.cr.execute(query)
            
            query_results = self.env.cr.dictfetchall()
            outstand_amt_amortized=0.0000000

            if query_results[0].get('outstanding') != None:
                outstand_amt_amortized=query_results[0].get('outstanding') 
            


            
        

        if self.payment_type == 'outbound' or  self.payment_type == 'inbound':

            #################################################################
            #################################################################
            #################################################################
            ###################     Reprocessing  ###########################
            #################################################################
            #################################################################
            #################################################################
            
            ### schedule insert
            select_sql_clause = """SELECT id,schddate 
                                        from loan_schedule 
                                       where schddate >'"""+ str(dateutil.parser.parse(self.payment_date).date()) + """' and 
                                             schedule_id = """ + str(schedule_id) + """ and transtypeid=4 order by schdnr """
                    
            self.env.cr.execute(select_sql_clause)
            query_results = self.env.cr.dictfetchall()
            if query_results[0].get('schddate') != None:
                schddate=dateutil.parser.parse(query_results[0].get('schddate')).date()
            else:
                schddate='Null'
            



            if self.payment_type == 'inbound':

                select_sql_clause = """SELECT 
                                            sum(loan_payments.intdue) + sum(loan_payments.prindue) as corresponding_pen
                                       FROM 
                                            loan_payments
                                            
                                       WHERE 
                                            loan_payments.schdid = """+str(schid)+""" and loan_payments.transtypeid <>1 and loan_payments.loanid ='""" + id_loan + """'
                                            and loan_payments.transdate <='"""+ str(dateutil.parser.parse(self.payment_date).date()) + """'
                                    """

                self.env.cr.execute(select_sql_clause)
                query_results_under = self.env.cr.dictfetchall()
                        
                    #total_principal_remain=0.0000
                penalty_amount_calculation=0.0000
                #Crimson
                if query_results_under[0].get('corresponding_pen') != None:
                    penalty_amount_calculation=query_results_under[0].get('corresponding_pen')

                #delete all one schedule later
                select_sql_clause = """    delete 
                                           from loan_payments 
                                           where 
                                                 loanid ='""" + id_loan + """' and
                                                 transdate >'"""+ str(schddate) + """' and 
                                                 transtypeid <>5 """     
                self.env.cr.execute(select_sql_clause)

                #delete all with transtypeid=4 one schedule later
                
                select_sql_clause = """   delete 
                                           from loan_payments 
                                           where 
                                                 loanid ='""" + id_loan + """' and
                                                 transdate ='"""+ str(schddate) + """' and 
                                                 transtypeid = 4 """     
                self.env.cr.execute(select_sql_clause)
                

                if penalty_amount_calculation <= 0.1 and grace_penalty > 0:
                    select_sql_clause = """    delete 
                                           from loan_payments 
                                           where 
                                                 loanid ='""" + id_loan + """' and
                                                 transdate >'"""+ str(dateutil.parser.parse(self.payment_date).date()) + """' and 
                                                 transtypeid in (12,13) """     
                    self.env.cr.execute(select_sql_clause)

                if grace_penalty == 0:
                    select_sql_clause = """SELECT id,transtypeid,transdate from loan_payments 
                                                where transdate >= '""" + str(dateutil.parser.parse(self.payment_date).date()) + """' and 
                                                transtypeid in (4,13,200) and loanid ='""" + id_loan + """' order by transdate,transtypeid"""    
                else:
                    select_sql_clause = """SELECT id,transtypeid,transdate from loan_payments 
                                                where transdate >= '""" + str(dateutil.parser.parse(self.payment_date).date()) + """' and 
                                                transtypeid in (12,13,200) and loanid ='""" + id_loan + """' order by transdate,transtypeid"""    

                self.env.cr.execute(select_sql_clause)
                query_results_under = self.env.cr.dictfetchall()
                blncontinue_12 = 1
                blncontinue_13 = 1
                blncontinue_200 = 1
               
                for index in range(0, len(query_results_under)):
                    if query_results_under[index].get('id') != None:
                        if query_results_under[index].get('id') != None:
                            payments_id=query_results_under[index].get('id') 
                        else:
                            payments_id='Null'

                        if query_results_under[index].get('transtypeid') != None:
                            transtypeid=query_results_under[index].get('transtypeid')
                        else:
                            transtypeid='Null'

                        if query_results_under[index].get('transdate') != None:
                            record_date=dateutil.parser.parse(query_results_under[index].get('transdate')).date()
                        else:
                            record_date='Null'

                        days_diff=(record_date-previous_date).days
                        if days_diff<0:
                            days_diff=0

                        days_diff_payment=(record_date-dateutil.parser.parse(self.payment_date).date()).days
                        if days_diff_payment<0:
                            days_diff_payment=0

                        
                        if transtypeid==4 and blncontinue_12==1:
                            
                            update_sql_clause = """update loan_payments set pencap = '""" +str(penalty_amount_calculation) +"""'  where id = """ +str(payments_id)+ """  """
                            blncontinue_12 = 2

                        if days_diff_payment>0:
                            
                            if transtypeid==12 and blncontinue_12==1:
                                update_sql_clause = """update loan_payments set pencap = '""" +str(penalty_amount_calculation) +"""'  where id = """ +str(payments_id)+ """  """
                                blncontinue_12 = 2
                            
                            if transtypeid==13 and  blncontinue_13==1:
                                if blncontinue_12 == 2:
                                    update_sql_clause = """update loan_payments set pencap = '""" +str(-1*penalty_amount_calculation) +"""' , penacc=""" +str(days_diff*penalty_amount_calculation*penalty_rate) + """ where id = """ +str(payments_id)+ """  """
                                else:
                                    update_sql_clause = """update loan_payments set  penacc=""" +str(days_diff*penalty_amount_calculation*penalty_rate) + """ where id = """ +str(payments_id)+ """  """                            
                                blncontinue_13==2
                            if transtypeid==200 and   blncontinue_200==1:
                                update_sql_clause = """update loan_payments set penacc=""" +str(days_diff*penalty_amount_calculation*penalty_rate) + """ where id = """ +str(payments_id)+ """  """
                                blncontinue_200==2
                        
                        self.env.cr.execute(update_sql_clause)

                        previous_date=record_date



            


            #select_sql_clause = """SELECT id,schddate from loan_schedule where schedule_id=""" + str(schedule_id) + """ and transtypeid=4 """
                
            #self.env.cr.execute(select_sql_clause)
            #query_results = self.env.cr.dictfetchall()
            #print len(query_results)
                
            for index in range(0, len(query_results)):
                if query_results[index].get('id') != None:
                    if query_results[index].get('id') != None:
                        schid=query_results[index].get('id') 
                    else:
                        schid='Null'

                    if query_results[index].get('schddate') != None:
                        schddate=dateutil.parser.parse(query_results[index].get('schddate')).date()
                    else:
                        schddate='Null'

                    #Error on calculation    
                    select_sql_clause = """SELECT 
                                            sum(loan_payments.intdue) as total_interes_remain, 
                                            sum(loan_payments.prindue) as total_principal_remain
                                       FROM 
                                            loan_payments
                                            
                                       WHERE 
                                            loan_payments.schdid = """+str(schid)+""" and loan_payments.transtypeid <>1 and loan_payments.loanid ='""" + id_loan + """'
                                            and loan_payments.transdate <='"""+ str(schddate) + """'
                                    """




                    #select_sql_clause = """SELECT 
                    #                    sum(loan_payments.pencap) as corresponding_pen
                    #               FROM 
                    #                    loan_payments
                    #                    
                    #               WHERE 
                    #                    loan_payments.transtypeid in (12,13)  and loan_payments.loanid ='""" + id_loan + """'
                    #                    and loan_payments.schddate<='"""+ str(schddate) + """'
                    #            """

                    self.env.cr.execute(select_sql_clause)
                    query_results_under = self.env.cr.dictfetchall()
                        
                    total_principal_remain=0.0000
                    penalty_amount_calculation=0.0000
                    total_interes_remain=0.0000

                        

                    if query_results_under[0].get('total_interes_remain') != None:
                            total_interes_remain=query_results_under[0].get('total_interes_remain') 
                              
                    if query_results_under[0].get('total_principal_remain') != None:
                            total_principal_remain=query_results_under[0].get('total_principal_remain')
                                                            
                
                    #Crimson ################################################################
                    #Crimson ################################################################
                    #Crimson ################################################################
                    #Crimson ################################################################

                    #if query_results_under[0].get('corresponding_pen') != None:
                        #=query_results_under[0].get('corresponding_pen')
                    #if self.payment_type == 'outbound':
                    penalty_amount_calculation = my_kest
                    #else:
                    #    penalty_amount_calculation=total_interes_remain+total_principal_remain
                    
                        

                        
                    one_month= relativedelta(months=+1)

                    end_of_month_date= schddate.replace(day=1)

                    #if self.payment_type == 'outbound':
                    end_of_month_date=end_of_month_date+one_month  

                    #print end_of_month_date

                    ##################################################################################
                    ############ if EOMONTH bigger then Schdate             ##########################
                    ##################################################################################


                    if end_of_month_date >= schddate:

                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                        ######################           Step III          ###########################
                        ######################          Schedule Part      ###########################
                        ##############################################################################
                        ##############################################################################
                        ##############################################################################



                            #4
                            # the installment of first schedule is saved
                            

                        days_late=(schddate-previous_date).days
                        if days_late < 0:
                            days_late = 0

                        
                            #360 days configuration    
                        days_late=30
                        days_late_penalty = (schddate-previous_date).days
                        if days_late_penalty < 0:
                            days_late_penalty = 0

                        if grace_penalty == 0:
                            #Rasti per Chrimson per te tjeret duhet te shikosh
                            #penalty_amount_calculation = my_kest

                            if index==len(query_results)-1:
                                    #this for adjusing the installment at end
                                my_kest=outstand_amt_amortized*days_late*(interest_rate/100/360)+outstand_amt_amortized
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                                     penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                    #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                    #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",0,0,0,"""+str(1*(penalty_amount_calculation))+""",0,0,0,0,0) """
                        
                                self.env.cr.execute(insert_sql_clause)

                            else:
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",   0,     0,     0,    """+str(1*(penalty_amount_calculation))+""",0,0,0,0,0) """
                        
                                self.env.cr.execute(insert_sql_clause)

                        else:

                            if index==len(query_results)-1:
                                    #this for adjusing the installment at end
                                my_kest=outstand_amt_amortized*days_late*(interest_rate/100/360)+outstand_amt_amortized
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                    #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                    #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",   0,     0,     0,    0,  """+str(1*(penalty_amount_calculation*days_late_penalty*penalty_rate))+""",     0,      0,         0,         0) """
                        
                                self.env.cr.execute(insert_sql_clause)

                            else:
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",   0,     0,     0,      0,     """+str(1*(penalty_amount_calculation*days_late_penalty*penalty_rate))+""",     0,      0,         0,         0) """
                        
                                self.env.cr.execute(insert_sql_clause)

                        #Rasti per Chrimson per te tjeret duhet te shikosh
                        #penalty_amount_calculation = my_kest
                        outstand_amt_amortized = outstand_amt_amortized-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))
                        previous_date=schddate
                            

                            #lexo grace period kamata produkt
                        grace_period_days_pen= schddate+timedelta(days=+grace_penalty)                                
                        
                        if end_of_month_date>=grace_period_days_pen:

                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                            ######################           Step IV           ###########################
                            ######################          Pen Grace Date     ###########################
                            ######################     Day of begining penal   ########################### 
                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                        

                            if grace_penalty > 0:    

                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,                              schdid,                                        schddate,  pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                insert_sql_clause += """ values  (           '""" + id_loan + """',12,          '"""+str(grace_period_days_pen) +"""',"""+str(schid)+""",'"""+str(schddate) +"""',   Null,0,0,      0,        0,        0,     0,        0, """+str(1*(penalty_amount_calculation))+""",     0,     0,      0,         0,         0)"""
                                
                                self.env.cr.execute(insert_sql_clause)
                            
                            previous_date=grace_period_days_pen

                            #Date end kamata
                            date_end_pen= schddate+timedelta(days=+30)
                            
                            if end_of_month_date >= date_end_pen:

                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                ######################           Step V            ###########################
                                ######################          Pen Stop Date      ###########################
                                ######################        Penalty Stop Date    ########################### 
                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                    
                                days_late=(date_end_pen-previous_date).days

                           
                                if days_late < 0:
                                    days_late = 0
                                    

                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,                              schdid,                                        schddate,  pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                insert_sql_clause += """ values  (           '""" + id_loan + """',13,          '"""+str(date_end_pen) +"""',"""+str(schid)+""",'"""+str(schddate) +"""',   Null,0,0,      0,        0,      0,     0,        0, """+str(-1*(penalty_amount_calculation))+""",     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                                
                                self.env.cr.execute(insert_sql_clause)

                                previous_date=date_end_pen


                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                ######################           Step II           ###########################
                                ######################      Int,Pen Calculation    ###########################
                                ######################           EOMONTH           ########################### 
                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                    



                                days_late=(end_of_month_date-previous_date).days
                                if days_late < 0:
                                    days_late = 0

                                
                                #200

                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,            prinnotdue,        prindue,intnotdue,intdue,intcap,             intacc,                  penpaid,pencap,                         penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                    
                                insert_sql_clause += """ values  (     '""" + id_loan + """',200,          '"""+str(end_of_month_date) +"""',Null,Null,   Null,0,0,      0,        0,                                            0,     0,        0, 0,     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                                
                                self.env.cr.execute(insert_sql_clause)
                                previous_date=end_of_month_date




                            else:


                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                ######################           Step II           ###########################
                                ######################      Int,Pen Calculation    ###########################
                                ######################           EOMONTH           ########################### 
                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                    



                                days_late=(end_of_month_date-previous_date).days
                                if days_late < 0:
                                    days_late = 0
                                
                                    #200

                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,            prinnotdue,        prindue,intnotdue,intdue,intcap,             intacc,                  penpaid,pencap,                         penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                    #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                    
                                insert_sql_clause += """ values  (     '""" + id_loan + """',200,          '"""+str(end_of_month_date) +"""',Null,Null,   Null,0,0,      0,        0,                                            0,     0,        0, 0,     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                                
                                self.env.cr.execute(insert_sql_clause)
                                previous_date=end_of_month_date


                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                ######################           Step V            ###########################
                                ######################          Pen Stop Date      ###########################
                                ######################        Penalty Stop Date    ########################### 
                                ##############################################################################
                                ##############################################################################
                                ##############################################################################
                                    
                                days_late=(date_end_pen-previous_date).days
                                if days_late < 0:
                                    days_late = 0

                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,                              schdid,                                        schddate,  pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                    #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                insert_sql_clause += """ values  (           '""" + id_loan + """',13,          '"""+str(date_end_pen) +"""',"""+str(schid)+""",'"""+str(schddate) +"""',   Null,0,0,      0,        0,      0,     0,        0, """+str(-1*(penalty_amount_calculation))+""",     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                                
                                self.env.cr.execute(insert_sql_clause)

                                previous_date=date_end_pen


                        else:


                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                            ######################           Step II           ###########################
                            ######################      Int,Pen Calculation    ###########################
                            ######################           EOMONTH           ########################### 
                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                                    


                            days_late=(end_of_month_date-previous_date).days
                            if days_late < 0:
                                days_late = 0
                            
                            #200

                            insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,            prinnotdue,        prindue,intnotdue,intdue,intcap,             intacc,                  penpaid,pencap,                         penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                            #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                
                            insert_sql_clause += """ values  (     '""" + id_loan + """',200,          '"""+str(end_of_month_date) +"""',Null,Null,   Null,0,0,      0,        0,                                            0,     0,        0, 0,     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                          
                            self.env.cr.execute(insert_sql_clause)
                            previous_date=end_of_month_date

                                
                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                            ######################           Step IV           ###########################
                            ######################          Pen Grace Date     ###########################
                            ######################     Day of begining penal   ########################### 
                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                    

                            #lexo grace period kamata produkt
                            grace_period_days_pen= schddate+timedelta(days=+grace_penalty)

                            if grace_penalty > 0:
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,                              schdid,                                        schddate,  pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                insert_sql_clause += """ values  (           '""" + id_loan + """',12,          '"""+str(grace_period_days_pen) +"""',"""+str(schid)+""",'"""+str(schddate) +"""',   Null,0,0,      0,        0,        0,     0,        0, """+str(1*(penalty_amount_calculation))+""",     0,     0,      0,         0,         0)"""
                            
                                self.env.cr.execute(insert_sql_clause)
                            
                            previous_date=grace_period_days_pen

                            #Date end kamata
                            date_end_pen= schddate+timedelta(days=+30)

                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                            ######################           Step V            ###########################
                            ######################          Pen Stop Date      ###########################
                            ######################        Penalty Stop Date    ########################### 
                            ##############################################################################
                            ##############################################################################
                            ##############################################################################
                                
                            days_late=(date_end_pen-previous_date).days
                            if days_late < 0:
                                days_late = 0
                                
                            insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,                              schdid,                                        schddate,  pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                            #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                            insert_sql_clause += """ values  (           '""" + id_loan + """',13,          '"""+str(date_end_pen) +"""',"""+str(schid)+""",'"""+str(schddate) +"""',   Null,0,0,      0,        0,      0,     0,        0, """+str(-1*(penalty_amount_calculation))+""",     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                        
                            self.env.cr.execute(insert_sql_clause)
                            previous_date=date_end_pen

                    else:

                        ##############################################################################
                        ############ if EOMONTH lower then Schdate             #######################
                        ##############################################################################


                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                        ######################           Step II           ###########################
                        ######################      Int,Pen Calculation    ###########################
                        ######################           EOMONTH           ########################### 
                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                                


                        days_late=(end_of_month_date-previous_date).days
                        if days_late < 0:
                            days_late = 0
                        
                        #200

                        insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,            prinnotdue,        prindue,intnotdue,intdue,intcap,             intacc,                  penpaid,pencap,                         penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                        #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                
                        insert_sql_clause += """ values  (     '""" + id_loan + """',200,          '"""+str(end_of_month_date) +"""',Null,Null,   Null,0,0,      0,        0,                                            0,     0,        0, 0,     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                          
                        self.env.cr.execute(insert_sql_clause)
                        previous_date=end_of_month_date

                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                        ######################           Step III          ###########################
                        ######################          Schedule Part      ###########################
                        ##############################################################################
                        ##############################################################################
                        ##############################################################################



                        #4
                        # the installment of first schedule is saved
                        
                        
                        days_late=(schddate-previous_date).days
                        if days_late < 0:
                            days_late = 0
                        
                        #360 days configuration    
                        days_late=30

                        days_late_penalty = (schddate-previous_date).days
                        if days_late_penalty < 0:
                            days_late_penalty = 0


                        if grace_penalty == 0:
                            if index==len(query_results)-1:
                                #this for adjusing the installment at end
                                #rasti per crimson per te tjeret duhet ndryshohet
                                #penalty_amount_calculation = my_kest
                                my_kest=outstand_amt_amortized*days_late*(interest_rate/100/360)+outstand_amt_amortized
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",   0,     0,     0,      """+str(1*(penalty_amount_calculation))+""",   0,     0,      0,         0,         0) """
                    
                                self.env.cr.execute(insert_sql_clause)

                            else:
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",   0,     0,    0,     """+str(1*(penalty_amount_calculation))+""",  0,     0,      0,         0,         0) """
                    
                                self.env.cr.execute(insert_sql_clause)
                        else:

                            if index==len(query_results)-1:
                                #this for adjusing the installment at end
                                my_kest=outstand_amt_amortized*days_late*(interest_rate/100/360)+outstand_amt_amortized
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",   0,     0,     0,  0,     """+str(1*(penalty_amount_calculation*days_late_penalty*penalty_rate))+""",         0,      0,         0,         0) """
                    
                                self.env.cr.execute(insert_sql_clause)

                            else:
                                insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                                #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                                #insert_sql_clause += """ values  (     '0000018',4,          '"""+schddate +"""',"""+str(schid)+""",'"""+schddate+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""","""+str(my_kest-outstand_amt_amortized*days_late*0.000416666666666667)+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*0.000416666666666667))+""", """+str(+1*(outstand_amt_amortized*days_late*0.000416666666666667))+""",   """+str(-1*(my_kest-outstand_amt_amortized*days_late*0.000416666666666667))+""",     0,     0,      0,     0,     0,      0,         0,         0) """
                                insert_sql_clause += """ values  (     '""" + id_loan + """',4,          '"""+str(schddate) +"""',"""+str(schid)+""",'"""+str(schddate)+"""',   Null,"""+str(-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360)))+""","""+str(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))+"""  ,  """+str(-1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""", """+str(+1*(outstand_amt_amortized*days_late*(interest_rate/100/360)))+""",   0,     0,     0,      0,     """+str(1*(penalty_amount_calculation*days_late_penalty*penalty_rate))+""",     0,      0,         0,         0) """
                    
                                self.env.cr.execute(insert_sql_clause)

                        #rasti per crimson per te tjeret duhet ndryshohet
                        #penalty_amount_calculation = my_kest
                        outstand_amt_amortized = outstand_amt_amortized-1*(my_kest-outstand_amt_amortized*days_late*(interest_rate/100/360))
                        previous_date=schddate
                        


                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                        ######################           Step IV           ###########################
                        ######################          Pen Grace Date     ###########################
                        ######################     Day of begining penal   ########################### 
                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                    

                        #lexo grace period kamata produkt
                        grace_period_days_pen= schddate+timedelta(days=+grace_penalty)

                        if grace_penalty > 0:
                            insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,                              schdid,                                        schddate,  pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                            #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                            insert_sql_clause += """ values  (           '""" + id_loan + """',12,          '"""+str(grace_period_days_pen) +"""',"""+str(schid)+""",'"""+str(schddate) +"""',   Null,0,0,      0,        0,        0,     0,        0, """+str(1*(penalty_amount_calculation))+""",     0,     0,      0,         0,         0)"""
                            
                            self.env.cr.execute(insert_sql_clause)
                        
                        previous_date=grace_period_days_pen

                        #Date end kamata
                        date_end_pen= schddate+timedelta(days=+30)

                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                        ######################           Step V            ###########################
                        ######################          Pen Stop Date      ###########################
                        ######################        Penalty Stop Date    ########################### 
                        ##############################################################################
                        ##############################################################################
                        ##############################################################################
                                
                        days_late=(date_end_pen-previous_date).days
                        if days_late < 0:
                            days_late = 0
                                
                        insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,                              schdid,                                        schddate,  pmtid,                          prinnotdue,                                            prindue,                                                                  intnotdue,                                                      intdue,                                               intcap,             intacc,                  penpaid,pencap,                  penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                            #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                        insert_sql_clause += """ values  (           '""" + id_loan + """',13,          '"""+str(date_end_pen) +"""',"""+str(schid)+""",'"""+str(schddate) +"""',   Null,0,0,      0,        0,      0,     0,        0, """+str(-1*(penalty_amount_calculation))+""",     """+str(1*(penalty_amount_calculation*days_late*penalty_rate))+""",     0,      0,         0,         0)"""
                        
                        self.env.cr.execute(insert_sql_clause)
                        previous_date=date_end_pen

                    print "-----End-----"



                    #removed this line code --------------end_of_month_date= date_end_pen.replace(day=1) 
                    #removed this line code --------------select_sql_clause = """SELECT count(*) as count_number_record from loan_payments where loanid='""" + id_loan + """' and transtypeid=200 and transdate='"""+str(end_of_month_date) +"""'"""   
                    #removed this line code --------------self.env.cr.execute(select_sql_clause)
                    #removed this line code --------------query_results = self.env.cr.dictfetchall()
                    #removed this line code --------------#print query_results
                    #removed this line code --------------#move tab down to troubleshoot
                    #removed this line code --------------if query_results[0].get('count_number_record') ==0:
                    #removed this line code --------------insert_sql_clause = """insert  into loan_payments (loanid,transtypeid,transdate,               schdid,        schddate,pmtid,            prinnotdue,        prindue,intnotdue,intdue,intcap,             intacc,                  penpaid,pencap,                         penacc, feesdue,ovdintpaid,ovdintcap,ovdintacc)  """
                    #insert_sql_clause += """ values  (     'LOAN000001',1,          '"""+str(self.bank_date) +"""',"""+str(query_results[0].get('id'))+""",Null,   """+str(self.id)+""","""+str(self.amount)+""",0,      0,        0,     """+str(self.amount)+""",     0,     0,      0,     0,     0,      0,         0,         0)"""
                    #removed this line code --------------insert_sql_clause += """ values  (     '""" + id_loan + """',200,          '"""+str(end_of_month_date) +"""',"""+str(schid)+""",Null,   Null,0,0,      0,        0,                                            0,     0,        0, 0,     0,     0,      0,         0,         0)"""
                    #removed this line code --------------self.env.cr.execute(insert_sql_clause)


        query = ''
        #select_sql_clause = """insert into loan_payments_tmp select * from loan_payments where """
        #query += ""+select_sql_clause+" schedule_id ='t100'"
        #self.env.cr.execute(query)

        ##############################################################################
        ##############################################################################
        ##############################################################################
        ######################           Step VI           ###########################
        ######################   Calculation of IntAcc     ###########################
        ######################                             ########################### 
        ##############################################################################
        ##############################################################################
        ##############################################################################



        select_sql_clause = """select sum(prinnotdue + prindue) as outstanding from loan_payments where """
        query += ""+select_sql_clause+" loanid ='" + id_loan + "' and  transtypeid<>4 "
        self.env.cr.execute(query)
        query_results = self.env.cr.dictfetchall()
        outstand_amt_amortized=0
        if query_results[0].get('outstanding') >=0:
            outstand_amt_amortized=query_results[0].get('outstanding')
        
        query = ''
        select_sql_clause = """select max(transdate) as max_date from loan_payments where """
        query += ""+select_sql_clause+" loanid ='" + id_loan + "' and  transtypeid=1 "
        self.env.cr.execute(query)
        query_results = self.env.cr.dictfetchall()
        max_date='1900-01-01'
        if query_results[0].get('max_date') !=None:
            max_date=dateutil.parser.parse(query_results[0].get('max_date')).date()
        
        query = ''
        if max_date=='1900-01-01':
            select_sql_clause = """select min(transdate) as max_date from loan_payments where """
            query += ""+select_sql_clause+" loanid ='" + id_loan + "' and  transtypeid=1"
            self.env.cr.execute(query)
            query_results = self.env.cr.dictfetchall()
            if query_results[0].get('max_date') !=None:
                max_date=dateutil.parser.parse(query_results[0].get('max_date')).date()

        total_interes=0.0000
        min_date_360_calculation='1900-01-01'
        max_date_360_calculation='1900-01-01'

        query = ''
        select_sql_clause = """select sum(IntDue) as total_interes from loan_payments where """
        query += ""+select_sql_clause+" loanid ='" + id_loan + "' and  transtypeid=4 and  (prinnotdue<> 0 or prindue <> 0)"
        self.env.cr.execute(query)
        query_results = self.env.cr.dictfetchall()
        if query_results[0].get('total_interes') !=None:
            total_interes=query_results[0].get('total_interes')
        


        
        query = ''
        select_sql_clause = """select min(transdate) as min_date_360_calculation from loan_payments where """
        query += ""+select_sql_clause+" loanid ='" + id_loan + "' and  transtypeid=1 and  prinnotdue<> 0"
        self.env.cr.execute(query)
        query_results = self.env.cr.dictfetchall()
        if query_results[0].get('min_date_360_calculation') !=None:
            min_date_360_calculation=dateutil.parser.parse(query_results[0].get('min_date_360_calculation')).date() 

        query = ''
        select_sql_clause = """select max(transdate) as max_date_360_calculation from loan_payments where """
        query += ""+select_sql_clause+" loanid ='" + id_loan + "' and  transtypeid=4 "
        self.env.cr.execute(query)
        query_results = self.env.cr.dictfetchall()
        if query_results[0].get('max_date_360_calculation') !=None:
            max_date_360_calculation=dateutil.parser.parse(query_results[0].get('max_date_360_calculation')).date() 

       
        days_diff_360=(max_date_360_calculation-min_date_360_calculation).days
        if days_diff_360 == 0:
            days_diff_360 = 1

        #ne rastet me kalkulim ditor kjo me poshte
            #select_sql_clause = """SELECT id,transtypeid,transdate,prinnotdue from loan_payments where loanid ='0000018'  and transdate>='"""+ str(dateutil.parser.parse(max_date).date()) + """' order by transdate,transtypeid"""
        #ne rastet me kalkulim mujor kjo me poshte
        #select_sql_clause = """SELECT id,transtypeid,transdate,prinnotdue from loan_payments where transtypeid =200 and loanid ='""" + id_loan + """'  and transdate>='"""+ str(max_date) + """' order by transdate,transtypeid"""    
        select_sql_clause = """SELECT id,transtypeid,transdate,prinnotdue from loan_payments where transtypeid =200 and loanid ='""" + id_loan + """' order by transdate,transtypeid"""    
        
        self.env.cr.execute(select_sql_clause)
        query_results = self.env.cr.dictfetchall()
       
        for index in range(0, len(query_results)):
            if query_results[index].get('id') != None:
                if query_results[index].get('id') != None:
                    payments_id=query_results[index].get('id') 
                else:
                    payments_id='Null'

                if query_results[index].get('transtypeid') != None:
                    transtypeid=query_results[index].get('transtypeid')
                else:
                    transtypeid='Null'

                if query_results[index].get('transdate') != None:
                    record_date=dateutil.parser.parse(query_results[index].get('transdate')).date()
                else:
                    record_date='Null'

                if query_results[index].get('prinnotdue') != None:
                    prinnotdue=query_results[index].get('prinnotdue')
                else:
                    prinnotdue='Null'

                #per rastet me inters days calculation
                #days_diff=(dateutil.parser.parse(record_date).date()-dateutil.parser.parse(max_date).date()).days
                #print days_diff,outstand_amt_amortized*days_diff*0.000403225806451613,outstand_amt_amortized
                #update_sql_clause = """update loan_payments set intacc=""" +str(outstand_amt_amortized*days_diff*0.000403225806451613) + """ where id = """ +str(payments_id)+ """  """
                #print update_sql_clause
                #self.env.cr.execute(update_sql_clause)

                #max_date=record_date

                #if transtypeid==4:
                    
                    #outstand_amt_amortized=outstand_amt_amortized+prinnotdue

                #Per rastin ASFund and Chrimson
                days_diff=(record_date-max_date).days

                if index == 0:
                    remember_this_value=total_interes/days_diff_360*days_diff
                if index == len(query_results)-1:
                    update_sql_clause = """update loan_payments set intacc=""" +str(total_interes/days_diff_360*days_diff-remember_this_value) + """ where id = """ +str(payments_id)+ """  """
                else:
                    update_sql_clause = """update loan_payments set intacc=""" +str(total_interes/days_diff_360*days_diff) + """ where id = """ +str(payments_id)+ """  """

                self.env.cr.execute(update_sql_clause)

                max_date=record_date

                if transtypeid==4:
                    
                    outstand_amt_amortized=outstand_amt_amortized+prinnotdue

        ##############################################################################
        ##############################################################################
        ##############################################################################
        ######################           Step VII          ###########################
        ######################   Calculation of PenAcc     ###########################
        ######################                             ########################### 
        ##############################################################################
        ##############################################################################
        ##############################################################################






        return 1

#================================================================================
class LoanPayments (models.Model):
    _name='loan.payments'

    
    loanid =fields.Char(string='Identifies loan from Loan table')
    transtypeid=fields.Integer(string='Identifies type of transaction from TransSubType table')
    transdate=fields.Date (string='Date of transaction')
    schdid=fields.Integer (string='Identifies scheduled transaction in Loan Schedule')
    schddate=fields.Date (string='Scheduled  Date to which transaction applies')
    pmtid=fields.Integer (string='Identifies Payment from Pmt table')
    prinnotdue=fields.Float (string='Principal not yet due as of transaction date')
    prindue=fields.Float (string='Principal due or overdue as of transaction date')
    intnotdue=fields.Float (string='Interest not yet due as of transaction date')
    intdue=fields.Float (string='Interest due or overdue as of transaction date')
    intcap=fields.Float (string='Capital on which interest accrues')
    intacc=fields.Float (string='Accrued Interest')
    penpaid=fields.Float (string='Penalties paid during transaction')
    pencap=fields.Float (string='Capital on which penalties accrue')
    penacc=fields.Float (string='Accrued Penalties')
    feesdue=fields.Float (string='Fees due or overdue as of transaction date')
    ovdintpaid =fields.Float (string='Overdue Interest paid during transaction')
    ovdintcap=fields.Float (string='Capital on which Overdue Interest accrues')
    ovdintacc=fields.Float (string='Overdue accrued Interest')

class LoanTrans (models.Model):
    _name='loan.trans'

    LoanID=fields.Char(string='Identifies loan from the Loan table')


    TransTypeID=fields.Integer(string='Identifies type of transaction from TransSubType table')
    PmtDate=fields.Datetime (string='Date repayment is received')
    
    PmtCode=fields.Char (string='Check number, receipt number, etc')
    PmtAmt=fields.Float (string='Repayment amount in payment currency (usually local currency)')
    IdxAmt=fields.Float (string='Repayment amount in index currency (rounded according to calculation methodology')
    BankDate=fields.Datetime (string='Date repayment is processed (i.e. by bank)')
    fund_src=fields.Char (string='Funding Source')
    

# =============to add fields from account payment to account move line=============
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    receipt_no = fields.Char(string='Receipt No.')
    loan_no = fields.Char(string='Loan No.')
    bank_date = fields.Date(string='Bank Date')
    trans_type = fields.Selection([('1','Disbursement'),
                                    ('2','Additional Disb.'),
                                    ('4','Scheduled Payment'),
                                    ('5','Repayment'),
                                    ('6','Buy Down'),
                                    ('7','Penalty Writeoff'),
                                    ('8','Interest Writeoff'),
                                    ('9','Total Writeoff'),
                                    ('10','Rescheduling'),
                                    ('12','Grace Period'),
                                    ('13','Penalty Stop'),
                                    ('14','Penalty Charge'),
                                    ('15','Overdue Int Writeoff'),
                                    ('16','Returned Principal'),
                                    ('17','Transfer In'),
                                    ('18','Transfer Out'),
                                    ('19','Recov Pen Pmt'),
                                    ('20','Recov Pen Rev'),
                                    ('21','Future Interest Writeoff'),
                                    ('90','Cash Over'),
                                    ('91','Cash Short'),
                                    ('92','Recovery'),
                                    ('101','Deposit'),
                                    ('105','Withdrawal'),
                                    ('109','Forfeit'),
                                    ('117','Transfer In Dpst'),
                                    ('118','Transfer Out Dpst'),
                                    ('120','IntPost'),
                                    ('121','TaxPost'),
                                    ('191','Cash Over Dpst'),
                                    ('200','Accrual')
                                   ],string='Transaction Type')
    fund_src = fields.Char(string='Funding Source')
    
    """@api.model
    def create(self, vals):
        #### :context's key apply_taxes: set to True if you want vals['tax_ids'] to result in the creation of move lines for taxes and eventual
        ####        adjustment of the line amount (in case of a tax included in price).

        ####:context's key `check_move_validity`: check data consistency after move line creation. Eg. set to false to disable verification that the move
        ####        debit-credit == 0 while creating the move lines composing the move.

        
        context = dict(self._context or {})
        amount = vals.get('debit', 0.0) - vals.get('credit', 0.0)
        if not vals.get('partner_id') and context.get('partner_id'):
            vals['partner_id'] = context.get('partner_id')
        move = self.env['account.move'].browse(vals['move_id'])
        account = self.env['account.account'].browse(vals['account_id'])
        if account.deprecated:
            raise UserError(_('You cannot use deprecated account.'))
        if 'journal_id' in vals and vals['journal_id']:
            context['journal_id'] = vals['journal_id']
        # ======================newly added=========================
        # print 'self======================',self
        # ggg
        if 'receipt_no' in vals and vals['receipt_no']:
            context['receipt_no'] = vals['receipt_no']
        if 'loan_no' in vals and vals['loan_no']:
            context['loan_no'] = vals['loan_no']
        if 'bank_date' in vals and vals['bank_date']:
            context['bank_date'] = vals['bank_date']
        if 'fund_src' in vals and vals['fund_src']:
            context['fund_src'] = vals['fund_src']
        

        # ============================================================
        if 'date' in vals and vals['date']:
            context['date'] = vals['date']
        if 'journal_id' not in context:
            context['journal_id'] = move.journal_id.id
            context['date'] = move.date
        #we need to treat the case where a value is given in the context for period_id as a string
        if not context.get('journal_id', False) and context.get('search_default_journal_id', False):
            context['journal_id'] = context.get('search_default_journal_id')
        if 'date' not in context:
            context['date'] = fields.Date.context_today(self)

        journal = vals.get('journal_id') and self.env['account.journal'].browse(vals['journal_id']) or move.journal_id
        vals['date_maturity'] = vals.get('date_maturity') or vals.get('date') or move.date
        ok = not (journal.type_control_ids or journal.account_control_ids)
        print 'vals===============newly added=================', vals
        _logger.info('=====================vals newly added  %s======================' % vals)
        # gggggg
        if journal.type_control_ids:
            type = account.user_type_id
            for t in journal.type_control_ids:
                if type == t:
                    ok = True
                    break
        if journal.account_control_ids and not ok:
            for a in journal.account_control_ids:
                if a.id == vals['account_id']:
                    ok = True
                    break
        # Automatically convert in the account's secondary currency if there is one and
        # the provided values were not already multi-currency
        if account.currency_id and 'amount_currency' not in vals and account.currency_id.id != account.company_id.currency_id.id:
            vals['currency_id'] = account.currency_id.id
            ctx = {}
            if 'date' in vals:
                ctx['date'] = vals['date']
            vals['amount_currency'] = account.company_id.currency_id.with_context(ctx).compute(amount, account.currency_id)

        if not ok:
            raise UserError(_('You cannot use this general account in this journal, check the tab \'Entry Controls\' on the related journal.'))

        # Create tax lines
        tax_lines_vals = []
        if context.get('apply_taxes') and vals.get('tax_ids'):
            # Get ids from triplets : https://www.odoo.com/documentation/master/reference/orm.html#openerp.models.Model.write
            tax_ids = [tax['id'] for tax in self.resolve_2many_commands('tax_ids', vals['tax_ids']) if tax.get('id')]
            # Since create() receives ids instead of recordset, let's just use the old-api bridge
            taxes = self.env['account.tax'].browse(tax_ids)
            currency = self.env['res.currency'].browse(vals.get('currency_id'))
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            res = taxes.with_context(round=True).compute_all(amount,
                currency, 1, vals.get('product_id'), partner)
            # Adjust line amount if any tax is price_include
            if abs(res['total_excluded']) < abs(amount):
                if vals['debit'] != 0.0: vals['debit'] = res['total_excluded']
                if vals['credit'] != 0.0: vals['credit'] = -res['total_excluded']
                if vals.get('amount_currency'):
                    vals['amount_currency'] = self.env['res.currency'].browse(vals['currency_id']).round(vals['amount_currency'] * (res['total_excluded']/amount))
            # Create tax lines
            for tax_vals in res['taxes']:
                if tax_vals['amount']:
                    account_id = (amount > 0 and tax_vals['account_id'] or tax_vals['refund_account_id'])
                    if not account_id: account_id = vals['account_id']
                    temp = {
                        'account_id': account_id,
                        'name': vals['name'] + ' ' + tax_vals['name'],
                        'tax_line_id': tax_vals['id'],
                        'move_id': vals['move_id'],
                        'partner_id': vals.get('partner_id'),
                        'statement_id': vals.get('statement_id'),
                        'debit': tax_vals['amount'] > 0 and tax_vals['amount'] or 0.0,
                        'credit': tax_vals['amount'] < 0 and -tax_vals['amount'] or 0.0,
                    }
                    bank = self.env["account.bank.statement"].browse(vals.get('statement_id'))
                    if bank.currency_id != bank.company_id.currency_id:
                        ctx = {}
                        if 'date' in vals:
                            ctx['date'] = vals['date']
                        temp['currency_id'] = bank.currency_id.id
                        temp['amount_currency'] = bank.company_id.currency_id.with_context(ctx).compute(tax_vals['amount'], bank.currency_id, round=True)
                    tax_lines_vals.append(temp)
        print 'vals=====================================',vals
        _logger.info('=====================vals  latest %s======================' % vals)
        # mmmmmmm
        new_line = super(AccountMoveLine, self).create(vals)
        print 'new_line=========================================',new_line
        _logger.info('=====================new_line  %s======================' % new_line)
        for tax_line_vals in tax_lines_vals:
            # TODO: remove .with_context(context) once this context nonsense is solved
            self.with_context(context).create(tax_line_vals)

        if self._context.get('check_move_validity', True):
            move.with_context(context)._post_validate()

        return new_line



#================================================================================

# =============to add fields from account payment to account move line=============
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    receipt_no = fields.Char(string='Receipt No.')
    loan_no = fields.Char(string='Loan No.')
    bank_date = fields.Date(string='Bank Date')
    trans_type = fields.Selection([('repay','Repayment'),('pen_write','Penalty Writeoff'),
                                   ('int_write','Interesr Writeoff'),('total_write','Total Writeoff'),
                                   ('pen_charge','Penalty Charge'),('ov_int_write','Overdue Int Writeoff'),
                                   ('ret_pri','Returned Principal'),('trans_out','Transfer Out'),
                                   ('pen_trans_pmt','Penalty Transfer Payment'),('fut_int_write','Future Interest Writeoff'),
                                   ('cash_over','Cash Over'),('cash_short','Cash Short'),
                                   ],string='Transaction Type')
    fund_src = fields.Char(string='Funding Source')

    @api.model
    def create(self, vals):

        context = dict(self._context or {})
        amount = vals.get('debit', 0.0) - vals.get('credit', 0.0)
        if not vals.get('partner_id') and context.get('partner_id'):
            vals['partner_id'] = context.get('partner_id')
        move = self.env['account.move'].browse(vals['move_id'])
        account = self.env['account.account'].browse(vals['account_id'])
        if account.deprecated:
            raise UserError(_('You cannot use deprecated account.'))
        if 'journal_id' in vals and vals['journal_id']:
            context['journal_id'] = vals['journal_id']
        # ======================newly added=========================
        if 'receipt_no' in vals and vals['receipt_no']:
            context['receipt_no'] = vals['receipt_no']
        if 'loan_no' in vals and vals['loan_no']:
            context['loan_no'] = vals['loan_no']
        if 'bank_date' in vals and vals['bank_date']:
            context['bank_date'] = vals['bank_date']
        if 'fund_src' in vals and vals['fund_src']:
            context['fund_src'] = vals['fund_src']


        # ============================================================
        if 'date' in vals and vals['date']:
            context['date'] = vals['date']
        if 'journal_id' not in context:
            context['journal_id'] = move.journal_id.id
            context['date'] = move.date
        #we need to treat the case where a value is given in the context for period_id as a string
        if not context.get('journal_id', False) and context.get('search_default_journal_id', False):
            context['journal_id'] = context.get('search_default_journal_id')
        if 'date' not in context:
            context['date'] = fields.Date.context_today(self)

        journal = vals.get('journal_id') and self.env['account.journal'].browse(vals['journal_id']) or move.journal_id
        vals['date_maturity'] = vals.get('date_maturity') or vals.get('date') or move.date
        ok = not (journal.type_control_ids or journal.account_control_ids)
        print 'vals===============newly added=================', vals
        _logger.info('=====================vals newly added  %s======================' % vals)
        # gggggg
        if journal.type_control_ids:
            type = account.user_type_id
            for t in journal.type_control_ids:
                if type == t:
                    ok = True
                    break
        if journal.account_control_ids and not ok:
            for a in journal.account_control_ids:
                if a.id == vals['account_id']:
                    ok = True
                    break
        # Automatically convert in the account's secondary currency if there is one and
        # the provided values were not already multi-currency
        if account.currency_id and 'amount_currency' not in vals and account.currency_id.id != account.company_id.currency_id.id:
            vals['currency_id'] = account.currency_id.id
            ctx = {}
            if 'date' in vals:
                ctx['date'] = vals['date']
            vals['amount_currency'] = account.company_id.currency_id.with_context(ctx).compute(amount, account.currency_id)

        if not ok:
            raise UserError(_('You cannot use this general account in this journal, check the tab \'Entry Controls\' on the related journal.'))

        # Create tax lines
        tax_lines_vals = []
        if context.get('apply_taxes') and vals.get('tax_ids'):
            # Get ids from triplets : https://www.odoo.com/documentation/master/reference/orm.html#openerp.models.Model.write
            tax_ids = [tax['id'] for tax in self.resolve_2many_commands('tax_ids', vals['tax_ids']) if tax.get('id')]
            # Since create() receives ids instead of recordset, let's just use the old-api bridge
            taxes = self.env['account.tax'].browse(tax_ids)
            currency = self.env['res.currency'].browse(vals.get('currency_id'))
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            res = taxes.with_context(round=True).compute_all(amount,
                currency, 1, vals.get('product_id'), partner)
            # Adjust line amount if any tax is price_include
            if abs(res['total_excluded']) < abs(amount):
                if vals['debit'] != 0.0: vals['debit'] = res['total_excluded']
                if vals['credit'] != 0.0: vals['credit'] = -res['total_excluded']
                if vals.get('amount_currency'):
                    vals['amount_currency'] = self.env['res.currency'].browse(vals['currency_id']).round(vals['amount_currency'] * (res['total_excluded']/amount))
            # Create tax lines
            for tax_vals in res['taxes']:
                if tax_vals['amount']:
                    account_id = (amount > 0 and tax_vals['account_id'] or tax_vals['refund_account_id'])
                    if not account_id: account_id = vals['account_id']
                    temp = {
                        'account_id': account_id,
                        'name': vals['name'] + ' ' + tax_vals['name'],
                        'tax_line_id': tax_vals['id'],
                        'move_id': vals['move_id'],
                        'partner_id': vals.get('partner_id'),
                        'statement_id': vals.get('statement_id'),
                        'debit': tax_vals['amount'] > 0 and tax_vals['amount'] or 0.0,
                        'credit': tax_vals['amount'] < 0 and -tax_vals['amount'] or 0.0,
                    }
                    bank = self.env["account.bank.statement"].browse(vals.get('statement_id'))
                    if bank.currency_id != bank.company_id.currency_id:
                        ctx = {}
                        if 'date' in vals:
                            ctx['date'] = vals['date']
                        temp['currency_id'] = bank.currency_id.id
                        temp['amount_currency'] = bank.company_id.currency_id.with_context(ctx).compute(tax_vals['amount'], bank.currency_id, round=True)
                    tax_lines_vals.append(temp)
        _logger.info('=====================vals  latest %s======================' % vals)
        new_line = super(AccountMoveLine, self).create(vals)
        _logger.info('=====================new_line  %s======================' % new_line)
        for tax_line_vals in tax_lines_vals:
            # TODO: remove .with_context(context) once this context nonsense is solved
            self.with_context(context).create(tax_line_vals)

        if self._context.get('check_move_validity', True):
            move.with_context(context)._post_validate()

        return new_line
"""

# ==============================================================================
# ===========================for product code menu in administration===================
class product_code(models.Model):
    _name = "product.code"

    name = fields.Char(string='Code')
    quote_rate = fields.Float(string='Quoted Int Rate')
    daily_rate = fields.Float(string='Daily Interest Rate')

    # calc_meth =fields.Char(string='Calculation Meth')
    calc_meth =fields.Many2one('calculation.meth',string='Calculation Meth')
    index_curr = fields.Many2one('res.currency',string='Index Currency')
    pay_curr = fields.Many2one('res.currency',string='Payment Currency')

    # sch_type = fields.Char(string='Schedule Type')
    sch_type = fields.Many2one('schedule.type',string='Schedule Type')
    # term_length = fields.Char(string='Term Length')
    term_length = fields.Many2one('term.length',string='Term Length')
    # pay_day = fields.Char(string='Payment Day')
    pay_day = fields.Many2one('payment.day',string='Payment Day')
    # rounding = fields.Char(string='Rounding')
    rounding = fields.Many2one('rounding',string='Rounding')


    proc_fees = fields.Float(string='Processing Fee')
    grace_per = fields.Integer(string='Grace Period')

#     ===================newly added===================
    daily_pen_rate = fields.Float(string='Daily Penalty Rate')
    pen_grace_per = fields.Integer(string='Penalty grace per')
    max_pen_days = fields.Integer(string='Max Penalty Days')
    grace_penalty = fields.Float(string='Grace Penalty')

    loan_resch = fields.Boolean(string='Loan Rescheduled')
    locked = fields.Boolean(string='Locked')

#     ===============for controls tab=======================
    min_loan_amt = fields.Float(string='Min Loan Amt')
    max_loan_amt = fields.Float(string='Max Loan Amt')
    loan_amt_con = fields.Many2one('loan.amt.control',string='Loan Amt Control')

    min_open_date = fields.Date(string='Min Open Date')
    max_open_date = fields.Date(string='Max Open Date')

    min_int_rate = fields.Float(string='Min Int Rate')
    max_int_rate = fields.Float(string='Max Int Rate')

    lindur_ne = fields.Char(string='Lindur ne')
    nr_acct_allowed = fields.Integer(string='No. Accts Allowed')
    credit_line_meth = fields.Selection([('limit','Limit Total Disb')],string='Credit Line Meth')


#     ================for authorize tab=======================
    auth1 = fields.Many2one('res.users',string='Authorization 1')
    auth2 = fields.Many2one('res.users',string='Authorization 2')
    auth3 = fields.Many2one('res.users',string='Authorization 3')

class clac_meth(models.Model):
    _name = 'calculation.meth'
    name  = fields.Integer(string='Meth Code')
    desc  = fields.Text(string='Description')

class schedule_type(models.Model):
    _name = 'schedule.type'
    name  = fields.Char(string='Name')
    desc  = fields.Text(string='Description')

class term_length(models.Model):
    _name = 'term.length'
    name  = fields.Char(string='Name')
    desc  = fields.Text(string='Description')

class rounding(models.Model):
    _name = 'rounding'
    name  = fields.Char(string='Name')
    desc  = fields.Text(string='Description')


class payment_day(models.Model):
    _name = 'payment.day'
    name  = fields.Char(string='Name')
    desc  = fields.Text(string='Description')

class loan_amt_control(models.Model):
    _name = 'loan.amt.control'
    name  = fields.Char(string='Name')
    desc  = fields.Text(string='Description')
class management_funds(models.Model):
    _name = 'management.funds'

    mf_donor = fields.Many2one('res.partner',string='Donor')
    mf_date =fields.Date(string='Date')
    mf_status = fields.Char(string='Status')

    branch = fields.Many2one('admin.branch', string='Branch', required=True)

    sub_branch = fields.Many2one('admin.sub.branch', string='Sub Branch', required=True)
    officer_id = fields.Many2one('res.partner', string='Officer')

    appln_no = fields.Char(string='Application Number')
    office = fields.Char(string='Office')
    customer_acc_id = fields.Char(string='Customer Account Id', required=True)
    s_name = fields.Char(string='Short Name')
    last_name = fields.Char(string='Last Name')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    birthdate = fields.Date('Date Of Birth', )
    reg_date = fields.Date('Date Of Registration')
    country_birth = fields.Many2one('res.country', string='Country Of Birth')

    city_birth = fields.Many2one('admin.city', string='City Of Birth')
    fin_currency = fields.Many2one('res.currency', string='Financial Currency')
    cust_category = fields.Selection([('categ1', 'Category 1'), ('categ2', 'Category 2')], string='Customer Caegory')
    accnt_no = fields.Char('Account Number')
    accnt_class = fields.Char('Account Class')

    country = fields.Many2one('res.country', string='Country', required=True)

    country_issuer = fields.Many2one('res.country', string='Country Issuer', )
    natinality = fields.Many2one('res.nationality', string='Nationality')
    language = fields.Char(string='Language')
    mobile_no = fields.Char(string='Mobile No.')
    landline_no = fields.Char(string='Landline No.')
    office_no = fields.Char(string='Office No.')
    fax_no = fields.Char(string='Fax ')
    email = fields.Char(string='Email')

    city_issued = fields.Many2one('admin.city', string='City Issued', )

    passport_no = fields.Char(string='ID Number', )
    pas_issue_date = fields.Date('Issue Date', )
    pas_exp_date = fields.Date('Expiry Date', )

    type_of_id1 = fields.Selection(
        [('certificate', 'Certificate'), ('identity', 'Identification Card / Biometric Password'),
         ('identity_card', 'Identity Card'), ('passport', 'Passport'), ('license', 'Driving License')],
        string="Type Of ID")
    marital_status = fields.Selection([('married', 'Married'), ('unmarried', 'Unmarried'), ('divorcee', 'Divorcee')],
                                      string='Marital Status')

    education = fields.Selection([('year', '8-year'), ('primary', 'PRIMARY'),
                                  ('up', 'UP'), ('medium', 'MEDIUM'), ('univer_satar', 'AFTER UNIVERSATAR')],
                                 string='Education:', )
    exp = fields.Char(string='Experience', )

    social_sit = fields.Selection([('ambulant', 'AMBULANT'), ('without_job', 'WITHOUT JOB'),
                                   ('private_with_license', 'PRIVATE WITH LICENSE'),
                                   ('private_without_license', 'PRIVATE WITHOUT LICENSE'),
                                   ('employed', 'EMPLOYED')], string='Social situations:', )
    currency_fin = fields.Many2one('res.currency', string='Financing Currency',
                                   help='Utility field to express amount currency')
    financing_amt = fields.Float(string='Financing Amount')
    interest_rate = fields.Float(string='Interest Rate(%)')
    rate_code = fields.Char(string='Rate Code', )
    spread = fields.Char(string='Spread', )
    cl_acc_no = fields.Char(string='CL Account No.', )
    ins_start_date = fields.Date('Installment Start Date', )
    effect_rate = fields.Integer(string='Effective Rate(%)')

    grace = fields.Char(string='Grace', )


    # c_name = fields.Char(string='Name')
    # c_father_name = fields.Char(string="Father's Name")
    # c_last_name = fields.Char(string='Last Name')
    # c_date = fields.Date('Date', required=True)








