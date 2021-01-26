from odoo import models, fields, api, _
import math
from datetime import datetime

class prelim_app(models.Model):
    _name = "prelim.app"
    _rec_name = "name"

    @api.one
    @api.depends('partner_id.account_id')
    def _compute_id(self):
        #ret = super(prelim_app,self)._compute_id()
        self.account_id1 = self.partner_id.account_id
        return 1
    
    @api.one
    def _compute_user(self):
        self.user_id = self._uid

    is_company_customer=fields.Integer(string="CheckCompany",required = True)
    is_bank_customer=fields.Integer(string="Bank Customer",required=True)

    state = fields.Selection([('draft','Registered'), 
       ('ready','Ready for Approve'), ('approve','Loan Application'), ('eliminate','Eliminated'),
       ('reject','Do Not Approve')],default='draft')

    user_id = fields.Many2one('res.users', compute='_compute_user',string='Created by')
    create_date = fields.Datetime('Create Date')
    user_update_id = fields.Many2one('res.users',string='Updated by')
    update_date = fields.Datetime('Update Date')
    user_authorize_id = fields.Many2one('res.users',string='Authorize by')
    authorize_date = fields.Datetime('Authorize Date')
    
    #if is_company_customer =='-10' and is_bank_customer=='-1':
    #    partner_id = fields.Many2one('res.partner', string='Partner',domain="[('is_company_customer','=','-10'),('is_bank_customer','=','-1')]")
    #elif is_company_customer =='-20' and is_bank_customer=='-1':
    #    partner_id = fields.Many2one('res.partner', string='Partner',domain="[('is_company_customer','=','-20'),('is_bank_customer','=','-1')]")
    #else:
    #partner_id = fields.Many2one('res.partner', string='Partner',select=2)
    #partner_id=fields.Many2one('res.partner', string='Partner')
    partner_id = fields.Many2one('res.partner', string='Partner',domain="[('is_company_customer','=',is_company_customer),('is_bank_customer','=','-1')]")
    
    branch_id = fields.Many2one('admin.branch', string='Branch' ,required=True)
    sub_branch_id = fields.Many2one('admin.sub.branch', string='Sub Branch' ,required=True)
    officer = fields.Many2one('admin.officer', 'Officer' ,required=True)
    account_id1 = fields.Char('Unique Client Id',compute = '_compute_id', required=False)

    user_officer_id = fields.Many2one('res.users', 'Officer' )
    
    #==>
    customer_type_name = fields.Selection([
                    ('mr', 'Mr.'),('mrs','Mrs.'),('miss','Miss'),
                    ('dr','Dr.'),('anonime','ANONIME'), ('private','PRIVATE'),('ltd', 'Ltd.'), ('join', 'Join.'), ('stock', 'Stock')
                    ,('other','OTHERS')
                    ],string='Customer Type',required=True)
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
    #                ('viticulture','Viticulture')],string='Industry Sector',required=False)
        #    industry = fields.Char('Industry:' ,required=True)
    #industry_group = fields.Selection([('handicraft','HANDICRAFT'), ('livestock','AGRICULTURE & LIVESTOCK'), 
    #                ('industry','INDUSTRY'), ('consumer','CONSUMER'),
    #                ('construction','CONSTRUCTION'), ('service','SERVICES'),
    #                ('transport','TRANSPORT'), ('trade','TRADE'),
    #                ('tourism','TOURISM')],string='Industry Group',required=False)
    #industry_code = fields.Selection([('code1','Code1'), ('code2','Code2'), 
    #                ],string='Industry Code',required=False)


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

    productservice = fields.Char('Product Services' ,required=False)
    

    fathername= fields.Char('Fathername' ,required=False)
    lastname = fields.Char('Last Name' ,required=False)
        
        
        
        
    gender = fields.Selection([('M', 'Man'), ('W', 'Woman')], string="Gender" ,required=False)
        
    
    mstatus = fields.Selection([('unmarried','Unmarried'), ('divorcee','Divorcee'), 
                ('married','Married')],string='Marital status',required=False)
    ssituation = fields.Selection([('ambulant','AMBULANT'), ('without_job','WITHOUT JOB'), 
                ('private_with_license','PRIVATE WITH LICENSE'), ('private_without_license','PRIVATE WITHOUT LICENSE'),
                ('employed','EMPLOYED')],string='Social situations',required=False)

    educat = fields.Selection([('year','8-year'), ('primary','PRIMARY'), 
                ('up','UP'), ('medium','MEDIUM'), ('univer_satar','AFTER UNIVERSATAR')],string='Education',required=False)
    exp = fields.Char('Experience ',required=False)
    chdrn = fields.Integer('Children under 18' ,required=False)
    tmember = fields.Integer('Nr. The member according to cert.' ,required=False)
    #==>

    other_name_ids = fields.One2many('other.name', 'prelim_id' ,string='Other Name')


    
    
    name = fields.Char('Name' ,required=True)
    maiden_name = fields.Char('Maiden Name')
    last_name_bef= fields.Char(string='Last Name Before Marriage')
    preferedname= fields.Char('Prefered Name')
    detail_name_com = fields.Char('Detail Name')

    birthday = fields.Date('Birthdate' ,required=True)

    national_id_type = fields.Selection([
                                            ('certificate', 'Certificate'), 
                                            ('biometric', 'Identification Card / Biometric Password'),
                                            ('identity_card', 'Identity Card Old'), 
                                            ('passport', 'Passport Old'),
                                            ('license', 'Driving License')], 
                       string="Type", required=True)
    document_client_id=fields.Char('Document Id' , required=True)
    
    country_issuance = fields.Many2one('res.country', string='Country of Issuance', required=True)
    citizenship = fields.Selection([('foreign', 'Foreign'), ('albania', 'Albania')], string="Citizenship", required=True)
    

    date_release = fields.Date('Release Date', required=True)
    date_expiry = fields.Date('Expiration Date', required=True)
    birth_country = fields.Many2one('res.country', string='Country of Birth', required=True)
    city_id = fields.Many2one('admin.city', string='City of Birth', required=True)
        

    national_id= fields.Char('National id' , required=True)
    country_id = fields.Many2one('res.country', string='Country')
    # district_id = fields.Many2one('admin.district', string='District:',required=True)
    district_id = fields.Many2one('admin.district', string='District')
    # municipality = fields.Many2one('admin.municipal', string='Municipalities/Municipality:', required=True)
    municipality = fields.Many2one('admin.municipal', string='Municipality',)
    # city_village = fields.Many2one('admin.village', string='City/Village:', required=True)
    city_village = fields.Many2one('admin.village', string='City/Village',)
    street = fields.Char('Street',)
    data_placement = fields.Date('Placement Date' )
    fax = fields.Char('Fax' )
    email = fields.Char('Email' )
    mobile = fields.Char(string='Mobile No.' ,required=True)
    phone = fields.Char(string='Phone' ,)
    oaddress = fields.Text('Other Address')
    
    contact_company_ids = fields.One2many('contact.company', 'prelim_com_id' ,string='People contact the company')
    
    phone_ids = fields.One2many('phone.record', 'prelim_id' ,string='Other Phones')

    amount_available = fields.Float('Amount Available' ,required=False)
    monthly_turnover = fields.Float('Monthly Turnover' ,required=False)
    friend_relative = fields.Float('Friends and relatives' ,required=True)
    loan_credit = fields.Float('Loan Credit' ,required=True)
    #project = fields.Char('Project' ,required=False)
    currency = fields.Many2one('res.currency', string='Currency',required=True)
    investment = fields.Char('Specify Investment' ,required=False)
    
    guarantee_ids = fields.One2many('guarantee.record', 'prelim_id' ,string='Guarantees')
    
    inform_by = fields.Char('I was informed by' ,required=True)
    notes = fields.Text('Notes' ,required=True)
    black_list = fields.Selection([('no', 'NO'), ('yes', 'YES')], string="Black List")
    approve = fields.Boolean('Approve', default=False)  
    
    eliminate_note = fields.Text('Note For Eliminating')
    reject_note = fields.Text('Note For Rejecting')


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        print"----------self-----------",self
        print"----------self-----------",self.partner_id
        #if self.partner_id != '' or self.partner_id != '0':
        if self.partner_id:
            print self.partner_id.account_id
            if self.is_company_customer == -10:
                self.name = self.partner_id.name or ''
                self.fathername = self.partner_id.fathername or ''
                self.national_id = self.partner_id.national_id or ''
                self.account_id1 = self.partner_id.account_id or ''
                self.customer_type_name =  self.partner_id.customer_type_name or ''
                self.industry_sector =  self.partner_id.industry_sector or ''
                self.industry_group =  self.partner_id.industry_group or ''
                self.industry_code =  self.partner_id.industry_code or ''
                self.lastname = self.partner_id.lastname or ''
                self.maiden_name = self.partner_id.maiden_name or ''
                self.last_name_bef = self.partner_id.last_name_bef or ''
                self.fathername = self.partner_id.fathername or ''
                self.national_id_type = self.partner_id.national_id_type or ''
                self.document_client_id = self.partner_id.document_client_id or ''
                self.date_release = self.partner_id.date_release or ''
                self.country_issuance = self.partner_id.country_issuance.id or ''
                self.citizenship = self.partner_id.citizenship or ''
                self.date_expiry = self.partner_id.date_expiry or ''
                self.birthday = self.partner_id.birthday
                self.birth_country = self.partner_id.birth_country or ''
                self.city_id = self.partner_id.city_id.id or ''
                self.gender = self.partner_id.gender or ''
                self.country_id = self.partner_id.country_id or ''
                self.district_id = self.partner_id.district_id or ''
                self.municipality = self.partner_id.municipality or ''
                self.city_village = self.partner_id.city_village or ''
                self.street = self.partner_id.street or ''
                self.phone = self.partner_id.phone or ''
                self.fax = self.partner_id.fax or ''
                self.mobile = self.partner_id.mobile or ''
                self.notes = self.partner_id.note or ''
                self.oaddress = self.partner_id.street2 or ''
            if self.is_company_customer == -20:
                #self.branch_id = self.partner_id.branch_id or ''
                #self.sub_branch_id = self.partner_id.sub_branch_id or ''
                self.name = self.partner_id.name or ''
                self.detail_name_com = self.partner_id.detail_name_com or ''
                self.national_id = self.partner_id.national_id or ''
                self.account_id1 = self.partner_id.account_id or ''
                self.customer_type_name =  self.partner_id.customer_type_name or ''
                self.industry_sector =  self.partner_id.industry_sector or ''
                self.industry_group =  self.partner_id.industry_group or ''
                self.industry_code =  self.partner_id.industry_code or ''
                self.national_id_type = self.partner_id.national_id_type or ''
                self.document_client_id = self.partner_id.document_client_id or ''
                self.date_release = self.partner_id.date_release or ''
                self.country_issuance = self.partner_id.country_issuance.id or ''
                self.citizenship = self.partner_id.citizenship or ''
                self.date_expiry = self.partner_id.date_expiry or ''
                self.birthday = self.partner_id.birthday
                self.birth_country = self.partner_id.birth_country or ''
                self.country_id = self.partner_id.country_id or ''
                self.district_id = self.partner_id.district_id or ''
                self.municipality = self.partner_id.municipality or ''
                self.city_id = self.partner_id.city_id or ''
                self.city_village = self.partner_id.city_village or ''
                self.street = self.partner_id.street or ''
                self.phone = self.partner_id.phone or ''
                self.fax = self.partner_id.fax or ''
                self.mobile = self.partner_id.mobile or ''
                self.notes = self.partner_id.note or ''
                self.oaddress = self.partner_id.street2 or ''

    @api.multi
    def action_eliminate(self):
        self.write({'state': 'eliminate','user_update_id': self._uid,'update_date':datetime.now()})
        
    @api.multi
    def action_ready(self):
        self.write({'state': 'ready','user_update_id': self._uid,'update_date':datetime.now()})
        
    @api.multi
    def action_approve(self):
        #print"---------------",self.write_date
        self.write({'state': 'approve'})
        if self.is_company_customer==-10:

            if self.partner_id:
                no_accoun=self.partner_id.account_id
            else:
                no_accoun=""
                select_sql_clause = """SELECT count(id)  as no_accoun from res_partner where is_bank_customer=-1"""
                    
                self.env.cr.execute(select_sql_clause)
                query_results = self.env.cr.dictfetchall()
                print query_results, "----------------------------",query_results[0].get('no_accoun'),len(query_results)
                if query_results[0].get('no_accoun') != None:
                    if query_results[0].get('no_accoun') != None:
                        no_accoun=str(query_results[0].get('no_accoun')+1) 
                    else:
                        no_accoun='Null'

                while len(no_accoun)<6:
                    no_accoun='0' + no_accoun

                m           = 1
                shuma_total = 0
                shuma = 0
                for index in range(0, len(no_accoun)):
                    shifra_kodi_llogari = int(no_accoun[index: index+1])

                    shuma       = shifra_kodi_llogari*m
                    shuma_total = shuma_total + shuma
                    if m == 1:
                        m = 2
                    else:
                        m = 1

                #kapet mbetja ---------------------------------------------------------------
                shifra_e_fundit=0L
                mbetja=0L
                mbetja = math.fmod(shuma_total, 10)
                if mbetja == 0:
                    shifra_e_fundit = 0
                else:
                    shifra_e_fundit = int(10 - mbetja)                      
                #------------------------------------------------------------------------------

                # hequr no_accoun = no_accoun + str(shifra_e_fundit)
                self.account_id1=no_accoun

            partner_vals = {
                
                'branch_id': self.branch_id.id,
                'sub_branch_id': self.sub_branch_id.id,
                'national_id': self.national_id,
                'name': self.name,
                'fathername': self.fathername,
                'lastname': self.lastname,
                'maiden_name': self.maiden_name or '',
                'last_name_bef': self.last_name_bef or '',
                'preferedname': self.preferedname or '',
                'national_id_type': self.national_id_type or '',
                'document_client_id': self.document_client_id,
                'date_release': self.date_release,
                'country_issuance': self.country_issuance.id or '',
                
                'citizenship': self.citizenship or '', 
                'customer_type_name': self.customer_type_name or '',
                'industry_sector': self.industry_sector or '',
                'industry_group': self.industry_group or '',
                'industry_code': self.industry_code or '',   
                'date_expiry': self.date_expiry,
                'birth_country': self.birth_country.id or '',
                'city_id': self.city_id.id or '',
                'gender': self.gender,
                'account_id': no_accoun,
                'country_id': self.country_id.id or '',
                'district_id': self.district_id.id or '',
                'municipality': self.municipality.id or '',
                'city_village': self.city_village.id or '',
                'street': self.street,
                'street2': self.oaddress,
                'phone': self.phone,
                'mobile': self.mobile,
                'email': self.email,
                'note': self.notes,
                'is_company':0,
                'is_company_customer':-10,
                'is_bank_customer':-1,
                'client_guarantor':'customer',
                'birthday':self.birthday,
                
            }
            #print"-------partner_id-------",self.partner_id
            #print"-------partner_id-------",partner_vals
            
                
            
            #print"-------partner_id-------",partner_id      
        if self.is_company_customer ==-20:

            if self.partner_id:
                no_accoun=self.partner_id.account_id
            else:
                no_accoun=""
                select_sql_clause = """SELECT count(id)  as no_accoun from res_partner where is_bank_customer=-1"""
                    
                self.env.cr.execute(select_sql_clause)
                query_results = self.env.cr.dictfetchall()
                print query_results, "----------------------------",query_results[0].get('no_accoun'),len(query_results)
                if query_results[0].get('no_accoun') != None:
                    if query_results[0].get('no_accoun') != None:
                        no_accoun=str(query_results[0].get('no_accoun')+1) 
                    else:
                        no_accoun='Null'

                while len(no_accoun)<6:
                    no_accoun='0' + no_accoun

                m           = 1
                shuma_total = 0
                shuma = 0
                for index in range(0, len(no_accoun)):
                    shifra_kodi_llogari = int(no_accoun[index: index+1])

                    shuma       = shifra_kodi_llogari*m
                    shuma_total = shuma_total + shuma
                    if m == 1:
                        m = 2
                    else:
                        m = 1

                #kapet mbetja ---------------------------------------------------------------
                shifra_e_fundit=0L
                mbetja=0L
                mbetja = math.fmod(shuma_total, 10)
                if mbetja == 0:
                    shifra_e_fundit = 0
                else:
                    shifra_e_fundit = int(10 - mbetja)                      
                #------------------------------------------------------------------------------

                #hequr no_accoun = no_accoun + str(shifra_e_fundit)
                self.account_id1=no_accoun


            partner_vals = {
                
                'branch_id': self.branch_id.id,
                'sub_branch_id': self.sub_branch_id.id,
                'name': self.name,
                'national_id': self.national_id,
                'detail_name_com': self.detail_name_com,
                'account_id': no_accoun,
                'birth_country': self.birth_country.id or '',
                'city_id': self.city_id.id or '',
                'national_id_type': self.national_id_type or '',
                'document_client_id': self.document_client_id or '',
                'date_release': self.date_release,
                'country_issuance': self.country_issuance.id or '',
                
                'citizenship': self.citizenship or '',    
                'date_expiry': self.date_expiry,
                'customer_type_name': self.customer_type_name or '',
                'industry_sector': self.industry_sector or '',
                'industry_group': self.industry_group or '',
                'industry_code': self.industry_code or '',
                'country_id': self.country_id.id or '',
                'district_id': self.district_id.id or '',
                'municipality': self.municipality.id or '',
                'city_village': self.city_village.id or '',
                'street': self.street,
                'street2': self.oaddress,
                'phone': self.phone,
                'mobile': self.mobile,
                'email': self.email,
                'note': self.notes,
                'is_company':1,
                'is_company_customer':-20,
                'is_bank_customer':-1,
                'client_guarantor':'customer',
                'birthday':self.birthday,
                
                
            }
            #'id':self.partner_id.id,
            #print"-------partner_id-------",self.partner_id
        
        if self.partner_id:
            self.partner_id.write(partner_vals)
            print"-------partner_id-------",self.partner_id.id
            self.write({'user_authorize_id': self._uid,'account_id1':no_accoun, 'authorize_date': datetime.now(),'partner_id':self.partner_id.id, 'user_update_id': self._uid, 'update_date':datetime.now()})
        else:    
            partner_id = self.env['res.partner'].create(partner_vals)
            self.write({'user_authorize_id': self._uid,'account_id1':no_accoun, 'authorize_date': datetime.now(),'partner_id':partner_id.id, 'user_update_id': self._uid, 'update_date':datetime.now()})
        
       
            #print"-------partner_id-------",partner_id
            #print"-------partner_id-------",partner_vals
        ###print"-------partner_id-------",self.partner_id
        ###print"-------partner_id-------",self.partner_id.id
        ###print"-------partner_id-------",partner_id
        #print"-------partner_id-------",partner_id.id

        
        
    @api.multi
    def action_return_data(self):
        self.write({'state': 'draft','user_update_id': self._uid,'update_date':datetime.now()})
    

    @api.multi
    def action_reject(self):
        self.write({'state': 'reject','user_update_id': self._uid})

    
    
class other_name(models.Model):
    _name = "other.name"
    _rec_name = "name"  
    
    
    name = fields.Char('Name:' ,required=True)
    ppuse = fields.Char('Purpose Use:' )
    prelim_id = fields.Many2one('prelim.app', string='Prelim App:')
    
class contact_company(models.Model):
    _name = "contact.company"
    _rec_name = "name"  
    
    
    position = fields.Char('Position:' ,required=True)
    name = fields.Char('Name:' ,required=True)
    pk = fields.Selection([('yes','YES'), ('no','NO')],string='PK?:' )
    wire = fields.Char('Wire:' )
    document = fields.Char('Fax:' )
    email = fields.Char('Email:' )
    note = fields.Text('Notes:' )
    prelim_com_id = fields.Many2one('prelim.app', string='Prelim App:')
    
class phone_record(models.Model):
    _name = "phone.record"
    _rec_name = "nrte"  
    
    
    nrte = fields.Char(string='Nr.Tel:' ,required=True)
    descp = fields.Char('Description:' )
    prelim_id = fields.Many2one('prelim.app', string='Prelim App:')
    
        
class guarentee_record(models.Model):
    _name = "guarantee.record"
    _rec_name = "guarantee"  
    
    
    guarantee = fields.Char('Guarantee:' ,required=True)
    value_guarantee = fields.Char('Value Guarantee:' ,required=True)
    prelim_id = fields.Many2one('prelim.app', string='Prelim App:')
    

        
#class res_partner_extention(osv.osv):

    #_inherit = 'res.partner'

    #def name_get(self,cr,uid,ids,context=None):
        #result = {}
        #for partner in self.browse(cr,uid,ids,context=context):
            #result[partner.id] = partner.name + " " + partner.lastname

        #return result.items()       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        