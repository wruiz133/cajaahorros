from odoo import models, fields, api
import math

class base_number(models.Model):
    _name = "base.number"
    _rec_name = "account_id"

    branch_id = fields.Many2one('admin.branch', string='Branch', required=True)
    sub_branch_id = fields.Many2one('admin.sub.branch', string='Sub Branch' ,required=True)
    individual = fields.Boolean(string="Individual") 
    company = fields.Boolean(string="Company") 
    if individual==True:
    	client_guarantor = fields.Selection([('customer', 'Customer'), ('guarantor', 'Guarantor')], string="Client/Guarantor")
    else:
    	client_guarantor = fields.Selection([('company', 'Company'), ('guarantor', 'Guarantor')], string="Company/Guarantor")
   
    state = fields.Selection([('draft','Draft'), ('monitor','Monitor'), ('approve','Approve')],default='draft')
    
    tin = fields.Char('TIN:')
    brief_name = fields.Char('Brief Name')
    create_date = fields.Date('Date created')
    
    name = fields.Char('Name')
    fathername = fields.Char('Fathername')
    lastname = fields.Char('Last Name')
    birthday = fields.Date('Birthday')
    account_id = fields.Char('Account ID', required=False)
    mnemnonic = fields.Char('Mnemonic')
    birth_circle = fields.Many2one('res.country', string='Circle Of Birth')
    gender = fields.Selection([('man', 'Man'), ('woman', 'Woman')], string="Gender")
    phone = fields.Char('Personal Number')
    base_type = fields.Selection([('certificate', 'Certificate'), ('identity', 'Identification Card / Biometric Password'),
     ('identity_card', 'Identity Card'), ('passport', 'Passport'),
     ('license', 'Driving License')], string="Type")
    logari = fields.Char('Nr.Llogari')
    date_release = fields.Date('Release Date')
    country_issuance = fields.Many2one('res.country', string='Country of Issuance')
    citizenship = fields.Selection([('foreign', 'Foreign'), ('albania', 'Albania')], string="Citizenship")
    date_expiry = fields.Date('Expiration Date')
    country_id = fields.Many2one('res.country', string='Circle')
    municipality = fields.Many2one('admin.municipal', string='Municipalities/Municipality')
    city_village = fields.Many2one('admin.village', string='City/Village')
    street = fields.Char('Street')
    telefoni_1 = fields.Char('Nr.Telefoni 1')
    telefoni_2 = fields.Char('Nr.Telefoni 2')
    telefoni_3 = fields.Char('Nr.Telefoni 3')
    note = fields.Text('Notes')
    black_list = fields.Selection([('no', 'NO'), ('yes', 'YES')], string="Black List")
    comment = fields.Text('Notes')

    _sql_constraints = [
        ('account_id_uniq', 'unique(account_id)', 'The Customer Account ID should be unique !!!')
    ]

    @api.multi
    def action_submit(self):
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

        no_accoun = no_accoun + str(shifra_e_fundit)

        self.write({'state': 'monitor','account_id': no_accoun})
        
    @api.multi
    def action_approve(self):
        self.write({'state': 'approve'})
        
#    @api.model
#    def default_get(self, fields):
#        print"------self--------",self
#        print"------fields--------",fields
#        rec = super(base_number, self).default_get(fields)
#        context = dict(self._context or {})
#        active_model = context.get('active_model')
#        active_ids = context.get('active_ids')
#        prelim_id = self.env[active_model].browse(active_ids)
#        print"------prelim_id--------",prelim_id
#        rec.update({
#            'identity' :  prelim_id.identity,
#            'branch_id' :  prelim_id.branch_id.id,
#            'name' :  prelim_id.name,
#            'fathername' :  prelim_id.fathername,
#            'sur_name' :  prelim_id.sur_name,
#            'birthdate' :  prelim_id.birthdate,
#            'account_id' :  prelim_id.account_id,
#            'mnemnonic' :  prelim_id.mnemnonic,
#            'birth_circle' :  prelim_id.birth_circle.id,
#            'gender' :  prelim_id.gender,
#            'circle' :  prelim_id.circle.id,
#            'municipality' :  prelim_id.municipality.id,
#            'city_village' :  prelim_id.city_village.id,
#            'street' :  prelim_id.street,
#            'telefoni_1' :  prelim_id.nrt,
#            'black_list' :  prelim_id.black_list,
#            'tin' :  prelim_id.tin,
#            'brief_name' :  prelim_id.short_name,
#        })
#        return rec