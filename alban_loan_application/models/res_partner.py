from odoo import models, fields, api, _
import math

import logging
from odoo.osv import expression
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = 'res.partner'
    _order = 'account_id'
    # _rec_name = 'account_id'

    #these are wrong
        
    #prelim_app_id = fields.Many2one('prelim.app', string='Preliminary Application')   
    #collateral_id = fields.Many2one('prelim.app', string='Collateral')   
    #collateral_type = fields.Selection([('property', 'Property'), ('mortgage', 'Mortgage'),
    # ('bank_account', 'Bank Account'), ('insurance', 'Insurance Company')], string="Collateral Type")   
    #loan_app_id = fields.Many2one('loan.app', string='Loan Application')
    #individual = fields.Boolean(string="Individual") 
    #company = fields.Boolean(string="Company") 
    #check_box = fields.Boolean(string="Check")



    branch_id = fields.Many2one('admin.branch', string='Branch', required=True)
    sub_branch_id = fields.Many2one('admin.sub.branch', string='Sub Branch' ,required=True)
    state = fields.Selection([('draft','Draft'),('monitor','Monitor') , ('approve','Approve') ],default='draft')

    # ------ base_num_id = fields.Many2one('base.number', string='Base Number') 
    is_company = fields.Boolean(string="Check") 
    is_company_customer=fields.Integer(string="CheckCompany")
    is_bank_customer=fields.Integer(string="Bank Customer")
    client_guarantor = fields.Selection([('customer', 'Customer'), ('guarantor', 'Guarantor')], string="Client/Guarantor", required=True)
    
    # ------ vat = fields.Char('VAT Number', required=True)
    
    #create_date = fields.Date('Date created', required=True)
    
    
    #Client Profile
    
    fathername = fields.Char('Father Name' , required =True)
    lastname = fields.Char('Last Name', required=True )
    
    maiden_name = fields.Char('Maiden Name')
    last_name_bef= fields.Char(string='Last Name Before Marriage')
    preferedname= fields.Char('Prefered Name')
    detail_name_com = fields.Char('Detail Name')
    account_id = fields.Char('Account Id', required=False)
	
    birth_country = fields.Many2one('res.country', string='Country of Birth', required=True)
    city_id = fields.Many2one('admin.city', string='City of Birth', required=True)

    
    gender = fields.Selection([('M', 'Man'), ('W', 'Woman')], string="Gender", required=True)
    national_id_type = fields.Selection([
    										('certificate', 'Certificate'), 
    										('biometric', 'Identification Card / Biometric Password'),
     										('identity_card', 'Identity Card Old'), 
     										('passport', 'Passport Old'),
     										('license', 'Driving License')], 
     				   string="Type", required=True)
    
    national_id= fields.Char('National id' , required=True) 
    document_client_id=fields.Char('Document Id' , required=True)
    date_release = fields.Date('Release Date', required=True)
    country_issuance = fields.Many2one('res.country', string='Country of Issuance', required=True)
    citizenship = fields.Selection([('foreign', 'Foreign'), ('albania', 'Albania')], string="Citizenship", required=True)
    birthday = fields.Date('Birth Date' , required=True)
    date_expiry = fields.Date('Expiration Date', required=True)
    # country_id = fields.Many2one('res.country', string='Circle:', required=True)
    country_id = fields.Many2one('res.country', string='Country')
    # district_id = fields.Many2one('admin.district', string='District:',required=True)
    district_id = fields.Many2one('admin.district', string='District')
    # municipality = fields.Many2one('admin.municipal', string='Municipalities/Municipality:', required=True)
    municipality = fields.Many2one('admin.municipal', string='Municipality',)
    # city_village = fields.Many2one('admin.village', string='City/Village:', required=True)
    city_village = fields.Many2one('admin.village', string='City/Village',)

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
    #                ('viticulture','Viticulture')],string='Industry Sector',required=True)
    
    industry_sector = fields.Selection([('trade','Trade'), ('agriculture','Agriculture'), 
                    ('animal_husbandry','Animal Husbandry'), ('manufacturing','Manufacturing'),
                    ('services','Services'), ('trade','Trade'), ('unknown','Unknown')],string='Industry Sector',required=True)
        #    industry = fields.Char('Industry:' ,required=True)
    #industry_group = fields.Selection([('handicraft','HANDICRAFT'), ('livestock','AGRICULTURE & LIVESTOCK'), 
    #                ('industry','INDUSTRY'), ('consumer','CONSUMER'),
    #                ('construction','CONSTRUCTION'), ('service','SERVICES'),
    #                ('transport','TRANSPORT'), ('trade','TRADE'),
    #                ('tourism','TOURISM')],string='Industry Group',required=True)
    industry_group = fields.Selection([('ac','A- Crops'),('ao','A- Other'),('a','A-Bujqesi'), 
                    ('an','AN-Blegtori'), ('anl','AN- Livestock'),('ano','AN- Other'),('anp','AN- Poultry'),
                    ('cw','C-Konsum CWBO'), ('c','C-Konsum'), ('h','H-Housing'),
                    ('p','P-Prodhim'), ('pd','P- Dairy'), ('pf','P- Food'), ('po','P- Other'), ('pw','P- Wood-Related'), 
                    ('s','S-Sherbim'), ('sb','S- Bar/Rest'),('sc','S- Construction'),('sm','S -Media & Com.'),
                    ('so','S- Other'),('st','S- Transport'),('sp','S- Prof Trade'),
                    ('t','T-Tregti'), ('to','T- Other'),('ts','T- Shops Retail'),('tsh','T- Shops Whole.'),('unknown','Unknown')
                    ],string='Industry Group',required=True)

    #industry_code = fields.Selection([('a','A-Bujqesi'), ('an','AN-Blegtori'), 
    #                ('cw','C-Konsum CWBO'), ('c','C-Konsum'), ('h','H-Housing'),
    #                ('p','P-Prodhim'), ('s','S-Sherbim'), ('t','T-Tregti'), 
    #                ],string='Industry Code',required=True)
    industry_code = fields.Selection([('unknown','Unknown') 
                    ],string='Industry Code',required=True)


    #industry_group = fields.Selection([
    #    ('A',       'AGRICULTURE, FORESTRY AND FISHING'),
    #    ('B',       'MINING AND QUARRYING' ),
    #    ('C',       'MANUFACTURING' ),
    #    ('D',       'ELECTRICITY, GAS, STEAM AND AIR CONDITIONING SUPPLY' ),
    #    ('E',       'WATER SUPPLY; SEWERAGE, WASTE MANAGEMENT AND REMEDIATION ACTIVITIES'), 
    #    ('F',       'CONSTRUCTION' ),
    #    ('G',       'WHOLESALE AND RETAIL TRADE; REPAIR OF MOTOR VEHICLES AND MOTORCYCLES' ),
    #    ('H',       'TRANSPORTATION AND STORAGE' ),
    #    ('I',       'ACCOMMODATION AND FOOD SERVICE ACTIVITIES' ),
    #    ('J',       'INFORMATION AND COMMUNICATION' ),
    #    ('K',       'FINANCIAL AND INSURANCE ACTIVITIES' ),
    #    ('L',       'REAL ESTATE ACTIVITIES' ),
    #    ('M',       'PROFESSIONAL, SCIENTIFIC AND TECHNICAL ACTIVITIES' ),
    #    ('N',       'ADMINISTRATIVE AND SUPPORT SERVICE ACTIVITIES' ),
    #    ('O',       'PUBLIC ADMINISTRATION AND DEFENCE; COMPULSORY SOCIAL SECURITY' ),
    #    ('P',       'EDUCATION'),
    #    ('Q',       'HUMAN HEALTH AND SOCIAL WORK ACTIVITIES' ),
    #    ('R',       'ARTS, ENTERTAINMENT AND RECREATION' ),
    #    ('S',       'OTHER SERVICE ACTIVITIES') ,
    #    ('T',       'ACTIVITIES OF HOUSEHOLDS AS EMPLOYERS; UNDIFFERENTIATED GOODS- AND SERVICES-PRODUCING ACTIVITIES OF HOUSEHOLDS FOR OWN USE' ),
    #    ('U',       'ACTIVITIES OF EXTRATERRITORIAL ORGANISATIONS AND BODIES')],string='Industry Group',required=True)

    # street = fields.Char('Street:', required=True)
    # ------ street = fields.Char('Street', )
    # ------ mobile = fields.Char('Mobile', )
    # ------ phone = fields.Char('Phone')
    # ------ fax = fields.Char('Fax')
    note = fields.Text('Notes', required=True)
    black_list = fields.Selection([('no', 'No'), ('yes', 'Yes')], string="Black List", required=True)

    _sql_constraints = [
        ('account_id_uniq_1', 'unique(account_id)', 'The Customer Account ID should be unique !!!')

    ]


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            # (((A or B) or C) or D)
            # [ '|', '|', A, B, C ] <== ((A OR B) OR C)
            # [ '|', A, '|', B, C ] <== (A OR (B OR C))
            domain = ['|','|','|', ('name', '=ilike', name + '%'), ('lastname', operator, name), ('account_id', operator, name), ('fathername', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
                #print  args,domain
        partners = self.search(domain + args, limit=limit)
        #print  args,domain
        return partners.name_get()


    @api.depends('account_id','name', 'fathername','lastname','detail_name_com')
    def name_get(self):
        result = []
        name=''
        for partner in self:
            name = str(partner.account_id) + ' ' + str((partner.name).encode('utf-8')) \

            if partner.fathername:
                name += ", " + str((partner.fathername).encode('utf-8'))
            if partner.lastname:
                name += " " + str((partner.lastname).encode('utf-8'))
            #if partner.detail_name_com:
             #   name += " " + str((partner.detail_name_com).encode('utf-8'))

            if partner.detail_name_com:
                name += " " + str((partner.detail_name_com).encode('utf-8'))


            result.append((partner.id, name))
        return result

    #@api.onchange('state')
    #def onchange_state(self):
        #self.write({'state': 'approve'})

    ###@api.model
    ###def name_get(self):
        #res={}
        ###print "fuck here"
        
        ###val = {}
        
        #student_obj = self.pool.get('res.partner')
        #student_data = student_obj.browse()
        #val.update({'id': [ g.id for g in student_data.groups_ids ]})
        ###res = [('7', 'alban'), ('3','kokalari')]
        ###return res




        #print self.browse
        #for record in self.browse():
        #        print record
        #        name = record.name
        #        fathername = record.fathername

        #        lastname = record.lastname
        #        res.append(record.id, name + ", " + fathername + " " + lastname)
        #res = {
                
        #        1,"test"}

        
        #res.append(2, "Alban" + ", " + "Hulusi1" + " " + "Kokalari")
        #res.append(3, "Alban" + ", " + "Hulusi2" + " " + "Kokalari")
        #return res

    

    @api.multi
    def action_approve(self):
        self.write({'state': 'approve'})
        
    @api.multi
    def action_submit(self):
        if len(self.account_id)<=6:
            no_accoun=""

            select_sql_clause = """SELECT count(id)  as no_accoun from res_partner where is_bank_customer=-1"""
            self.env.cr.execute(select_sql_clause)
                    
            query_results = self.env.cr.dictfetchall()
            print query_results, "----------------------------",query_results[0].get('no_accoun'),len(query_results)
            if query_results[0].get('no_accoun') != None:
                if query_results[0].get('no_accoun') != None:
                    no_accoun=str(query_results[0].get('no_accoun')) 
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

            self.write({'state': 'monitor','account_id': no_accoun})
        else:
            self.write({'state': 'monitor'})
        
    #@api.multi
    #def action_collateral(self):
        #self.write({'state': 'collateral'})
        
    #@api.multi
    #def action_monitor_collateral(self):
        #self.write({'state': 'monitor_collateral'})

    @api.model
    def create(self, vals):
        res = super(res_partner, self).create(vals)
        acc_id = self.account_id

        # flag = False
        if acc_id:
            res_id = self.search([])
            for ids in res_id:
                if ids == self:
                    pass
                else:
                    if acc_id == ids.account_id:
                        raise UserError(_('The Customer Account ID already exists!!! Please Enter a new one!!!!'))
                # if acc_id == ids.account_id:
                #
                #     raise UserError(_('The Customer Account ID already exists!!! Please Enter a new one!!!!'))
                #

        return res

    @api.multi
    def write(self, vals):
        res = super(res_partner, self).write(vals)
        _logger.info('=====================res %s======================' % res)
        acc_id = self.account_id
        if acc_id:
            # res_id = self.search([('account_id','=',acc_id.strip(' '))])
            res_id = self.search([])
            _logger.info('=====================res_id %s======================'%res_id )
            for ids in res_id:
                if ids == self:
                    pass
                else:
                    if acc_id == ids.account_id:
                        raise UserError(_('The Customer Account ID already exists!!! Please Enter a new one!!!!'))

            # if res_id:
            #     raise UserError(_('The Customer Account ID already exists!!! Please Enter a new one!!!!'))
            # for ids in res_id:
            #     if acc_id == ids.account_id:
            #         raise UserError(_('The Customer Account ID already exists!!! Please Enter a new one!!!!'))
        # res = super(res_partner, self).write(vals)

        return res


class res_users(models.Model):
    _inherit = 'res.users'
    
    
    branch_id = fields.Many2one('admin.branch', string='Branch')
    sub_branch_id = fields.Many2one('admin.sub.branch', string='Sub Branch')
    

