from odoo import models, fields, api

class loan_application(models.Model):
    _inherit = "loan.application"

    name = fields.Char(string='Customer Name',)

    add_det_ids = fields.One2many('address.details','add_det_id',string='Address Details')

    emp_det_ids = fields.One2many('employment.details','emp_det_id',string='Employment Details')

    insure_det_ids = fields.One2many('insurance.details', 'insure_det_id',string='Insurance Details')

    info_links_ids = fields.One2many('information.links', 'info_links_id',string='Information Links')

class address_details(models.Model):
    _name = "address.details"

    address_type = fields.Selection([('permanent', 'Permanent'), ('home', 'Home'),
                                     ('work', 'Work'), ('temporary', 'Temporary'), ('others', 'Others')],
                                    string='Address Type', )
    mailing = fields.Boolean(string='Mailing')
    add_line1 = fields.Char(string='Address Line 1')
    add_line2 = fields.Char(string='Address Line 2')
    add_line3 = fields.Char(string='Address Line 3')

    contact_no = fields.Char(string='Contact Number')
    zip = fields.Char(string='Zip')
    country_add = fields.Many2one('res.country', string='Country')
    placement_date1 = fields.Date(string='Placement Date')

    add_det_id = fields.Many2one('loan.application',string='Address Details',readonly=True)

class employment_details(models.Model):
    _name = "employment.details"

    empl_type = fields.Selection(
        [('part_time', 'Part Time'), ('full_time', 'Full Time'), ('contract_based', 'Contract Based')],
        string='Employment Type')
    # employer = fields.Char(string='Employer',required = True)
    employer = fields.Char(string='Employer', )
    occupation = fields.Char(string='Occupation')
    designation = fields.Char(string='Designation')
    empl_id = fields.Char(string='Employee Id')

    add_line12 = fields.Char(string='Address Line 1')
    add_line22 = fields.Char(string='Address Line 2')
    add_line32 = fields.Char(string='Address Line 3')
    zip2 = fields.Char(string='Zip')
    country_add2 = fields.Many2one('res.country', string='Country')
    placement_date2 = fields.Date(string='Placement Date')

    extension = fields.Char(string='Extension')
    cont_phone_no = fields.Char(string='Contact Phone')
    contact_name = fields.Char(string='Contact Name')
    contact_ext = fields.Char(string='Contact Extension')
    comments = fields.Char(string='Comments')
    dept = fields.Char(string='Department')
    phone_no = fields.Char(string='Phone Number')

    emp_det_id = fields.Many2one('loan.application',string='Employment Details',readonly=True)

class insurance_details(models.Model):
    _name = "insurance.details"

    sec_company = fields.Char(string='Security Company')
    nr_policy = fields.Char(string='Nr. Policy Life Insurance')
    policy_holder = fields.Char(string='Policy Holder')
    contact_info = fields.Char(string='Contact Information')
    renew_date1 = fields.Date(string='Renewal Date')

    insure_det_id =fields.Many2one('loan.application',string='Insurance Details',readonly=True)



class Information_links(models.Model):
    _name = "information.links"

    part_of_an = fields.Selection([('no', 'Not'), ('yes', 'Yes'), ], string='Part Of another Business', )
    specify = fields.Char(string='Specify Business')
    member_of_foun = fields.Char(string='Member of the Foundation associated with the client')
    connection_type = fields.Selection([('baba','BABA'),('men','MEN'),('kinship','Kinship'),
                                    ('grfat','Grandfather'),('gramot','Grandmother'),('woman','WOMAN'),
                                    ('group','Group'),('sis_comp','Sister Company'),('woman','WOMAN'),
                                    ('mama','MAMA'),('sister','Sister'),('family_mem','Family Members'),
                                    ('same_owner','Same Owner'),('subdiary_co','Subdiary Co.'),('group_mem','Group Members'),
                                    ('brother','Brother')],string='Connection Type')
    # connection_type = fields.Char(string='Connection Type')

    info_links_id = fields.Many2one('loan.application',string='Information Links',readonly=True)


class applicant_details(models.Model):
    _name = 'applicant.details'

    #is_company_customer=fields.Integer(string="CheckCompany",required = True)
    #is_company_customer_det = fields.Integer(string='CheckCompany',required = False)
    #partner_id = fields.Many2one('res.partner', string='Partner',domain="[('is_company_customer','=',is_company_customer),('is_bank_customer','=','-1')]")
    partner_id = fields.Many2one('res.partner', string='Partner',required = True, domain="[('is_bank_customer','=','-1')]")
    #is_company_customer=fields.Integer(string='CheckCompany',required = False)
    is_company_customer_det = fields.Integer(string='CheckCompany',required = True )
    
    type = fields.Selection([('primary', 'Primary'),('co_appl','Co-Applicant'),], string='Type',required = True)
    existing = fields.Boolean(string='Existing',required = True)
    customer_no1 = fields.Char(string='Customer No.',required = True)

    customer_type_name = fields.Selection([
                    ('mr', 'Mr.'),('mrs','Mrs.'),('miss','Miss'),
                    ('dr','Dr.'),('anonime','ANONIME'), ('private','PRIVATE'),('ltd', 'Ltd.'), ('join', 'Join.'), ('stock', 'Stock')
                    ,('other','OTHERS')
                    ],string='Customer Type',required=True)
    f_name = fields.Char(string='First Name',required = True)
    m_name = fields.Char(string='Middle Name')
    l_name = fields.Char(string='Last Name',required = True)
    national_id = fields.Char(string='National Id',required = True)
    in_cont = fields.Selection([('yes', 'Yes'), ('no', 'No'), ], string='Include in Contract',required = True)  # include this line
    applicant_id =fields.Many2one('loan.application',required = True)

    gender = fields.Selection([('M', 'Man'), ('W', 'Woman')], string="Gender" ,required=False)
    birthdate = fields.Date('Date Of Birth',required = True)
    country_birth = fields.Many2one('res.country', string='Country Of Birth',required = True)
    city_birth = fields.Many2one('admin.city', string='City Of Birth',required = True)
    
    mother_name = fields.Char(string='Mothers/ Maiden Name')
    last_name_bef= fields.Char(string='Last Name Before Marriage')
    # cust_category = fields.Selection([()],string='Customer Caegory')

    exp_wife_husband = fields.Char(string='Experience Wife/Husband')
    name_last_name = fields.Char(string='Name,Father Name,Last Name Wife/Husband')

    

    country = fields.Many2one('res.country', string='Country',required=True)

    country_issuer = fields.Many2one('res.country', string='Country Issuer',required = True)
    #nationality = fields.Many2one('res.nationality',string='Nationality')
    nationality = fields.Selection([('foreign', 'Foreign'), ('albania', 'Albania')], string="Citizenship", required=True)
    language =fields.Char(string='Language')
    mobile_no = fields.Char(string='Mobile No.',required = True)
    landline_no = fields.Char(string='Landline No.')
    office_no = fields.Char(string='Office No.')
    fax_no = fields.Char(string='Fax ')
    email = fields.Char(string='Email')

    city_issued = fields.Many2one('admin.city', string='City Issued',required = False)

    passport_no = fields.Char(string='ID Number',required = True)
    pas_issue_date = fields.Date('Issue Date',required = True)
    pas_exp_date = fields.Date('Expiry Date',required = True )

    type_of_id1 = fields.Selection([
                                            ('certificate', 'Certificate'), 
                                            ('biometric', 'Identification Card / Biometric Password'),
                                            ('identity_card', 'Identity Card Old'), 
                                            ('passport', 'Passport Old'),
                                            ('license', 'Driving License')], 
                       string="Type of ID", required=True)

    type_of_id2 = fields.Selection([('certificate', 'Certificate'), ('identity', 'Identification Card / Biometric Password'),
     ('identity_card', 'Identity Card'), ('passport', 'Passport'),('license', 'Driving License')], string="Type Of ID(Optional)")
    passport_no1 = fields.Char(string='ID Number (Optional)')
    pas_issue_date1 = fields.Date(' Issue Date (Optional)')
    pas_exp_date1 = fields.Date(' Expiry Date (Optional)')
    no_of_people = fields.Integer(string='No. of people on certificate')
    dependents  = fields.Integer(string='Dependents',help='Specify the number of dependents for the customer.')
    marital_status = fields.Selection([('married','Married'),('unmarried','Unmarried'),('divorcee','Divorcee')],string='Marital Status')

    education = fields.Selection([('year','8-year'), ('primary','PRIMARY'),
       ('up','UP'), ('medium','MEDIUM'), ('univer_satar','AFTER UNIVERSATAR')],string='Education:',)
    exp = fields.Char(string='Experience',)

    social_sit = fields.Selection([('ambulant','AMBULANT'), ('without_job','WITHOUT JOB'),
       ('private_with_license','PRIVATE WITH LICENSE'), ('private_without_license','PRIVATE WITHOUT LICENSE'),
       ('employed','EMPLOYED')],string='Social situations:',)



    #industry_sector = fields.Selection([('airline_part','Airlines Part'), ('touristic_agency','Touristic Agency'), 
    #                ('private_educat','Private Education'), ('artist','Artist'),
    #                ('lawyer','Lawyer'), ('coffee_bar','Coffee Bar'),
    #                ('coffee_bar_tourist','Coffee Bar (Tourist Season)'), ('business_purposes','Purchase wheel used for business purposes'),
    #                ('dentist','Dentist'), ('pharmacist','Pharmacist'),
    #                ('light_food','Light Industry & Food'), ('construct_industry','Construction Industry'),
    #                ('extract_process','Extracting Industry & processing'), ('agri_service','Agricultural Inputs and Services'),
    #                ('input_livestock','Inputs To Livestock'), ('loan_ee','Loans for EE (Energy Efficiency)'),
    #                ('agri_machine','Agricultural Machinary'), ('doctor','Doctor'),
    #                ('barber','Hairdresser/Barber'), ('real_estate','Real estate, leasing'),
    #                ('rental_tourism','Real estate, rental Tourism'), ('arboriculture','Arboriculture'),
    #                ('field_vegetables','Field vegetables'), ('fishing','Fishing'),
    #                ('not_include','Not included above it'), ('restaurant','Restaurant'),
    #                ('restaurant_tourist','Restaurant (Tourist season)'), ('vehicle_repair_free','Vehicle repair free & other charges'),
    #                ('home_repairs','Home repairs (Used for tourism)'), ('hotel_motel','Repair, construction, furniture Hotel-Motel used for Tourism'),
    #                ('various_repairs','Various repairs'), ('cattle_growing','Cattle Growing of fine'),
    #                ('cattle_breeding','Cattle Breeding'), ('poultry','Poultry Growing'),
    #                ('seamstress','Seamstress'), ('sere','Sere'),
    #                ('agri_land','Agricultural land'), ('retail','Retail'),
    #                ('wholesale_trade','Wholesale Trde'), ('olive_groves','Olive groves'),
    #                ('viticulture','Viticulture')],string='Industry Sector')
        #    industry = fields.Char('Industry:' ,required=True)
    #industry_group = fields.Selection([('handicraft','HANDICRAFT'), ('livestock','AGRICULTURE & LIVESTOCK'), 
    #                ('industry','INDUSTRY'), ('consumer','CONSUMER'),
    #                ('construction','CONSTRUCTION'), ('service','SERVICES'),
    #                ('transport','TRANSPORT'), ('trade','TRADE'),
    #                ('tourism','TOURISM')],string='Industry Group')
    #industry_code = fields.Selection([('code1','Code1'), ('code2','Code2'), 
    #                ],string='Industry Code')

    industry_sector = fields.Selection([('trade','Trade'), ('agriculture','Agriculture'), 
                    ('animal_husbandry','Animal Husbandry'), ('manufacturing','Manufacturing'),
                    ('services','Services'), ('trade','Trade'), ('unknown','Unknown')],string='Industry Sector',required=True)
    
    industry_group = fields.Selection([('ac','A- Crops'),('ao','A- Other'),('a','A-Bujqesi'), 
                    ('an','AN-Blegtori'), ('anl','AN- Livestock'),('ano','AN- Other'),('anp','AN- Poultry'),
                    ('cw','C-Konsum CWBO'), ('c','C-Konsum'), ('h','H-Housing'),
                    ('p','P-Prodhim'), ('pd','P- Dairy'), ('pf','P- Food'), ('po','P- Other'), ('pw','P- Wood-Related'), 
                    ('s','S-Sherbim'), ('sb','S- Bar/Rest'),('sc','S- Construction'),('sm','S -Media & Com.'),
                    ('so','S- Other'),('st','S- Transport'),('sp','S- Prof Trade'),
                    ('t','T-Tregti'), ('to','T- Other'),('ts','T- Shops Retail'),('tsh','T- Shops Whole.'),('unknown','Unknown')
                    ],string='Industry Group',required=True)

    industry_code = fields.Selection([('unknown','Unknown') 
                    ],string='Industry Code',required=True)

    #reg_date1 = fields.Date(string='Registration Date')

    begin_act_date = fields.Date(string='Date of Begin Activity')

    no_of_employees = fields.Integer(string='Number of Employees')
    business_env= fields.Selection([('with_rent','With Rent'),('ownership','Ownership'),
                                    ('own_part','Ownership Of Partner'),('other','Other')],string='Business Environment')
    no_of_owners = fields.Integer(string='Number of Owners')

    # company_name = fields.Char(string='Company Name')
    ext_audit = fields.Char(string='External Audit')
    email_audit = fields.Char(string='Email Audit')
    type_of_rel = fields.Selection([('baba','BABA'),('men','MEN'),('kinship','Kinship'),
                                    ('grfat','Grandfather'),('gramot','Grandmother'),('woman','WOMAN'),
                                    ('group','Group'),('sis_comp','Sister Company'),('woman','WOMAN'),
                                    ('mama','MAMA'),('sister','Sister'),('family_mem','Family Members'),
                                    ('same_owner','Same Owner'),('subdiary_co','Subdiary Co.'),('group_mem','Group Members'),
                                    ('brother','Brother')


                                    ],string='Type of relation to Client')





    date_incopr = fields.Date(string='Date')
    capital = fields.Float(string='Capital')
    net_worth = fields.Float(string='Net Worth')
    country_1 = fields.Many2one('res.country', string='Country')
    currency_amt = fields.Many2one('res.currency',string='Currency Amount', help='Utility field to express amount currency')


    

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        print"----------self-----------",self
        print"----------self-----------",self.partner_id
        #if self.partner_id != '' or self.partner_id != '0':
        if self.partner_id:
            if self.partner_id.is_company_customer == -10:
                self.is_company_customer_det='-10'
                self.m_name = self.partner_id.fathername or ''
                self.l_name = self.partner_id.lastname or ''
                self.mother_name = self.partner_id.maiden_name or ''
                self.last_name_bef = self.partner_id.last_name_bef or ''
                self.gender = self.partner_id.gender or ''   
                self.existing = True
            if self.partner_id.is_company_customer == -20:
                #self.branch_id = self.partner_id.branch_id or ''
                #self.sub_branch_id = self.partner_id.sub_branch_id or ''
                self.is_company_customer_det='-20'
                self.f_name = self.partner_id.name or ''
                self.l_name = self.partner_id.detail_name_com or ''
                self.existing = True
                self.m_name =''
                self.gender =''
                self.mother_name = ''
                self.last_name_bef = ''


            if self.partner_id.is_company_customer == -10 or self.partner_id.is_company_customer == -20:
                self.f_name = self.partner_id.name or ''
                self.national_id = self.partner_id.national_id or ''
                self.customer_no1 = self.partner_id.account_id or ''
                self.country= self.partner_id.country_issuance or ''
                self.customer_type_name =  self.partner_id.customer_type_name or ''
                self.industry_sector =  self.partner_id.industry_sector or ''
                self.industry_group =  self.partner_id.industry_group or ''
                self.industry_code =  self.partner_id.industry_code or ''
                self.type_of_id1 = self.partner_id.national_id_type or ''
                self.passport_no = self.partner_id.document_client_id or ''
                self.pas_issue_date = self.partner_id.date_release or ''
                self.country_issuer = self.partner_id.country_issuance or '' 
                self.city_issued = self.partner_id.city_id or ''
                self.nationality = self.partner_id.citizenship or ''
                self.pas_exp_date = self.partner_id.date_expiry or ''
                self.birthdate = self.partner_id.birthday
                self.country_birth = self.partner_id.birth_country or ''
                self.city_birth = self.partner_id.city_id or ''
                self.landline_no = self.partner_id.phone or ''
                self.fax = self.partner_id.fax or ''
                self.mobile_no = self.partner_id.mobile or ''

        print"----------self-----------",self.is_company_customer_det
        
        #for line in self.browse(cr, uid, ids):
            #if line.purchase_order_id:
                #raise osv.except_osv('error!', 'not allowed to delete record with purchase_line_id')
            #return super(name_of_class, self).unlink(cr, uid, ids)


    @api.multi
    def unlink(self, cr, uid, ids, context=None):
         print"-------unlink-------",self.type
         if self.type == 'primary':
             raise except_orm('Warning','It is advisable to deactivate the record rather than deleting it!')
         return super(applicant_details, self).unlink()
    @api.multi
    def get_data(self):

        cust_acc_id = self.customer_no1
        res_part_object = self.env['res.partner']
        pre_app_object = self.env['prelim.app']

        if cust_acc_id:
            partner_id = res_part_object.search([('account_id', '=', cust_acc_id.strip(" "))])
            prelim_app_id = pre_app_object.search([('account_id1', '=', cust_acc_id.strip(" "))])
            appl_id = self.applicant_id
            if appl_id:

                if partner_id or prelim_app_id:
                    if not self.existing:
                        self.existing = True
                    if prelim_app_id:
                        self.f_name =  prelim_app_id[0].name or partner_id[0].name or ''
                        self.m_name =  prelim_app_id[0].fathername or ''
                        self.l_name = prelim_app_id[0].lastname or ''
                    else:
                        self.f_name = partner_id[0].name or ''
                        self.m_name = partner_id[0].fathername or ''
                        self.l_name = partner_id[0].lastname or ''
                    #'customer_acc_id':cust_acc_id,  
                    write_vals={
                       
                        'name': partner_id[0].name or prelim_app_id[0].name,
                        'birthdate':partner_id[0].birthday,
                        'country_birth':partner_id[0].birth_circle.id,
                        'city_birth':partner_id[0].city_id.id,
                        'country': partner_id[0].country_id.id or partner_id[0].birth_circle.id,

                    }
                    if prelim_app_id:
                        write_vals.update({'mobile_no': partner_id[0].phone  or prelim_app_id[0].mobile_no or '+91',
                                           'fax_no': prelim_app_id[0].fax or '',
                                           'email': prelim_app_id[0].email or '',
                                           'exp': prelim_app_id[0].exp or 0,
                                           'dependents': prelim_app_id[0].chdrn or '',
                                           'no_of_people': prelim_app_id[0].tmember or '',
                                           'social_sit': prelim_app_id[0].ssituation or '',
                                           'education': prelim_app_id[0].educat or '',

                                           })
                    if partner_id[0].gender == 'man':
                        write_vals.update({'gender': 'man'})
                    else:
                        write_vals.update({'gender': 'woman'})

                    if prelim_app_id:
                        if prelim_app_id[0].mstatus == 'single':
                            write_vals.update({'marital_status': 'unmarried'})
                        elif prelim_app_id[0].mstatus == 'divorce':
                            write_vals.update({'marital_status': 'divorcee'})
                        elif prelim_app_id[0].mstatus == 'married':
                            write_vals.update({'marital_status': 'married'})
                        else:
                            write_vals.update({'marital_status': 'unmarried'})

                    appl_id.write(write_vals)
                    #if len(appl_id.applicant_ids)>1:
                    #    for cust_det_id in appl_id.applicant_ids:
                            #--if appl_id.customer_acc_id != cust_det_id.customer_no1:
                             #--   cust_det_id.existing =False
                                # _logger.info('=====================After Write operation======================' )
                else:
                    self.existing = False

                    current_date = datetime.datetime.now().date()
                    #'customer_acc_id': cust_acc_id or '',
                    write_vals = {
                        
                        'name': '',
                        'birthdate': current_date ,
                        'mobile_no': '',
                        'landline_no': '',
                        'fax_no':  '',
                        'email': '',
                        'exp': 0,
                        'dependents': '',
                        'no_of_people': '',
                        'social_sit': '',
                        'education':  '',
                        'marital_status':'',
                        'gender':'',
                    }
                    appl_id.write(write_vals)
                    self._cr.commit()
                    # _logger.info('=====================After Clear operation======================')


            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
