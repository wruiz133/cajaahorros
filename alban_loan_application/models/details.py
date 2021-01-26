from odoo import models, fields, api

class loan_application(models.Model):
    _inherit = "loan.application"
    # ========================fields for company
    # company_name = fields.Char(string='Company Name',required=True)
    company_name = fields.Char(string='Company Name')

    # type_of_business = fields.Char(string='Type Of Business',)
    type_of_business = fields.Selection([('anonime','ANONIME'), ('private','PRIVATE'),
       ('sh_pk','SH.PK'), ('joint_stock','JOINT-STOCK COMPANY')
       ,('other','OTHERS')],string='Company Type',)

    legal_status = fields.Char(string='Legal Status',)
    # company_type = fields.Selection(string='Company Type',required=True)
    # company_type = fields.Char(string='Company Type',)
    # sector = fields.Selection([('consumer','Consumer')],string='Sector',)
    
    industry_group = fields.Selection([('ac','A- Crops'),('ao','A- Other'),('a','A-Bujqesi'), 
                    ('an','AN-Blegtori'), ('anl','AN- Livestock'),('ano','AN- Other'),('anp','AN- Poultry'),
                    ('cw','C-Konsum CWBO'), ('c','C-Konsum'), ('h','H-Housing'),
                    ('p','P-Prodhim'), ('pd','P- Dairy'), ('pf','P- Food'), ('po','P- Other'), ('pw','P- Wood-Related'), 
                    ('s','S-Sherbim'), ('sb','S- Bar/Rest'),('sc','S- Construction'),('sm','S -Media & Com.'),
                    ('so','S- Other'),('st','S- Transport'),('sp','S- Prof Trade'),
                    ('t','T-Tregti'), ('to','T- Other'),('ts','T- Shops Retail'),('tsh','T- Shops Whole.'),('unknown','Unknown')
                    ],string='Industry Group',required=False)
    industry_sector = fields.Selection([('trade','Trade'), ('agriculture','Agriculture'), 
                    ('animal_husbandry','Animal Husbandry'), ('manufacturing','Manufacturing'),
                    ('services','Services'), ('trade','Trade'), ('unknown','Unknown')],string='Industry Sector',required=False)
    industry_code = fields.Selection([('unknown','Unknown') 
                    ],string='Industry Code',required=False)

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
    #                ('various_repairs','Various repairs'), ('cattle_growing','Cattle Growing of fine'),
    #                ('cattle_breeding','Cattle Breeding'), ('poultry','Poultry Growing'),
    #                ('seamstress','Seamstress'), ('sere','Sere'),
    #                ('agri_land','Agricultural land'), ('retail','Retail'),
    #                ('wholesale_trade','Wholesale Trde'), ('olive_groves','Olive groves'),
    #                ('viticulture','Viticulture')],string='Industry Sector',required=True)
        #    industry = fields.Char('Industry:' ,required=True)
    #industry_group = fields.Selection([('handicraft','HANDICRAFT'), ('livestock','AGRICULTURE & LIVESTOCK'), 
    #                ('industry','INDUSTRY'), ('consumer','CONSUMER'),
    #                ('construction','CONSTRUCTION'), ('service','SERVICES'),
    #               ('transport','TRANSPORT'), ('trade','TRADE'),
    #                ('tourism','TOURISM')],string='Industry Group',required=True)
    #industry_code = fields.Selection([('code1','Code1'), ('code2','Code2'), 
    #                ],string='Industry Code',required=True)
    bus_ownership = fields.Selection([('partnrshp','Partnership'),('join','Join'),('other','Other')],string='Business Ownership')
    # bus_ownership = fields.Char(string='Business Ownership')

    tin_no = fields.Char(string='TIN')
    date_of_create = fields.Date(string='Date Of Creation' )
    no_of_licence = fields.Integer(string='Number of Licenses')
    date_of_license = fields.Date(string='Date Of License')
    no_of_owners = fields.Integer(string='Number of Owners')
    no_of_employees = fields.Integer(string='Number of Employees')
    business_env= fields.Selection([('with_rent','With Rent'),('ownership','Ownership'),
                                    ('own_part','Ownership Of Partner'),('other','Other')],string='Business Environment')
    # business_env = fields.Char(string='Business Environment')

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
    id_num = fields.Char(string='Id Number')
    issue_date = fields.Date(string='Issue Date')
    expiry_date = fields.Date(string='Expiry Date')
    # reg_date1 = fields.Date(string='Registration Date')
    begin_act_date = fields.Date(string='Date of Begin Activity')


    date_incopr = fields.Date(string='Date')
    capital = fields.Float(string='Capital')
    net_worth = fields.Float(string='Net Worth')
    country_1 = fields.Many2one('res.country', string='Country')
    currency_amt = fields.Many2one('res.currency',string='Currency Amount', help='Utility field to express amount currency')



    add_line1 = fields.Char(string='Address Line 1')
    add_line2 = fields.Char(string='Address Line 2')
    city_add = fields.Char(string='City')
    country_add = fields.Many2one('res.country', string='Country ')


    placement_date =  fields.Date(string='Placement Date' )
    auditors = fields.Char(string='Auditors')
    tel_auditor = fields.Char(string='Tel Auditors')



class income_details(models.Model):
    _name = "income.details"

    income_type= fields.Selection([('salary','Salary'),('rent','Rent'),('business','Business'),('others','Others')],string='Income Type')
    income_sub_type = fields.Char(string='Income Sub type')
    unit = fields.Char(string='Unit')
    qty =  fields.Integer(string='Quantity')
    currency = fields.Many2one('res.currency', help='Utility field to express amount currency')
    amt = fields.Float(string='Amount')
    freq = fields.Selection([('daily','Daily'),('weekly','Weekly'),('monthly','Monthly'),('quarterly','Quarterly'),('half_yearly','Half Yearly'),('yearly','Yearly')],string='Frequency')
    # grp_id = fields.Selection('Group Id')
    # grp_id = fields.Char(string='Group Id')
    grp_id = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D'),('e','E')],string='Group Id')
    total_value = fields.Float(string='Total Value')
    income_det_id = fields.Many2one('loan.application',string='Income Details')




class liability_details(models.Model):
    _name = "liability.details"

    liability_type = fields.Selection([('loan', 'Loan'), ('lease', 'Lease'), ('rent', 'Rent'), ('others', 'Others')], string='Liability Type')
    liability_sub_type = fields.Char(string='Liability Sub type')
    unit = fields.Char(string='Unit')
    qty = fields.Integer(string='Quantity')
    freq = fields.Selection([('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
         ('half_yearly', 'Half Yearly'), ('yearly', 'Yearly')], string='Frequency')
    amt = fields.Float(string='Amount')
    acct_bal = fields.Float(string='Account Balance')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    # grp_id = fields.Selection('Group Id')
    grp_id = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D'),('e','E')],string='Group Id')
    total_value = fields.Float(string='Total Value')
    liab_detail_id = fields.Many2one('loan.application',string='Liability Details')


class loan_application(models.Model):
    _inherit = 'loan.application'

    asset_det_ids =fields.One2many('asset.details','asset_det_id',string='Asset Details')
    # seq_no5 = fields.Char(string='Sequence No.', default=lambda self: self.env['ir.sequence'].next_by_code('loan.application5'))
    income_det_ids =fields.One2many('income.details','income_det_id',string='Income Details')
    liab_detail_ids =fields.One2many('liability.details','liab_detail_id',string='Liability Details')


    cli_supp_ids =fields.One2many('cli.supp.information','cli_supp_id',string='Client Supplier Details')
    asset_info_ids =fields.One2many('asset.information','asset_info_id',string='Asset Information ')
    annual_ids =fields.One2many('lease.factoring.annual','annual_id',string='Annual Turnover')
    asset_ids =fields.One2many('lease.factoring.assets','asset_id',string='Assets')
    equity_ids =fields.One2many('lease.factoring.equity','equity_id',string='Equity')
    acc_pay_ids =fields.One2many('lease.factoring.acc.pay','acc_pay_id',string='Account Payable')

    comp_share_ids =fields.One2many('company.shareholder','comp_share_id',string='Account Payable')

    tran_loan_ids =fields.One2many('multi.transaction.loan','tran_loan_id',string='Multi Transaction Loan')

    # asset_issure
    pref_ins_comp = fields.Selection([('sigal','Sigal'),('eurosig','Eurosig'),('intersig','Intersig'),('others','Others')],
                                     string='Preferred Insurnace Company',default ='sigal' )
    others =fields.Char(string='Others')

# ============================new financial tab ===================
    fixed_asset = fields.Char(string='Fixed Assets')
    intan_asset = fields.Char(string='Intangible Assets')
    non_cur_asset = fields.Char(string='Non-Current Assets')
    cur_asset = fields.Char(string='Current Assets')

    cr_bal = fields.Float(string='Credit Balance in P')

    borrow_profile = fields.Char(string='Borrower Profile')
    borrow_pos = fields.Char(string='Borrower Market Position')
    fin_perform = fields.Char(string='Financial Performance')
    risk_mig = fields.Char(string='Risk and Migrants')
    risk_dept_mig = fields.Char(string='Risk Department Migrants')
    risk_dept_asmt = fields.Char(string='Risk Department Assessment')
    fac_prop = fields.Char(string='Facilities Proposed')
    app_fac = fields.Char(string='Approved Facilities')
    recom = fields.Char(string='Recommended')
    term_cond = fields.Text(string='Terms and Conditions')


    issued_cap = fields.Float(string='Issued Capital')
    paid_cap = fields.Float(string='Paid up Capital')

    term_liab = fields.Char(string='Term Liabilities')
    curr_liab = fields.Char(string='Current Liabilities')

    subsidy_gov = fields.Float(string='Subsidy from Government')
    gen_reserve = fields.Float(string='General Reserves')

    oper_act = fields.Float(string='Operation Ativities')
    invest_act = fields.Float(string='Investing Ativities')
    fin_act = fields.Float(string='Financing Ativities')
    # ===================================================================
# ============================new requested tab ===================
    nr_invoice_req = fields.Float(string='Nr. of Invoices to be financed')
    inv_desc_req =fields.Text(string='Invoices Description')
    buyer_dir_req =fields.Char(string='Buyers(Direct Factoring)')
    supplier_rev_req =fields.Char(string='Supplier(Reverse Factoring)')
    invoice_amt = fields.Float(string='Invoices Amount')
    percent_req = fields.Float(string='Percentage %')

    obj_fin = fields.Char(string='Object to be Financed')
    obj_desc_req = fields.Char(string='Object Description,Type ,Model')
    supp_req = fields.Char(string='Supplier')
    exp_del_date = fields.Date(string='Expected Delivery Date ')
    asset_price = fields.Float(string='Asset Price')
    percent_req1 = fields.Float(string='Percentage%')
    percent_req2 = fields.Float(string='Percentage%')
    amount = fields.Float(string='Amount')

    tendor_months = fields.Integer(string='Tendor (in months)')
    terms_usage =fields.Text(string='Term Of Usage')
#     ======================================================================

# ============================for changed financing=========================

class company_shareholder(models.Model):
    _name = 'company.shareholder'

    comp_share = fields.Char(string='Loans Company and Shareholders')

    institute = fields.Char(string='Institution')
    type_loan = fields.Char(string='Type of Loan')
    amt_currency =fields.Many2one('res.currency',string='Amount Currency')
    intrst_rate =fields.Float(string='Interest Rate')
    start_date = fields.Date(string='Starting Date ')
    tendor = fields.Integer(string='Tendor')
    instl_amt = fields.Float(string='Installment Amount')

    comp_share_id =fields.Many2one('loan.application')
# ==============================================================================

# =====================for multi-transaction loan===============================
class multi_transaction_loan(models.Model):
    _name = 'multi.transaction.loan'

    sr_no = fields.Integer(string='Sr No.')
    amount = fields.Float(string='Amount')
    date = fields.Date(string='Date ')
    notes =fields.Text(string='Notes')

    tran_loan_id = fields.Many2one('loan.application')


class asset_details(models.Model):
    _name = "asset.details"

    type = fields.Selection([('vehicle', 'Vehicle'), ('home', 'Home'), ('others', 'Others')], string='Type')
    asset_sub_type = fields.Char(string='Asset Sub type')
    desc = fields.Char(string='Description')
    asset_value = fields.Float(string='Asset Value')
    make = fields.Char(string='Make')
    model = fields.Char(string='Model')
    man_yr = fields.Integer(string='Manufacture Year')
    body = fields.Char(string='Body')
    reg_no = fields.Char(string='Reg#')

    add_line1 = fields.Char(string='Address Line 1')
    add_line2 = fields.Char(string='Address Line 2')
    add_line3 = fields.Char(string='Address Line 3')
    width = fields.Float(string='Width')
    length = fields.Float(string='Length')
    occupancy = fields.Integer(string='Occupancy')

    asset_det_id = fields.Many2one('loan.application',string='Asset Details')



#     ==========================for leasing/factoring tab=========================

class lease_factoring_annual(models.Model):
    _name = "lease.factoring.annual"

    annual_turn = fields.Float(string='Annual Turnover')
    curr_year = fields.Float(string='Current Year')
    prev_year = fields.Float(string='Previous Year')
    two_year_ago = fields.Float(string='2 Years ago')

    annual_id = fields.Many2one('loan.application',string='Annual Turnover')

class lease_factoring_assets(models.Model):
    _name = "lease.factoring.assets"

    assets = fields.Float(string='Assets')
    curr_year = fields.Float(string='Current Year')
    prev_year = fields.Float(string='Previous Year')
    two_year_ago = fields.Float(string='2 Years ago')

    asset_id = fields.Many2one('loan.application',string='Assets')

class lease_factoring_equity(models.Model):
    _name = "lease.factoring.equity"

    equity = fields.Float(string='Equity')
    curr_year = fields.Float(string='Current Year')
    prev_year = fields.Float(string='Previous Year')
    two_year_ago = fields.Float(string='2 Years ago')

    equity_id = fields.Many2one('loan.application',string='Assets')

class lease_factoring_acc_pay(models.Model):
    _name = "lease.factoring.acc.pay"

    acc_pay = fields.Float(string='Account Payable')
    curr_year = fields.Float(string='Current Year')
    prev_year = fields.Float(string='Previous Year')
    two_year_ago = fields.Float(string='2 Years ago')

    acc_pay_id = fields.Many2one('loan.application',string='Assets')

# ========for client/supplier information========
class cli_supp_information(models.Model):
    _name = "cli.supp.information"

    client = fields.Char(string="Clients")
    supp = fields.Char(string="Suppliers")

    cli_supp_id = fields.Many2one('loan.application',string='Client/Suppliers')

# =========for asset information=========
class asset_information(models.Model):
    _name = "asset.information"

    company_asset = fields.Char(string="Company's Assets")
    value1 = fields.Float(string='Value')
    personal_asset = fields.Char(string="Personal Assets")
    value2 = fields.Float(string='Value')

    asset_info_id = fields.Many2one('loan.application', string='Client/Suppliers')








