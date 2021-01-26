from odoo import api, fields, models, _


class admin_branch(models.Model):
    _name ='admin.branch'
    _rec_name = "branch_name"

    branch_name=fields.Char(string='Branch:')
    accounting_no=fields.Char(string='Accounting No:')
    sub_branch_ids = fields.One2many('admin.sub.branch', 'branch_id' ,string='Sub Branch') 


class admin_sub_branch(models.Model):
    _name = 'admin.sub.branch'
    _rec_name = "desig_sub_branch"
    
    branch_id= fields.Many2one('admin.branch',string="Branch:")
    desig_sub_branch = fields.Char(string='Designation Sub-Branch:')


class admin_officer(models.Model):
    _name = "admin.officer"
    _rec_name = "description"
    
    branch_id = fields.Many2one('admin.branch', string="Branch:")
    sub_branch_id = fields.Many2one('admin.sub.branch', string="Sub-Branch:")
    description = fields.Char(string=' Description:')
    status = fields.Selection([('false','0'),('true','1')],string=' Status:',default="true")


class officer_con_user(models.Model):
    _name = "officers.con.user"
    
    branch_id = fields.Many2one('admin.branch', string="Branch:")
    officer_id = fields.Many2one('admin.officer', string="Officer:")
    user_system_id = fields.Many2one('user.system', string="User System:")


class user_system(models.Model):
    _name = "user.system"

    name = fields.Char(string="User System:")


class circle_counties(models.Model):
    _name = "circle.counties"
    _rec_name = "desp_count"

    catalog = fields.Integer(string="Catalog:")
    desp_count = fields.Char(string="Description Of County:")


class admin_city(models.Model):
    _name = "admin.city"

    circle_id = fields.Many2one('res.country',string="Country:")
    city_code = fields.Integer(string="City Code:")
    name = fields.Char(string="City Name:")
    
class admin_district(models.Model):
    _name = "admin.district"

    circle_id = fields.Many2one('res.country',string="Country:")
    district_code = fields.Integer(string="District Code:")
    name = fields.Char(string="Naming District:")
    
   


class admin_municipal(models.Model):
    _name = "admin.municipal"

    district_id = fields.Many2one('admin.district', string="Name of District:")
    circle_id = fields.Many2one('res.country',string="Name The Disk:")
    district_code = fields.Integer(string="Commune Code:",size=2)
    name = fields.Char(string="Name Of Commune:")
    
   
    
    
class admin_village(models.Model):
    _name = "admin.village"

    circle_id = fields.Many2one('res.country',string="Circle:")
    district_id = fields.Many2one('admin.district', string="Name of District:")
    municipal_id = fields.Many2one('admin.municipal', string="Commune:")
    district_code = fields.Integer(string="Catalog Village:",size=2)
    name = fields.Char(string="Naming village:")
    
   
class civil_registry(models.Model):
    _name = "civil.registry"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class professional_status(models.Model):
    _name = "professional.status"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class admin_education(models.Model):
    _name = "admin.education"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class admin_marketing(models.Model):
    _name = "admin.marketing"
    
    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class admin_currencies(models.Model):
    _name = "admin.currencies"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class type_companies(models.Model):
    _name = "type.companies"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")
    
class sector_companies(models.Model):
    _name = "sector.companies"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class industries_companies(models.Model):
    _name = "industries.companies"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class custom_credit(models.Model):
    _name = "custom.credit"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class valid_ident(models.Model):
    _name = "valid.ident"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class admin_residential(models.Model):
    _name = "admin.residential"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class customer_relationship(models.Model):
    _name = "customer.relationship"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class legal_status(models.Model):
    _name = "legal.status"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class purpose_loan(models.Model):
    _name = "purpose.loan"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class type_guarantees(models.Model):
    _name = "type.guarantees"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class loan_products(models.Model):
    _name = "loan.products"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class admin_banks(models.Model):
    _name = "admin.banks"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class type_material(models.Model):
    _name = "type.material"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class property_type(models.Model):
    _name = "property.type"

    catalog = fields.Char(string="Catalog:")
    description = fields.Char(string="Description:")

    @api.depends('catalog')
    def name_get(self):
        result = []
        name=''
        for property_list in self:
            name = str(property_list.catalog)

           

            result.append((property_list.id, name))
        return result


class mortgage_type(models.Model):
    _name = "mortgage.type"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class insurance_companies(models.Model):
    _name = "insurance.companies"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class currency_exchange(models.Model):
    _name = "currency.exchange"

    date = fields.Date(string="Date:")
    currency_id = fields.Many2one("res.currency",string="Coins:")
    exeRate = fields.Integer(string="Currency Exchange at LEK:")


class document_type(models.Model):
    _name = "document.type"
    _rec_name = "description"

    ranking = fields.Integer(string="Ranking:")
    description = fields.Char(string="Description:")


class admin_documents(models.Model):
    _name = "admin.document"

    document_type_id = fields.Many2one("document.type",string="Custom:")
    description = fields.Char(string="Description:")
    ranking = fields.Integer(string="Order:", default=0);
    
    
class coll_status(models.Model):
    _name = "coll.status"

    status = fields.Char('Collateral Status')
    name = fields.Char(string="Type of Collateral")
    coll_status_ids = fields.One2many('collatoral.status','coll_status_id',string="Collateral Status",required=True)

    _sql_constraints = [
        ('col_type_uniq', 'unique(name)', 'Collateral Type should be unique !!!')
    ]


class collatoral_status(models.Model):
    _name="collatoral.status"

    name = fields.Char(string="Status Name",required=True)
    coll_status_id = fields.Many2one("coll.status")
    
    
    

#class coll_status(models.Model):
    #_name = "coll.status"

    #status = fields.Char('Collateral Status:')
    #col_type = fields.Selection([ ('non_move', 'Non-movable Property'),('move','Movable Property'), ('bank_acc', 'Bank Account'), ('insure', 'Insurance')],
    #                            string="Collateral Type")
#class collatoral_status(models.Model):
    #_name = "collatoral.status"

    #status = fields.Char('Collateral Status:')
    #col_type = fields.Selection([ ('non_move', 'Non-movable Property'),('move','Movable Property'), ('bank_acc', 'Bank Account'), ('insure', 'Insurance')],
    #                            string="Collateral Type")

class citizenship_info(models.Model):
    _name = "citizenship.info"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")

class gurantor_roles(models.Model):
    _name = "gurantor.roles"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class status_securing(models.Model):
    _name = "status.securing"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description::")



class company_executive(models.Model):
    _name = "company.executive"
    _rec_name = "description"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")



class society_executive(models.Model):
    _name = "society.executive"

    companyexecutive = fields.Many2one("company.executive", string=" Company Executive:")
    subsidiary = fields.Char(string="Subsidiary:")



class execution_status(models.Model):
    _name = "execution.status"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")



class property_execution(models.Model):
    _name = "property.execution"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")




class credit_categorization(models.Model):
    _name = "credit.categorization"

    order = fields.Integer(string="Order:")
    description = fields.Char(string="Description:")
    module = fields.Selection([('enforcement', 'Enforcement'), ('writeoff', 'WRITE OFF'), ('activecollection', 'ACTIVE COLLECTION')], string="Module:")


class method_payment(models.Model):
    _name = "method.payment"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")

class documents_modules(models.Model):
    _name = "documents.modules"

    order = fields.Integer(string="Order:")
    description = fields.Char(string="Description:")
    module = fields.Selection([('enforcement', 'Enforcement'), ('writeoff', 'WRITE OFF'), ('activecollection', 'ACTIVE COLLECTION')], string="Module:")

class credit_module(models.Model):
    _name = "credit.module"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")



class execution_payment(models.Model):
    _name = "execution.payment"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")



class guarantors_execution(models.Model):
    _name = "guarantors.execution"

    catalog = fields.Integer(string="Catalog:")
    description = fields.Char(string="Description:")


class event_execution(models.Model):
    _name = "event.execution"

    order = fields.Integer(string="Order:")
    description = fields.Char(string="Description:")
    module = fields.Selection([('enforcement', 'Enforcement'), ('writeoff', 'WRITE OFF'), ('activecollection', 'ACTIVE COLLECTION')], string="Module:")



class  execution_writeoff(models.Model):
    _name = "execution.writeoff"

    understatus = fields.Char(string=" Under Status:")
    status = fields.Selection([('enforcement1', 'Enforcement-1'), ('enforcement2', 'Enforcement-2'),('writeoffpursuit', 'WRITE OFF - In Pursuit'), ('writeoffenforcement', 'WRITE OFF - In Enforcement'),], string="Status:")



class process_status(models.Model):
    _name = "process.status"

    order = fields.Integer(string="Order:")
    description = fields.Char(string="Description:")
    module = fields.Selection([('enforcement', 'Enforcement'), ('writeoff', 'WRITE OFF'), ('activecollection', 'ACTIVE COLLECTION')], string="Module:")





class process_workflow(models.Model):
    _name = "process.workflow"

    status = fields.Selection([('active', 'Active'), ('off', 'Off')], string="Status:")
    designation = fields.Char(string="Designation:")
    module = fields.Selection([('enforcement', 'Enforcement'), ('writeoff', 'WRITE OFF'), ('activecollection', 'ACTIVE COLLECTION')], string="Module:")


