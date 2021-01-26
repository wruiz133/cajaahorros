from odoo import models, fields, api,_
import datetime
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class loan_application(models.Model):
    _name = "loan.application"
    _rec_name = 'appln_no'


    is_company_customer=fields.Integer(string="CheckCompany",required = True)
    #is_bank_customer=fields.Integer(string="Bank Customer",required=True)

    priority =fields.Selection([('low', 'Low'), ('medium', 'Medium'),('high', 'High')],string='Priority', required=True)

    status = fields.Selection([('draft', 'Draft'), ('open', 'Open'),('ready','Ready to Approve'), ('approve', 'Approved'), ('reject', 'Rejected')],string="Status",default='open')
    appl_type =fields.Selection([('individual', 'Individual Loan'),('group','Group Loan')], string='Application Type',required=True,default='individual')

    product_code = fields.Many2one('product.code', string='Product Code')  # replace this line

    norm_restruct = fields.Selection([('normal', 'Normal'), ('refin', 'Refinanced'), ('restuct', 'Restructered')],
                                     string='Normal/Restructed')  # replace this line

    prelim_id = fields.Char(string='Preleminary ID',
                            default=lambda self: self.env['ir.sequence'].next_by_code('loan.prelim.id'))
    date = fields.Date('Date', required=True)

    purpose = fields.Char(string='Purpose',help='Specify the purpose for which the loan is availed.')

    usr_ref_no = fields.Char(string='User Reference',help='Specify the user reference number for the loan application.', )

    branch = fields.Many2one('admin.branch',string='Branch',required=True)
    customer_acc_id = fields.Char('Unique Client Id', required=True)

    sub_branch = fields.Many2one('admin.sub.branch',string='Sub Branch',required=True)
    officer_id = fields.Many2one('admin.officer', 'Officer' ,required=True)
  
    partner_id = fields.Many2one('res.partner', string='Partner',required=True)
    name = fields.Char('Name' ,required=True)
    fathername= fields.Char('Fathername' ,required=False)
    lastname = fields.Char('Last Name' ,required=False)
    national_id= fields.Char('National id' , required=True)


    loan_app_mem_ids = fields.One2many('people.contact','ppl_cont_id')
    ppl_cont_ids = fields.One2many('people.contact','ppl_cont_id')
    comp_stake_ids = fields.One2many('company.stakeholder','comp_stake_id')
    bank_info_ids = fields.One2many('bank.information','bank_info_id')
    comp_share_ids = fields.One2many('company.share','comp_share_id')
    purp_loan_ids = fields.One2many('purpose.loans.financing','purp_loan_id')
    
    applicant_ids = fields.One2many('applicant.details','applicant_id')
    fin_currency = fields.Many2one('res.currency',string='Financial Currency')
    cust_category = fields.Selection([('categ1','Category 1'),('categ2','Category 2')], string='Customer Caegory')
    accnt_no = fields.Char('Account Number')
    accnt_class = fields.Char('Account Class')


    appln_no = fields.Char(string='Application Number', default=lambda self: self.env['ir.sequence'].next_by_code('loan.application'))


    office = fields.Char(string='Office')
    created_by = fields.Many2one('res.users', string='Created By')
    create_date = fields.Date('Date Of Creation')
    updated_by = fields.Many2one('res.users', string='Last Updated By')
    update_date = fields.Date('Update Date')
    authorized_by = fields.Many2one('res.users', string='Authorized By')
    auth_date = fields.Date('Date Of Authorization')
    approved_by = fields.Many2one('res.users', string='Approved By')
    approval_date = fields.Date('Date Of Approval')

    @api.depends('account_id','name', 'fathername','lastname')
    def name_get(self):
        result = []
        name=''
        for loan_no in self:
            name = str(loan_no.appln_no)
            result.append(( loan_no.id, name))
        return result

class purpose_loans_financing(models.Model):
    _name = 'purpose.loans.financing'

    purpose = fields.Char(string='Purpose')

    comp_share = fields.Char(string='Loans Company and Shareholders')

    institute = fields.Char(string='Institution')
    type_loan = fields.Char(string='Type of Loan')
    amt = fields.Float(string='Amount')
    amt_currency = fields.Many2one('res.currency', string='Currency')
    intrst_rate = fields.Float(string='Interest Rate')
    start_date = fields.Date(string='Starting Date ')
    tendor = fields.Integer(string='Tenor')
    instl_amt = fields.Float(string='Installment Amount')
    notes = fields.Text(string='Notes')

    purp_loan_id = fields.Many2one('loan.application',string='Purpose')





class res_nationality(models.Model):
    _name = 'res.nationality'
    name = fields.Char('Nationality',required=True)
    country = fields.Many2one('res.country', string='Country', required=True)

    _sql_constraints = [
        ('customer_nation_uniq', 'unique(name)', 'The Customer nationality should be unique !!!')
    ]

 # ===============================for detail tab of company========================
class people_contact(models.Model):
    _name = 'people.contact'

    position = fields.Char(string='Position')
    name_cont = fields.Char(string='Name')
    lastname = fields.Char(string='Last Name')
    pk = fields.Selection([('job','Job')],string='Pk?')
    wire = fields.Char(string='Wire')
    docmnt = fields.Char(string='Document')
    nr_doc = fields.Char(string='Nr Doc.')
    address = fields.Char(string='Address')

    ppl_cont_id = fields.Many2one('loan.application',string='People contact the company')

class company_stakeholder(models.Model):
    _name = 'company.stakeholder'

    position = fields.Char(string='Position')
    name = fields.Char(string='Name')
    lastname = fields.Char(string='Last Name')
    education = fields.Selection([('year', '8-year'), ('primary', 'PRIMARY'),
                                  ('up', 'UP'), ('medium', 'MEDIUM'), ('univer_satar', 'AFTER UNIVERSATAR')],
                                 string='Education:', )


    society = fields.Char(string='Society')
    birthdate = fields.Date(string='Birthdate')
    part_per = fields.Integer(string='Part %')

    comp_stake_id = fields.Many2one('loan.application',string='People contact the company')

class bank_information(models.Model):
    _name = 'bank.information'

    branch = fields.Char(string='Branch')
    bank = fields.Selection([('bank1', 'Bank1'), ('bank2', 'Bank2'),],
                                 string='Bank', )

    nr_logaria = fields.Char(string='Nr. Llogaria')

    bank_info_id = fields.Many2one('loan.application',string='Bank Information')

class company_share(models.Model):
    _name = 'company.share'

    company = fields.Char(string='Company')
    part_per = fields.Integer(string='Part %')
    comp_share_id = fields.Many2one('loan.application', string="Company's Share in other companies")


class loan_application(models.Model):
    #_inherit = 'loan.application'
    _inherit = 'loan.application'

    #individual =fields.Boolean("Individual Loan")
    #company =fields.Boolean("Group Loan")

    @api.model
    def create(self, vals):

        current_date = datetime.datetime.now()
        print 'in the create def============================'
        if self._uid:
            vals.update({'created_by': self._uid, 'create_date': current_date, 'status': 'open'})

        _logger.info('=====================vals %s======================' % vals)
        res = super(loan_application, self).create(vals)

        return res

    @api.multi
    def write(self, vals):
        current_date = datetime.datetime.now()
        if self._uid:
            vals.update({'updated_by': self._uid,'update_date':current_date,})
            print 'after vals getting updated============================'
        _logger.info('=====================write operation of loan application  %s======================' % vals)
        res = super(loan_application, self).write(vals)


        return res

    @api.multi
    def action_loan_approve(self):
        #removed albani  res_part_object = self.env['res.partner']
        #removed albani  if self.customer_acc_id and self.name:
        #removed albani      res_part_id = res_part_object.search([('account_id', '=', self.customer_acc_id.strip(" "))])
            

            #removed albani
            # if not prelim_app_id:
            #removed albani if self.appl_type == 'individual':

                #removed albani print 'in the customer creation================'
                #removed albani if not res_part_id:
                #removed albani    part_vals = {
                #removed albani        'individual': True,
                 #removed albani         'account_id': self.customer_acc_id,
                #removed albani          'branch_id': self.branch.id,
                #removed albani          'name':self.name.strip(" "),
                #removed albani          'sub_branch_id': self.sub_branch.id,
                #removed albani          'create_date':self.date,
                #removed albani          'client_guarantor': 'customer',
                #removed albani          'birth_circle': self.country_birth.id,
                 #removed albani         'city_id': self.city_birth.id,
                 #removed albani         'base_type': 'passport',
                #removed albani          'country_issuance': self.country_issuer.id,
                #removed albani          'logari': self.passport_no,
                #removed albani          'citizenship': 'albania',
                #removed albani          'state': 'draft',
                #removed albani          'date_release': self.pas_issue_date,
                 #removed albani         'date_expiry': self.pas_exp_date,
                #removed albani          'country_id': self.country.id,
                 #removed albani         'birthday': self.birthdate,
                #removed albani          'phone': self.mobile_no,
                 #removed albani         'black_list': 'no',
                 #removed albani         'note': 'test note',

                #removed albani      }
                 #removed albani     if self.gender == 'male':
                #removed albani          part_vals.update({'gender': 'man'})
                #removed albani      else:
                #removed albani          part_vals.update({'gender': 'woman'})

                #removed albani      print 'partner vals=======================================', part_vals
                #removed albani      res_id = res_part_object.create(part_vals)
                 #removed albani     print 'res_id===================================', res_id

            #removed albani  elif self.appl_type == 'group':
                #removed albani  if not res_part_id:
                 #removed albani     print
                #removed albani      part_vals = {
                 #removed albani         'company': True,
                 #removed albani         'account_id': self.customer_acc_id,
                #removed albani          'branch_id': self.branch.id,
                 #removed albani         'sub_branch_id': self.sub_branch.id,
                 #removed albani         'create_date': self.date,
                 #removed albani         'client_guarantor': 'customer',
                 #removed albani         'brief_name': self.s_name.strip(" "),
                 #removed albani         'name': self.company_name.strip(" ") or 'company ',
                 #removed albani         'tin':self.tin_no,
                 #removed albani         'citizenship': 'albania',
                 #removed albani         'state': 'draft',
                 #removed albani         'phone': self.mobile_no,
                 #removed albani         'black_list': 'no',
                 #removed albani         'note': 'test note',

                 #removed albani     }

                 #removed albani     if self.country_issuer:
                 #removed albani         part_vals.update({'country_issuance': self.country_issuer.id or 1})
                 #removed albani     if self.type_of_id1:
                #removed albani          part_vals.update({'base_type':self.type_of_id1 or 'identity'})
                 #removed albani     if self.passport_no:
                 #removed albani         part_vals.update({'logari':self.passport_no or '001122'})
                 #removed albani     if self.pas_issue_date:
                #removed albani          part_vals.update({'date_release': self.pas_issue_date,})
                #removed albani      if self.pas_exp_date:
                 #removed albani         part_vals.update({'date_expiry': self.pas_exp_date,})

                 #removed albani     res_id = res_part_object.create(part_vals)
                    # _logger.info('=====================after client creation of company  %s======================'%res_id )



                  
                
                        
        current_date = datetime.datetime.now().date()
        self.write({'status': 'approve',
                    'updated_by': self._uid,
                    'update_date': current_date,
                    'approved_by': self._uid,
                    'approval_date': current_date,
                    })

    @api.multi
    def action_loan_reject(self):

        current_date = datetime.datetime.now().date()
        if self._uid:
            self.write({'status': 'reject',
                        'updated_by': self._uid,
                        'update_date': current_date
                        })
    #
    @api.multi
    def action_ready_approve(self):
        current_date = datetime.datetime.now().date()
        self.write({'status': 'ready', 'updated_by': self._uid, 'update_date': current_date})

    @api.multi
    def action_return_data(self):
        current_date = datetime.datetime.now().date()
        self.write({'status': 'draft', 'updated_by': self._uid, 'update_date': current_date})

    #@api.onchange('appl_type')
    #def onchange_appl_type(self):
        
        #if is_company_customer==-10
        #if not self.company and not self.individual:
        #    if self.appl_type == 'individual':
        #        self.individual =True
        #    else:
        #        self.company =True
        #else:

        #    if self.appl_type == 'individual' and not self.individual:
        #        self.individual = True
        #        self.company = False
        #    else:
        #        self.company =True
        #        self.individual = False

class loan_config_directory(models.Model):
    _name = 'loan.config.directory'
    _rec_name = 'parent_directory'

    parent_directory = fields.Char(string='Parent Directory for Documents')
    loan_directory = fields.Char(string='Loan Documents Directory')
    collateral_directory = fields.Char(string='Collateral Documents Directory')
    collateral_sub_directory = fields.Char(string='Subdirectory for Collateral')

    loan_indiv_directory = fields.Char(string='Subdirectory for Individual Loans')
    loan_compa_directory = fields.Char(string='Subdirectory for Company Loans')

    lien_directory = fields.Char(string='Lien Directory')

    parent_dir_exists = fields.Boolean(string='Parent Directory Exists')


    @api.multi
    def write(self,vals):
        res = super(loan_config_directory,self).write(vals)
        if not self.parent_dir_exists:
            _logger.info("self.parent_dir_exists==================%s" % self.parent_dir_exists)
            # raise UserError(_('Please Specify correct path for Parent Directory.'))
        return res

    @api.onchange('parent_directory')
    @api.depends('parent_directory')
    def check_parent_directory(self):

        path = self.parent_directory+'/'
        directory1 = os.path.dirname(path)
        # if not self.parent_dir_exists:
        if not os.path.exists(directory1):
            self.parent_dir_exists = False

        elif os.path.exists(directory1):
            if  self.parent_dir_exists == False:
                self.parent_dir_exists = True