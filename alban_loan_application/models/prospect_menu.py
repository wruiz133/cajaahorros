from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import datetime
import dateutil.parser


class prospect_menu(models.Model):
    _name = "prospect.menu"

    branch_id = fields.Many2one('admin.branch', string='Branch', required=True)
    officer = fields.Many2one('admin.officer', 'Officer', required=True)

    customer = fields.Many2one('res.partner',string='Customer',)
    name = fields.Char(string='First Name',required=True)
    fathername = fields.Char('Father Name', required=True,)
    lastname = fields.Char('Last Name', required=True,)
    date_contact = fields.Date('Date Contacting', required=True)
    
    relation_bus = fields.Selection([('admin', 'Administrator'), ('husband_wife', 'Husband/Wife'),
                                 ('family', 'Family'), ('children', 'Children'),
                                 ('owner', 'Owner'), ('employee', 'Employee'),
                                 ],
                                string='Relation to Business', required=True)
    type_business = fields.Selection([('ambulant', 'Ambulant'), ('without_job', 'Without job'),
                                   ('private_with_license', 'Private with license'),
                                   ('private_without_license', 'Private without license'),
                                   ('employed', 'Employed'),
                                   ('transport', 'Transport'), ('trade', 'Trade'),], string='Type of Business', required=True)

    client_status = fields.Selection([('preexist_client',    'Pre existing Client'), 
                                      ('active_client',         'Active Client'),
                                      ('potential_client',   'Potential Client'),
                                   ], string='Client Status', required=True)

    reason_visit = fields.Selection([('promotion_visit',          'Promotional Visit for new Customer'),
                                     ('routine_visit',          'Routine Visit'),
                                     ('duelate_visit',       'Due Late Visit'),
                                     ('duelate_court_visit', 'Due late (Client in court)'),
                                     ('duelate_exec',        'Due late (Client in baillif)'),
                                     ('other_visit',          'Others'),
                                   ], string='Reason of Visit',required=True )

    overall_visit = fields.Selection([('no_demand', 'Currently ,there is no demand for loans'), 
                                     ('apply',     'Will Apply for the subsequent period'),
                                     ('request',   "There's request for Loan amount All/EUR"),

                                   ], string='Conclusions on Visit',required=True )
    loan_amount = fields.Float(string='Loan Amount')
    #currency = fields.Many2one('res.currency')
    currency = fields.Many2one('res.currency')
    notes = fields.Text(string='Notes',required=True)

    country = fields.Many2one('res.country', string='Country:')
    district_id = fields.Many2one('admin.district', string='District:', )
    municipality = fields.Many2one('admin.municipal', string='Commune:', )
    city_village = fields.Many2one('admin.village', string='City/Village:', )
    street = fields.Char('Street:', )

    email = fields.Char(string='Email')
    mobile = fields.Char(string='Mobile No.')
    phone = fields.Char(string='Telephone No.')

    created_by = fields.Many2one('res.users', string='It was recorded by',readonly = True)
    create_date = fields.Date('It was recorded on',readonly = True)
    updated_by = fields.Many2one('res.users', string='Last updated by',readonly = True)
    update_date = fields.Date('Update Date',readonly = True)

    @api.model
    def create(self, vals):

        current_date = datetime.datetime.now().date()
        print 'in the create def============================'
        if self._uid:
            vals.update({'created_by': self._uid, 'create_date': current_date,})

        _logger.info('=====================vals %s======================' % vals)
        res = super(prospect_menu, self).create(vals)

        return res

    @api.multi
    def write(self, vals):
        current_date = datetime.datetime.now().date()
        if self._uid:
            # vals.update({'updated_by':self._uid,'id':res})
            vals.update({'updated_by': self._uid, 'update_date': current_date, })

        res = super(prospect_menu, self).write(vals)
        return res

    @api.onchange('date_contact')
    def onchange_date_contact(self):

        if self.date_contact:
            due_date_interest = dateutil.parser.parse(self.date_contact).date()
            current_date = datetime.datetime.now().date()
            current_day = current_date.strftime("%d")
            current_month = current_date.strftime("%m")
            day_of_cont = due_date_interest.strftime("%d")
            cont_month  = due_date_interest.strftime("%m")
            daydiff = float(current_day) - float(day_of_cont)
            monthdiff = float(current_month) - float(cont_month)
            if monthdiff == 0:
                if daydiff == 0 :
                    pass
                elif  daydiff < 3 :
                    pass
                elif daydiff >=3:
                    self.date_contact = current_date
                    _logger.info('===================After the current date is changed in if=======================' )
            elif monthdiff == 1:
                if daydiff < 3 :
                    pass
                else:
                    self.date_contact = current_date
                    _logger.info('===================After the current date is changed in elif=======================')
            else:

                self.date_contact = current_date
                _logger.info('===================After the current date is changed in else=======================')

    @api.onchange('customer')
    def onchange_customer(self):
        _logger.info('=====================customer %s======================' % self.customer)
        write_vals = {}
        cust_id = self.customer
        res_part_object = self.env['res.partner']

        partner_id = res_part_object.search([('id', '=', cust_id.id)])
        if partner_id:
            self.name = partner_id[0].name
            self.fathername = partner_id[0].fathername
            if partner_id[0].is_company == True :
                self.lastname = partner_id[0].display_name
            else:
                self.lastname = partner_id[0].lastname
            self.country = partner_id[0].country_id.id or False
            self.district_id = partner_id[0].district_id.id or False
            self.municipality = partner_id[0].municipality.id or False
            self.city_village = partner_id[0].city_village.id or False
            self.email= partner_id[0].city_village.id or False
            self.phone = partner_id[0].phone or '123456'
            self.mobile = partner_id[0].mobile or '123456'

            # write_vals={'name':partner_id[0].name,
            #             'fatherhood':partner_id[0].fatherhood,
            #             'surname':partner_id[0].sur_name,
            #             'country':partner_id[0].country_id.id or False,
            #             'district_id':partner_id[0].district_id.id or False,
            #             'municipality':partner_id[0].municipality.id or False,
            #             'city_village':partner_id[0].city_village.id or False,
            #             'telpne_no':partner_id[0].telefoni_1 or '123456',
            #
            #             }
            # self.write(write_vals)

            _logger.info('=====================customer info is filled======================')
            self._cr.commit()



