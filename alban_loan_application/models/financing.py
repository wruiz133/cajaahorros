from odoo import models, fields, api
import datetime
import math
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import dateutil.parser
import logging

_logger = logging.getLogger(__name__)

class loan_application(models.Model):
    _inherit = "loan.application"

    currency_fin = fields.Many2one('res.currency',string='Financing Currency', help='Utility field to express amount currency')
    financing_amt = fields.Float(string='Financing Amount')
    interest_rate = fields.Float(string='Interest Rate(%)')
    rate_code = fields.Char(string='Rate Code', )
    spread = fields.Char(string='Spread', )
    cl_acc_no = fields.Char(string='CL Account No.', )
    ins_start_date = fields.Date('Installment Start Date', )
    effect_rate = fields.Integer(string='Effective Rate(%)')

    grace = fields.Integer(string='Grace', )
    install_count = fields.Integer(string='No. Of Installments ')
    unit_fin  = fields.Selection([('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
                      ('half_yearly', 'Half Yearly'), ('yearly', 'Yearly')], string='Unit')
    freq_fin  = fields.Char(string='Frequency')

    do_pay_amt_fin = fields.Float(string="Down Payment Amount")
    do_pay_rate = fields.Integer(string="Down Payment %")
    rate_fin = fields.Integer(string='Rate')
    value_date = fields.Date('Value Date', )
    mature_date = fields.Date('Maturity Date', )

#     for information on previous loans
    loan_amt = fields.Float(string='Loan Amount')
    duration = fields.Integer(string="Duration (In months)")
    nr_credit = fields.Float(string="Nr. Credit Taken")

    institute  = fields.Char(string='Institution')
    reg_date_new = fields.Date('Registration Date', )
    approve_date = fields.Date('Approval Date', )

    notes_auth = fields.Text(string='Notes Authorizer')
    notes_fin = fields.Text(string='Notes')

    charge_det_ids = fields.One2many('charges.details','charge_det_id')

    # def for creating entries in schedule
    @api.multi
    def create_schedule(self):
        current_date = datetime.datetime.now().date()
        if self.financing_amt>0 and self.install_count>0 and self.interest_rate>=0 and self.grace>=0:
            #select_sql_clause = """SELECT sum(residual_company_signed) as total, min(date) as aggr_date from account_invoice where journal_id = %(journal_id)s and state = 'open'"""
            query = ''
            select_sql_clause = """delete from loan_schedule where"""
            query += ""+select_sql_clause+" schedule_id ='"+str(self.id)+"'"
            #self.env.cr.execute(query, {'journal_id':self.id})
            self.env.cr.execute(query)

            sc_det_obj = self.env['loan.schedule']
            no_of_days = ''
            next_ins_date =''
            if self.ins_start_date:
                next_ins_date = self.ins_start_date
            else:
                self.ins_start_date = current_date
                next_ins_date = current_date

            if self.unit_fin == 'daily':
                no_of_days = 1
                print
            elif self.unit_fin == 'weekly':
                no_of_days = 7
                print
            elif self.unit_fin == 'monthly':
                print
                no_of_days = 30
            elif self.unit_fin == 'quarterly':
                print
                no_of_days = 90
            elif self.unit_fin == 'half_yearly':
                print
                no_of_days = 180
            elif self.unit_fin == 'yearly':
                print
                no_of_days = 365
            else:
                self.unit_fin == 'monthly'
            #for count in self.install_count:

            
            my_kest=(-self.financing_amt + (-self.financing_amt/(math.pow(((self.interest_rate/100/12)+1),self.install_count) -1)))*-(self.interest_rate/100/12)
            outstand_amt_amortized=self.financing_amt
            count=1

            #one_month=datetime.timedelta(days=30)
            #next_month =dateutil.parser.parse(self.ins_start_date).date()+one_month
            #print next_month

            #Put the Amount of Approve
            sch_vals={
                        'schdnr':1,
                        'schedule_id':self.id,
                        'schddate':dateutil.parser.parse(self.ins_start_date).date(),
                        'transtypeid':1,
                        'install_percent':'',
                        'install_amt':outstand_amt_amortized,
                        'schdint':0,
                        'schdfee':0,
                        'schdprin':outstand_amt_amortized,
                        'outstand_amt':0,
                    }
            schedule_ids = sc_det_obj.create(sch_vals);
            #Put the Amount of Fees
            sch_vals={
                        'schdnr':0,
                        'schedule_id':self.id,
                        'schddate':dateutil.parser.parse(self.ins_start_date).date(),
                        'transtypeid':1,
                        'install_percent':'',
                        'install_amt':-outstand_amt_amortized*0.1,
                        'schdint':0,
                        'schdfee':-outstand_amt_amortized*0.1,
                        'schdprin':0,
                        'outstand_amt':0,
                    }
            schedule_ids = sc_det_obj.create(sch_vals);


            #print self.install_count
            #print self.id
            for count in range (1,self.install_count+1+self.grace):
                # install_date
                # 'install_month':self.ins_start_date,
                # + timedelta(days=no_of_days),
                #branch_id = fields.Char (string='Branch Id')
                #loanid=fields.Char (string= 'Loan Id')
                one_month= relativedelta(months=+count)
                print one_month
                if count <= self.grace:
                    my_kapital=0;
                    sch_vals={
                        'schdnr':count,
                        'schedule_id':self.id,
                        'schddate':dateutil.parser.parse(self.ins_start_date).date()+one_month,
                        'transtypeid':4,
                        'install_percent':'',
                        'install_amt':-outstand_amt_amortized*((self.interest_rate/100)/12),
                        'schdint':-(outstand_amt_amortized*((self.interest_rate/100)/12)-my_kapital),
                        'schdfee':0,
                        'schdprin':-my_kapital,
                        'outstand_amt':outstand_amt_amortized,
                    }
                else:
                    my_kapital=my_kest-outstand_amt_amortized*((self.interest_rate/100)/12)
                    sch_vals={
                        'schdnr':count,
                        'schedule_id':self.id,
                        'schddate':dateutil.parser.parse(self.ins_start_date).date()+one_month,
                        'transtypeid':4,
                        'install_percent':'',
                        'install_amt':-my_kest,
                        'schdint':-(my_kest-my_kapital),
                        'schdfee':0,
                        'schdprin':-my_kapital,
                        'outstand_amt':outstand_amt_amortized,
                    }
                count =1+count;
                outstand_amt_amortized=outstand_amt_amortized-my_kapital;
                schedule_ids = sc_det_obj.create(sch_vals);
                
                


        return True
        
#
#
class charges_details(models.Model):
    _name = "charges.details"

    comp_name = fields.Char(string='Component Name')
    event_code = fields.Char(string='Requested Amount')
    currency_charges = fields.Many2one('res.currency',string='Currency', help='Utility field to express amount currency')
    charge_amount = fields.Float(string='Amount')
    waive = fields.Boolean(string='Waive')
    # comp_name = fields.Char(string='Component Name')

    charge_det_id = fields.Many2one('loan.application',string='Charge Details')

# =========================    for credit score tab===============================

class credit_rating(models.Model):
    _name = "credit.rating"

    category = fields.Char(string='Category')
    question = fields.Char(string='Question')
    answer = fields.Char(string='Answer')

    crd_rate_id =  fields.Many2one('loan.application',string='Internal Credit Rating')

class risk_factor(models.Model):
    _name = "risk.factor"

    risk_fac = fields.Char(string='Risk Factor')
    description = fields.Char(string='Description')

    risk_fac_id = fields.Many2one('loan.application', string='Risk Factor Details')



class loan_application(models.Model):
    _inherit = "loan.application"
    rule_id = fields.Char(string='Rule Id')
    grade = fields.Char(string='Grade')
    score = fields.Char(string='Score')

    crd_rate_ids = fields.One2many('credit.rating','crd_rate_id')
    risk_factor_ids = fields.One2many('risk.factor','risk_fac_id')
#===========================================================================

# ================================== for Bureau tab=================================
class credit_bureau(models.Model):
    _name = "credit.bureau"

    cust_id = fields.Char(string='Customer Id')
    bureau = fields.Char(string='Bureau')
    status = fields.Selection([('completed', 'Completed'),('pending','Pending'),], string='Status')
    remarks = fields.Char(string='Remarks')


    crd_bur_id =  fields.Many2one('loan.application',string='Credit Bureau Details')

class ext_credit_rating(models.Model):
    _name = "ext.credit.rating"

    ext_agency = fields.Char(string='External Agency')
    bureau = fields.Char(string='Bureau')
    recommended = fields.Selection([('recommended', 'Recommended'),('nrecommended','Not Recommended'),], string='Recommended')
    status = fields.Selection([('initiated', 'Initiated'),('completed','Completed'),], string='Status')
    remarks = fields.Char(string='Remarks')
    score = fields.Char(string='Score')

    ext_crd_id =  fields.Many2one('loan.application',string='Credit Bureau Details')


class loan_application(models.Model):
    _inherit = "loan.application"

    @api.multi
    def create_default_lines(self):
        chk_lst_obj = self.env['checklist.details']
        chklist_ids = []
        chk_id = self.checklist_ids
        if not len(chk_id):
            chk_vals1 = {
                'serial_no': 1,
                'document': 'vdvsv',
                'status': 'not',
            }
            chk_vals2 = {
                'serial_no': 2,
                'document': 'Customer Contract',
                'status': 'not',
            }
            chk_vals3 = {
                'serial_no': 3,
                'document': 'For mortgage contract,should certificates of property'
                            'and property be blocked?',
                'status': 'not',
            }
            chk_vals4 = {
                'serial_no': 4,
                'document': 'For RBS contract documents must be the property of'
                            'movable property ,vehicle certificate,driving licence,goods'
                            'purchase invoices ,purchase contract goods,the form of '
                            'goods inventory conducted by Branch etc. and blocking the RBS ',
                'status': 'not',
            }
            chk_vals5 = {
                'serial_no': 5,
                'document': 'For mortgage,contract should also pledge statement',
                'status': 'not',
            }
            chk_vals6 = {
                'serial_no': 6,
                'document': 'Family certificate ,identity card of the client and guarantors',
                'status': 'not',
            }
            chk_vals7 = {
                'serial_no': 7,
                'document': 'Executive Order(must be original)',
                'status': 'not',
            }
            chk_vals8 = {
                'serial_no': 8,
                'document': 'BOA Report and paperwork for consent to search the BOA',
                'status': 'not',
            }
            chk_vals9 = {
                'serial_no': 9,
                'document': 'Applying for loans',
                'status': 'not',
            }
            chk_vals10 = {
                'serial_no': 10,
                'document': 'Tax certificate + NRC extract',
                'status': 'not',
            }
            chk_vals11 = {
                'serial_no': 11,
                'document': 'Map of location of collateral',
                'status': 'not',
            }
            chk_vals12 = {
                'serial_no': 12,
                'document': 'Letters to the delay of the loan officer,branch director or'
                            'director of the Legal Department of the customer signature '
                            'shows that he has taken notice of delay or mail'
                            'confirmations',
                'status': 'not',
            }
            chk_id1 = chk_lst_obj.create(chk_vals1)

            chk_id2 = chk_lst_obj.create(chk_vals2)
            chk_id3 = chk_lst_obj.create(chk_vals3)
            chk_id4 = chk_lst_obj.create(chk_vals4)
            chk_id5 = chk_lst_obj.create(chk_vals5)
            chk_id6 = chk_lst_obj.create(chk_vals6)
            chk_id7 = chk_lst_obj.create(chk_vals7)
            chk_id8 = chk_lst_obj.create(chk_vals8)
            chk_id9 = chk_lst_obj.create(chk_vals9)
            chk_id10 = chk_lst_obj.create(chk_vals10)
            chk_id11 = chk_lst_obj.create(chk_vals11)
            chk_id12 = chk_lst_obj.create(chk_vals12)
            _logger.info('=====================After Credit Ids creation======================')

            chklist_ids.append(chk_id1.id)
            chklist_ids.append(chk_id2.id)
            chklist_ids.append(chk_id3.id)
            chklist_ids.append(chk_id4.id)
            chklist_ids.append(chk_id5.id)
            chklist_ids.append(chk_id6.id)
            chklist_ids.append(chk_id7.id)
            chklist_ids.append(chk_id8.id)
            chklist_ids.append(chk_id9.id)
            chklist_ids.append(chk_id10.id)
            chklist_ids.append(chk_id11.id)
            chklist_ids.append(chk_id12.id)

            _logger.info('=====================chklist_ids %s======================' %chklist_ids)
            # print '=================================='

        return chklist_ids

    monthly_income1 = fields.Float(string='Monthly Income')
    monthly_debt1 = fields.Float(string='Monthly Debt')

    monthly_income2 = fields.Float(string='Monthly Income')
    monthly_debt2 = fields.Float(string='Monthly Debt')

    assets = fields.Char(string='Assets')
    liabilities = fields.Char(string='Liabilities(-)')
    net_worth = fields.Float(string='Net Worth')

    what_if = fields.Float(string='What if Payment Amt')

    crd_bur_ids = fields.One2many('credit.bureau','crd_bur_id')
    ext_crd_ids = fields.One2many('ext.credit.rating','ext_crd_id')
    inv_det_ids = fields.One2many('invets.details','inv_det_id')
    lmc_inv_ids = fields.One2many('lmc.eligible.details','lmc_inv_id')
    schedule_ids = fields.One2many('loan.schedule','schedule_id')

    checklist_ids = fields.One2many('checklist.details','checklist_id',default=create_default_lines)
    comment_ids = fields.One2many('comments.details','comment_id',string='Comments')
    categor_ids = fields.One2many('categ.details','categor_id',string='Categorization')


# ===================================================================================

# ===========================Investigation Tab===============================
class invest_details(models.Model):
    _name = "invets.details"

    customer_no_inv = fields.Char(string='Customer No.')
    ver_type = fields.Char(string='Verification Agency')
    ver_agency = fields.Char(string='Verification Agency')

    inv_det_id = fields.Many2one('loan.application',string='Invetigation Details')
# ===================================================================================


# ===========================LMC Eligibility Ratio Tab===============================
class lmc_eligible_details(models.Model):
    _name = "lmc.eligible.details"

    stated_bef1 = fields.Char(string='Stated Before')
    stated_aft1 = fields.Char(string='Stated After')
    stated_bef2 = fields.Char(string='Stated Before')
    stated_aft2 = fields.Char(string='Stated After')

    ratios = fields.Float(string='Ratios')


    lmc_inv_id = fields.Many2one('loan.application',string='Invetigation Details')
# ===================================================================================


# ===========================Schedule Tab===============================
class loan_schedule(models.Model):
    _name = "loan.schedule"

    branch_id = fields.Char (string='Branch Id')
    loanid=fields.Char (string= 'Loan Id')
    schddate=fields.Date(string='Schedule Date')
    install_percent = fields.Float(string='Installment %')
    install_amt = fields.Float(string='Installment Amount')
    transtypeid = fields.Integer (string = 'Transaction Type id')
    schdnr=fields.Integer(string='Schedule Number')
    schdprin= fields.Float(string='Schedule Principal')
    schdint= fields.Float(string='Schedule Interest')
    schdfee= fields.Float(string='Schedule Fees')
    outstand_amt = fields.Float(string='Outstanding')
    schedule_id = fields.Many2one('loan.application',string='Schedule Details')
# ===================================================================================



# ===========================Checklist Tab===============================
class checklist_details(models.Model):
    _name = "checklist.details"

    serial_no = fields.Integer(string='Sr. No')
    document = fields.Char(string='Document')
    status = fields.Selection([('not', 'Not'), ('pending', 'Pending'),('yes', 'Yes'),('no_need', 'Not needed'), ], string='Status')
    update_date = fields.Date('Last Update Date', )
    updated_by = fields.Many2one('res.users', string='Last Updated By')

    checklist_id = fields.Many2one('loan.application',string='Checklist Details')

    @api.model
    def create(self, vals):

        current_date = datetime.datetime.now().date()
        print 'in the create def============================'
        if self._uid:
            vals.update({'updated_by': self._uid, 'update_date': current_date,})

        res = super(checklist_details, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        current_date = datetime.datetime.now().date()
        if self._uid:
            # vals.update({'updated_by':self._uid,'id':res})
            vals.update({'updated_by': self._uid, 'update_date': current_date,})
            print 'after vals getting updated============================'

        res = super(checklist_details, self).write(vals)
        return res


# ===================================================================================

# ===========================Comments Tab===============================
class comments_details(models.Model):
    _name = "comments.details"

    update_date = fields.Date('Date', )
    status = fields.Char(string='Status')
    event = fields.Char(string='Event')
    notes = fields.Text(string='Notes')
    user = fields.Many2one('res.users', string='User')
    module = fields.Char(string='Module')

    comment_id = fields.Many2one('loan.application',string='Comments Details')
# ===================================================================================


# ===========================Comments Tab===============================
class categ_details(models.Model):
    _name = "categ.details"

    serial_no = fields.Integer(string='Sr. No')
    month = fields.Date('Month', )
    category = fields.Selection([('ca', 'CA'), ('cb', 'CB'), ('cc', 'CC'), ('cd', 'CD'),('ce', 'CE'), ],string='Categorization')

    subject = fields.Char(string='Subject')
    notes = fields.Text(string='Notes')
    user = fields.Many2one('res.users', string='User')
    update_date = fields.Date('Last Update Date', )

    categor_id = fields.Many2one('loan.application',string='Comments Details')
# ===================================================================================







