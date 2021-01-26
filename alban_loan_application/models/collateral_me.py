from odoo import models, fields, api,_
import datetime
from odoo.exceptions import UserError,ValidationError
import logging
import filestore_generic
_logger = logging.getLogger(__name__)


class property_structure(models.Model):
    _name = "property.structure"

    name = fields.Char(string='Name',required=True)
    desc =fields.Text(string='Description')

class collateral_type(models.Model):
    _name = "collateral.type"
    name =fields.Char(string='Name',required=True)
    desc = fields.Text(string='Description')

class collateral_status(models.Model):
    _name = "collateral.status"
    name =fields.Char(string='Name',required=True)
    desc = fields.Text(string='Description')
    col_type = fields.Many2one('collateral.type',string='Collateral Type',required=True)


class property_level(models.Model):
    _name = "property.level"

    name = fields.Char(string='Name',required=True)
    desc =fields.Text(string='Description')

class collateral_details(models.Model):
    _name = "collateral.details"

#     =================================for non-movable========================
    name = fields.Char(string='Naming',required=True)
    collateral_type =fields.Many2one('coll.status',string="Collateral Type",required=True)
    collatoral_status=fields.Many2one('collatoral.status',string="Collateral Status")

    col_exists = fields.Boolean(string='Collateral Exists')
    col_type1 = fields.Selection([ ('non_move', 'Non-movable Property'),('move','Movable Property'), ('bank_acc', 'Bank Account'), ('insure', 'Insurance')],
                                string="Collateral Type (Optional)")
    collateral_name = fields.Char(related='collateral_type.name',string='Collateral Name')
    col_type = fields.Many2one('collateral.type',string="Collateral Type")
    property_type = fields.Many2one('property.type',string='Property Type')


    property_struc = fields.Many2one('property.structure',string='Poperty Structure')
    property_level = fields.Many2one('property.level',string='Poperty Level')

    nr_pasurise = fields.Char(string='No. Property')
    prone = fields.Char(string='Nr. Prone')
    area = fields.Char(string='Area of Cadastral')
    dt_prone = fields.Char(string='Date Prone')
    phone = fields.Char(string='Phone')
    size = fields.Char(string='Size m2')
    age = fields.Integer(string='Age')


    bank =fields.Many2one('bank.details',string='Bank')
    col_status =fields.Many2one('collateral.status',string='Collateral Status')

    acc_no =fields.Char(string='Account No.')
    pledge_type = fields.Selection([('aprtmnt', 'Apartment'), ('dep_bank', 'Deposit Banking'),('store','Store'), ('living', 'Living Thing'),
                                    ('equip', 'Equipment'),('houses', 'Houses'),('land', 'Land'),
                                    ('book_invent', 'Book Inventory'),('vehicle', 'Vehicle'),],string="Pledge Type")
    serial_no = fields.Char(string='Serial No.')
    manuf = fields.Char(string='Manufacturer')
    model = fields.Char(string='Model')
    body = fields.Char(string='Body')
    year_prod = fields.Char(string='Year of Production')
    mileage = fields.Char(string='Mileage(KM)')

    insure_comp = fields.Char(string='Insurance Company')
    nr_police = fields.Char(string='Nr. polices of sig.')
    country = fields.Many2one('res.country', string='Country:')
    district_id = fields.Many2one('admin.district', string='District:', )
    municipality = fields.Many2one('admin.municipal', string='Commune:', )
    city_village = fields.Many2one('admin.village', string='City/Village:', )
    street = fields.Char('Street:', )
    data_placement = fields.Date('Placement Date:')
    notes = fields.Text(string="Collateral Notes")

    recorded_by = fields.Many2one('res.users',string='It was recorded By')
    changed_by = fields.Many2one('res.users',string='Changed By')

    reval_ids = fields.One2many('revaluation.details','reval_id','Revaluation')



class bank_details(models.Model):
    _name ='bank.details'

    name = fields.Char('Bank Name')

class revaluation_details(models.Model):
    _name ='revaluation.details'

    val_src = fields.Char(string='Valuation Source')
    id_no = fields.Char(string="Identification No.")
    val_type = fields.Char(string="Valuation Type")
    reval_id =fields.Many2one('collateral.details')

    whole_value = fields.Float(string="Wholesale Value")
    ret_value = fields.Float(string="Retail Value")
    use_value = fields.Float(string="Usage Value")
    attr_value = fields.Float(string="Attribute Value")
    total_value = fields.Float(string="Total Value")
    val_date = fields.Date('Valuaion Date')


# \======================for linkage tab===================


class collateral_details(models.Model):
    _inherit = "collateral.details"

    link_det_ids = fields.One2many('linkage.details', 'link_det_id',string='Linkage')
    owner_det_ids = fields.One2many('owner.details', 'owner_det_id',string='Owners')

class linkage_details(models.Model):
    _name = "linkage.details"

    res_part_id = fields.Many2one('res.partner', string='Partner', required=True)


    cust_id = fields.Char(related='res_part_id.account_id', string='Customer ID', required=True)
    role = fields.Many2one('linkage.roles', string='Role')
    name_c = fields.Char(related='res_part_id.name', string='Name')
    father_name_c = fields.Char(related='res_part_id.fathername', string="Father's Name")
    last_name_c = fields.Char(related='res_part_id.lastname', string="Last Name")
    country = fields.Many2one('res.country', string='Country ')
    city = fields.Many2one('admin.city', string='City')
    address = fields.Char(string="Address")
    telephone = fields.Char(string='Telephone')
    id_type = fields.Selection(related='res_part_id.national_id_type', string="Type", )

    card_id = fields.Char(string='Document Id', related='res_part_id.document_client_id')
    nation_id = fields.Char(string='National Id', related='res_part_id.national_id')
    issue_date = fields.Date('Issue Date', related='res_part_id.date_release')
    country_issuer = fields.Many2one('res.country', string='Country Issuer', related='res_part_id.country_issuance', )
    city_issued = fields.Many2one('admin.city', string='City Issuer', )
    exp_date = fields.Date('Expiry Date', related='res_part_id.date_expiry')

    link_det_id = fields.Many2one('collateral.details')


class owner_details(models.Model):
    _name = "owner.details"


    res_part_id = fields.Many2one('res.partner', string='Partner')
    cust_id = fields.Char(related='res_part_id.account_id', string='Customer ID', required=True)
    role = fields.Many2one('linkage.roles',string='Role')
    name_c = fields.Char(related='res_part_id.name',string='Name')
    father_name_c = fields.Char(related='res_part_id.fathername',string="Father's Name")
    last_name_c = fields.Char(related='res_part_id.lastname',string="Last Name")
    country = fields.Many2one('res.country', string='Country ')
    city = fields.Many2one('admin.city', string='City')
    address= fields.Char(string="Address")
    telephone = fields.Char(string='Telephone')
    id_type = fields.Selection(related='res_part_id.national_id_type', string="Type", )


    card_id = fields.Char(string='Document Id', related='res_part_id.document_client_id')
    nation_id = fields.Char(string='National Id', related='res_part_id.national_id')
    issue_date = fields.Date('Issue Date', related='res_part_id.date_release')
    country_issuer = fields.Many2one('res.country', string='Country Issuer', related='res_part_id.country_issuance', )
    city_issued = fields.Many2one('admin.city', string='City Issuer', )
    exp_date = fields.Date('Expiry Date', related='res_part_id.date_expiry')


    owner_det_id = fields.Many2one('collateral.details')


class linkage_roles(models.Model):
    _name = "linkage.roles"

    name =fields.Char('Role Name',required=True)
    role_desc = fields.Text('Description')

class id_type(models.Model):
    _name = "id.type"

    name =fields.Char('Id Type',required=True)
    id_desc = fields.Text('Description')

#|=========================================================


class collateral_details(models.Model):
    _inherit = "collateral.details"

    comment_ids = fields.One2many('comments.details.col','comment_id')
    doc_det_ids = fields.One2many('document.details.col','doc_det_id')

# ===========================Comments Tab===============================
class comments_details_col(models.Model):
    _name = "comments.details.col"

    update_date = fields.Date('Date', )
    status = fields.Char(string='Status')
    event = fields.Char(string='Event')
    notes = fields.Text(string='Notes')
    user = fields.Many2one('res.users', string='User')
    module = fields.Char(string='Module')

    comment_id = fields.Many2one('collateral.details',string='Comments Details')
# ===================================================================================


# |=====================documents tab+++++===========================

class document_details_col(models.Model):
    _name = "document.details.col"

    doc_title = fields.Char(string='Document Title',required=True)
    desc = fields.Text(string='Description')
    upload_date = fields.Datetime(' Date + Time' ,readonly=True)
    uploaded_by = fields.Many2one('res.users', string='User ',readonly=True)
    type = fields.Char(string='Type',compute='get_extension')
    # size = fields.Integer(string='Size')
    doc_file = fields.Binary(string='Document*',required=True)

    filename = fields.Char()

    static_test = fields.Char('Careful',default="""File types that can be charged:\
      .pdf,.jpeg,.jpg,.gif,.doc,.docx,.xls,.xlsx\
      .pdf files must have a maximum size of 3,000Kb\
      Other files must have a maximum size of 500Kb""")

    doc_det_id = fields.Many2one('collateral.details',string='Document Upload')

    #to get the type of the file and write it into type field
    @api.one
    @api.depends('filename')
    def get_extension(self):
        filename = self.filename
        flag = False
        if filename:
            flag = filestore_generic.FilestoreGeneric(filename).check_extension(filename)
            if not flag:
                extension = filename[filename.rfind('.'):]
                self.type = extension + " document"

    @api.model
    def create(self, vals):
        current_date = datetime.datetime.now()
        if self._uid:
            vals.update({'uploaded_by': self._uid, 'upload_date': current_date,})
        res = super(document_details_col, self).create(vals)
        # flag = self.check_extension()
        flag = filestore_generic.FilestoreGeneric(res.filename).check_extension(res.filename)
        if flag:
            raise UserError(_('You cannot upload files other than those specified.'))

        return res

    @api.multi
    def write(self, vals):

        current_date = datetime.datetime.now()
        if self._uid:
            vals.update({'uploaded_by': self._uid, 'upload_date': current_date,})
        res = super(document_details_col, self).write(vals)
        # flag = self.check_extension()
        flag = filestore_generic.FilestoreGeneric(self.filename).check_extension(self.filename)
        if flag:
            raise UserError(_('You cannot upload files other than those specified.'))

        return res

    # @api.multi
    # def check_extension(self):
    #     allow_ext_lst =  ['.pdf','.jpeg','.jpg','.gif','.doc','.docx','.xls','.xlsx']
    #     file_name1 = self.filename
    #     flag = False
    #     if file_name1:
    #
    #         extension = file_name1[file_name1.rfind('.'):]
    #         # self.type = extension +" document"
    #         if extension not in allow_ext_lst:
    #             flag = True
    #
    #     return flag


class loan_application(models.Model):
    _inherit = "loan.application"

    @api.multi
    def get_collateral_type(self):
        col_det_ids = self.env['collateral.details'].search([])

        appl_id_lst = []
        loan_app_cust_ids = []
        col_det_lst = []
        if self.applicant_ids:
            for app_id in self.applicant_ids:
                loan_app_cust_ids.append(app_id.customer_no1)

        for col_det_id in col_det_ids:
            flag = False
            if col_det_id.link_det_ids:
                # flag = False
                for link_det_id in col_det_id.link_det_ids:
                    appl_id_lst.append(link_det_id.cust_id)
                for list_id in appl_id_lst:
                    for appl_id in loan_app_cust_ids:
                        if list_id == appl_id:
                            flag = True
                            col_det_id.col_exists = True

                        else:
                            col_det_id.col_exists = False

        return True

    col_line_ids = fields.One2many('collateral.details.line','col_line_id',string='Collateral Line')
    sel_collateral = fields.Many2one('collateral.details', string='Select Collateral')

    @api.multi
    def get_collateral_data(self):
        col_det_ids = self.env['collateral.details'].search([('id','=',self.sel_collateral.id)])
        appl_id_lst = []
        loan_app_cust_ids = []
        if self.applicant_ids:
            for app_id in self.applicant_ids:
                loan_app_cust_ids.append(app_id.customer_no1)

        flag = False
        if col_det_ids.link_det_ids:
            # flag = False
            for link_det_id in col_det_ids.link_det_ids:
                appl_id_lst.append(link_det_id.cust_id)
            for list_id in appl_id_lst:
                for appl_id in loan_app_cust_ids:
                    if list_id == appl_id:
                        flag = True

        if flag:
            col_line_obj = self.env['collateral.details.line']
            col_line_vals={
                'sel_collateral':self.sel_collateral.id,
                # 'already_scanned':True,
                'col_line_id':self.id,
            }
            col_line_id = col_line_obj.create(col_line_vals)
            for link_det_id in col_det_ids.link_det_ids:
                link_det_line_obj = self.env['linkage.details.line']
                link_write_vals={
                    'res_part_id':link_det_id.res_part_id.id,
                    'cust_id':link_det_id.cust_id,
                    'name_c':link_det_id.name_c or '',
                    'father_name_c':link_det_id.father_name_c or '',
                    'last_name_c':link_det_id.last_name_c or '',
                    'country':link_det_id.country.id or '',
                    'city':link_det_id.city.id or '',
                    'street':link_det_id.address or '',
                    'wire':link_det_id.telephone or '',
                    'link_det_id':col_line_id.id,
                }

                link_det_line_obj.create(link_write_vals)

            if col_det_ids.owner_det_ids:
                for owner_det_id in col_det_ids.owner_det_ids:
                    owner_det_line_obj = self.env['owner.details.line']
                    owner_write_vals = {
                        'res_part_id': owner_det_id.res_part_id.id,
                        'cust_id': owner_det_id.cust_id,
                        'name_c': owner_det_id.name_c or '',
                        'father_name_c': owner_det_id.father_name_c or '',
                        'last_name_c': owner_det_id.last_name_c or '',
                        'country': owner_det_id.country.id or '',
                        'city': owner_det_id.city.id or '',
                        'street': owner_det_id.address or '',
                        'wire': owner_det_id.telephone or '',
                        'owner_det_id': col_line_id.id,
                    }
                    owner_det_line_obj.create(owner_write_vals)

        return True


class collateral_details_line(models.Model):
    _name = "collateral.details.line"

    sel_collateral = fields.Many2one('collateral.details',string='Select Collateral')

    col_type = fields.Many2one('collateral.type',related='sel_collateral.col_type',string='Collateral Type')
    collateral_type = fields.Many2one('coll.status',related='sel_collateral.collateral_type', string="Collateral Type")

    property_type = fields.Many2one('property.type',related='sel_collateral.property_type', string="Property Type", )#changed line
    nr_pasurise = fields.Char(string='No. Property')
    prone = fields.Char(string='Nr. Prone')

    col_status = fields.Many2one('collateral.status',related='sel_collateral.col_status',string='Collateral Status')
    # col_status = fields.Many2one('collateral.status',related='sel_collateral.collateral_type',string='Collateral Status')#changed line
    collatoral_status = fields.Many2one('collatoral.status',related='sel_collateral.collatoral_status',string='Collateral Status')#changed line
    area = fields.Char(related='sel_collateral.area',string='Area of Cadastral')
    dt_prone = fields.Char(related='sel_collateral.dt_prone',string='Date Prone')
    phone = fields.Char(related='sel_collateral.phone',string='Phone')

    #========================for other owners=========================

    owner_det_line_ids = fields.One2many('owner.details.line', 'owner_det_id', string='Owners')
    link_det_line_ids = fields.One2many('linkage.details.line', 'link_det_id', string='Linkage')

    country = fields.Many2one('res.country',related='sel_collateral.country', string='Country')
    district_id = fields.Many2one('admin.district',related='sel_collateral.district_id', string='District', )
    municipality = fields.Many2one('admin.municipal', related='sel_collateral.municipality',string='Commune', )
    city_village = fields.Many2one('admin.village',related='sel_collateral.city_village', string='City/Village', )
    street = fields.Char(related='sel_collateral.street',string='Street:', )


    property_value1 = fields.Float(string='Property Value')
    data_placement = fields.Date(related='sel_collateral.data_placement',string='Placement Date')
    nr_inskriptimi = fields.Float(string='Nr. Inskriptimi')

    exp_date = fields.Date('Expiry Date', )
    unblock_date = fields.Date('Unblocking Date', )
    col_notes = fields.Text(related='sel_collateral.notes',string='Collateral Notes')
    loan_notes = fields.Text(string='Loan Application Notes')

    col_line_id = fields.Many2one('loan.application',string='Collateral Details')


class owner_details_line(models.Model):
    _name = "owner.details.line"

    res_part_id = fields.Many2one('res.partner', string='Partner')
    cust_id = fields.Char(related='res_part_id.account_id', string='Customer ID', required=True)
    name_c = fields.Char(string='Name')
    father_name_c = fields.Char(string="Father's Name")
    last_name_c = fields.Char(string="Last Name")
    country = fields.Many2one('res.country', string='Country ')
    city = fields.Many2one('admin.city', string='City')
    street= fields.Char(string="Street")
    wire= fields.Char(string="Wire")

    owner_det_id = fields.Many2one('collateral.details.line')

class linkage_details_line(models.Model):
    _name = "linkage.details.line"

    res_part_id = fields.Many2one('res.partner', string='Partner', required=True)
    cust_id = fields.Char(related='res_part_id.account_id', string='Customer ID', required=True)
    name_c = fields.Char(string='Name')
    father_name_c = fields.Char(string="Father's Name")
    last_name_c = fields.Char(string="Last Name")
    country = fields.Many2one('res.country', string='Country ')
    city = fields.Many2one('admin.city', string='City')
    street = fields.Char(string="Street")
    wire = fields.Char(string='Wire')


    link_det_id = fields.Many2one('collateral.details.line')



