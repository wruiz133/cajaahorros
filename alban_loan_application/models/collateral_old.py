from odoo import models, fields, api
import datetime
import logging
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

    col_exists = fields.Boolean(string='Collateral Exists')
    col_type1 = fields.Selection([ ('non_move', 'Non-movable Property'),('move','Movable Property'), ('bank_acc', 'Bank Account'), ('insure', 'Insurance')],
                                string="Collateral Type (Optional)")
    #col_type = fields.Many2one('collateral.type',string="Collateral Type",required=True)
    col_type = fields.Many2one('collateral.type',string="Collateral Type")
    # property_type = fields.Many2one('property.type',string='Property Ty')

    property_type =  fields.Selection([('apartmnt', 'Apartment'), ('area_ground', 'Area Ground +'),('bodrum','Bodrum'),
                                       ('store', 'Store'), ('garage', 'Garage'),
                                       ('meadow', 'Meadow'), ('magazine', 'Magazine'),
                                       ('boats_in', 'Boats In'), ('building', 'Building'),
                                       ('forest', 'Forest'), ('priv_prop', 'Private Property'),
                                       ('arable_land', 'Arable Land'), ('ground', 'Ground'), ('ground_bldg', 'Ground+Buildings'),

                                       ],
                                      string="Property Type",)

    property_struc = fields.Many2one('property.structure',string='Poperty Structure')
    property_level = fields.Many2one('property.level',string='Poperty Level')

    nr_pasurise = fields.Char(string='Nr. Pasurise')
    prone = fields.Char(string='Nr. Prone')
    area = fields.Char(string='Area of Cadastral')
    dt_prone = fields.Date(string='Date Prone')
    phone = fields.Char(string='Phone')
    size = fields.Char(string='Size m2')
    age = fields.Integer(string='Age')


    bank =fields.Many2one('bank.details',string='Bank')
    col_status =fields.Many2one('coll.status',string='Collateral Status' , domain="[('col_type', '=', col_type1)]")
    # col_status =fields.Selection([('prop_leis','Property Of Leisure'),('prop_block','Property Blocked'),
    #                               ('unblock_prop','Unblocking Property'),('pledge_free','Pledge Free'),
    #                               ('pl_wait_block','Pledge Waiting to be Blocked '),('pledge_blocked','Pledge Blocked'),
    #                               ('pl_ubblock','Pledge Unblocked '),('blocked','Blocked'),('unblocked','Unblocked'),
    #
    #                               ],
    #                              string='Collateral Status')
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

    @api.onchange('col_type')
    def onchange_col_type(self):

        # _logger.info("coltype=========================================%s"%self.col_type.name)
        col_name = self.col_type.name
        if col_name:
            if col_name.strip(" ") == 'Non-movable Property':
                self.col_type1 = 'non_move'
                # _logger.info("coltype selection changed===================Non movable======================" )
            elif col_name.strip(" ") == 'Movable Property':
                self.col_type1 = 'move'
                # _logger.info("coltype selection changed============Movable=============================" )
            elif col_name.strip(" ") == 'Bank Account':
                self.col_type1 = 'bank_acc'
                # _logger.info("coltype selection changed=======Bank ==================================" )
            elif col_name.strip(" ") == 'Insurance':
                self.col_type1 = 'insure'
                # _logger.info("coltype selection changed=======Insurance ==================================" )


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


    res_part_id = fields.Many2one('res.partner',string='Partner',required=True)
    cust_id = fields.Char(related='res_part_id.account_id',string='Customer ID',required=True)
    role = fields.Many2one('linkage.roles',string='Role')
    name_c = fields.Char(string='Name')
    father_name_c = fields.Char(string="Father's Name")
    last_name_c = fields.Char(string="Last Name")
    country = fields.Many2one('res.country', string='Country ')
    city = fields.Many2one('admin.city', string='City')
    address= fields.Char(string="Address")
    telephone = fields.Char(string='Telephone')
    # id_type = fields.Many2one('id.type',string='Id Type')
    id_type = fields.Selection([('certificate', 'Certificate'), ('identity', 'Identification Card / Biometric Password'),
     ('identity_card', 'Identity Card'), ('passport', 'Passport'),
     ('license', 'Driving License')], string="Type:", )


    card_id = fields.Char(string='Card Id')
    nation_id = fields.Char(string='National Id')
    issue_date = fields.Date('Issue Date')
    country_issuer = fields.Many2one('res.country', string='Country Issuer', )
    city_issued = fields.Many2one('admin.city', string='City Issuer', )
    exp_date = fields.Date('Expiry Date', )

    link_det_id = fields.Many2one('collateral.details')

    @api.onchange('cust_id')
    def onchange_cust_id(self):
        write_vals = {}
        res_part_object = self.env['res.partner']
        if self.cust_id:
            res_part_id = res_part_object.search([('account_id', '=', self.cust_id.strip(" "))])
            if res_part_id:

                if res_part_id[0].account_id:
                    self.name_c = res_part_id[0].name

                if res_part_id[0].name:
                    self.name_c = res_part_id[0].name

                if res_part_id[0].fatherhood:
                    self.father_name_c = res_part_id[0].fatherhood

                if res_part_id[0].sur_name:
                    self.last_name_c = res_part_id[0].sur_name

                if res_part_id[0].country_id:
                    self.country = res_part_id[0].country_id.id

                if res_part_id[0].city_id:
                    self.city = res_part_id[0].city_id.id

                if res_part_id[0].telefoni_1:
                    self.telephone = res_part_id[0].telefoni_1

                if res_part_id[0].base_type:
                    self.id_type = res_part_id[0].base_type

                if res_part_id[0].logari:
                    self.card_id = res_part_id[0].logari

                if res_part_id[0].country_issuance:
                    self.country_issuer = res_part_id[0].country_issuance.id

                if res_part_id[0].date_release:
                    self.issue_date = res_part_id[0].date_release

                if res_part_id[0].date_expiry:
                    self.exp_date = res_part_id[0].date_expiry

                _logger.info('=====================create vals %s======================' % write_vals)

            else:
                _logger.info('=====================in the else part======================' )



class owner_details(models.Model):
    _name = "owner.details"

    res_part_id = fields.Many2one('res.partner', string='Partner')
    cust_id = fields.Char(related='res_part_id.account_id', string='Customer ID', required=True)
    # cust_id = fields.Char(string='Customer ID')
    role = fields.Many2one('linkage.roles',string='Role')
    name_c = fields.Char(string='Name')
    father_name_c = fields.Char(string="Father's Name")
    last_name_c = fields.Char(string="Last Name")
    country = fields.Many2one('res.country', string='Country ')
    city = fields.Many2one('admin.city', string='City')
    address= fields.Char(string="Address")
    telephone = fields.Char(string='Telephone')
    # id_type = fields.Many2one('id.type',string='Id Type')
    id_type = fields.Selection(
        [('certificate', 'Certificate'), ('identity', 'Identification Card / Biometric Password'),
         ('identity_card', 'Identity Card'), ('passport', 'Passport'),
         ('license', 'Driving License')], string="ID Type", )

    card_id = fields.Char(string='Card Id')
    nation_id = fields.Char(string='National Id')
    issue_date = fields.Date('Issue Date')
    country_issuer = fields.Many2one('res.country', string='Country Issuer', )
    city_issued = fields.Many2one('admin.city', string='City Issuer', )
    exp_date = fields.Date('Expiry Date', )

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
    type = fields.Char(string='Type')
    doc_file = fields.Binary(string='Document*',required=True)

    filename = fields.Char()

    static_test = fields.Char('Careful',default="""File types that can be charged:\
      .pdf,.jpeg,.jpg,.gif,.doc,.docx,.xls,.xlsx\
      .pdf files must have a maximum size of 3,000Kb\
      Other files must have a maximum size of 500Kb""")

    doc_det_id = fields.Many2one('collateral.details',string='Document Upload')

    @api.model
    def create(self, vals):

        current_date = datetime.datetime.now()
        print 'in the create def============================'
        if self._uid:
            vals.update({'uploaded_by': self._uid, 'upload_date': current_date, })

        res = super(document_details_col, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        current_date = datetime.datetime.now()
        if self._uid:
            # vals.update({'updated_by':self._uid,'id':res})
            vals.update({'uploaded_by': self._uid, 'upload_date': current_date, })
            print 'after vals getting updated============================'

        res = super(document_details_col, self).write(vals)
        return res

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
            # _logger.info('=====================loan_app_cust_ids %s======================' % loan_app_cust_ids)

        for col_det_id in col_det_ids:
            # _logger.info('=====================col_det_ids %s======================' % col_det_ids)
            flag = False
            if col_det_id.link_det_ids:
                # flag = False
                for link_det_id in col_det_id.link_det_ids:
                    # _logger.info('=====================link_det_id %s======================' % link_det_id)
                    appl_id_lst.append(link_det_id.cust_id)
                for list_id in appl_id_lst:
                    for appl_id in loan_app_cust_ids:
                        if list_id == appl_id:
                            flag = True
                            col_det_id.col_exists = True

                        else:
                            col_det_id.col_exists = False
                            # _logger.info('=====================in the else part===%s======================' % col_det_id)

        return True

    col_line_ids = fields.One2many('collateral.details.line','col_line_id',string='Collateral Line')
    # sel_collateral = fields.Many2one('collateral.details', string='Select Collateral',domain=lambda self:self.get_collateral_type())
    # sel_collateral = fields.Many2one('collateral.details', string='Select Collateral',domain=lambda self: [('id', '=', self.get_collateral_type())])
    sel_collateral = fields.Many2one('collateral.details', string='Select Collateral',domain="[('col_exists','=',True)]")



    @api.multi
    def get_collateral_data(self):
        col_det_ids = self.env['collateral.details'].search([('id','=',self.sel_collateral.id)])
        appl_id_lst = []
        loan_app_cust_ids = []
        if self.applicant_ids:
            for app_id in self.applicant_ids:
                loan_app_cust_ids.append(app_id.customer_no1)
            # _logger.info('=====================loan_app_cust_ids %s======================' % loan_app_cust_ids)

        # for col_det_id in col_det_ids:

        _logger.info('=====================col_det_ids %s======================' % col_det_ids)
        flag = False
        if col_det_ids.link_det_ids:
            # flag = False
            for link_det_id in col_det_ids.link_det_ids:
                # _logger.info('=====================link_det_id %s======================' % link_det_id)
                appl_id_lst.append(link_det_id.cust_id)
            for list_id in appl_id_lst:
                for appl_id in loan_app_cust_ids:
                    if list_id == appl_id:
                        flag = True

        if flag:
            # self.col_line_ids.sel = col_det_ids
            # _logger.info('=====================after setting the flag======================')
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
    property_type = fields.Selection([('apartmnt', 'Apartment'), ('area_ground', 'Area Ground +'), ('bodrum', 'Bodrum'),
                                      ('store', 'Store'), ('garage', 'Garage'),
                                      ('meadow', 'Meadow'), ('magazine', 'Magazine'),
                                      ('boats_in', 'Boats In'), ('building', 'Building'),
                                      ('forest', 'Forest'), ('priv_prop', 'Private Property'),
                                      ('arable_land', 'Arable Land'), ('ground', 'Ground'),
                                      ('ground_bldg', 'Ground+Buildings'),
                                      ],
                                     string="Property Type", )
    nr_pasurise = fields.Char(string='Nr. Pasurise')
    prone = fields.Char(string='Nr. Prone')

    col_status = fields.Many2one('collateral.status',related='sel_collateral.col_status',string='Collateral Status')
    area = fields.Char(related='sel_collateral.area',string='Area of Cadastral')
    dt_prone = fields.Char(related='sel_collateral.dt_prone',string='Date Prone')
    phone = fields.Char(related='sel_collateral.phone',string='Phone')

    #========================for other owners=========================
    # owner_det_line_ids = fields.One2many('owner.details.line', 'owner_det_id',related='sel_collateral.owner_det_ids', string='Owners')
    # link_det_line_ids = fields.One2many('linkage.details.line', 'link_det_id',related='sel_collateral.link_det_ids', string='Linkage')
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
    # cust_id = fields.Char(string='Customer ID')
    # role = fields.Many2one('linkage.roles',string='Role')
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
    # role = fields.Many2one('linkage.roles', string='Role')
    name_c = fields.Char(string='Name')
    father_name_c = fields.Char(string="Father's Name")
    last_name_c = fields.Char(string="Last Name")
    country = fields.Many2one('res.country', string='Country ')
    city = fields.Many2one('admin.city', string='City')
    street = fields.Char(string="Street")
    wire = fields.Char(string='Wire')
    # id_type = fields.Many2one('id.type',string='Id Type')


    link_det_id = fields.Many2one('collateral.details.line')



