from odoo import models, fields, api,_
import datetime
import logging
_logger = logging.getLogger(__name__)

class prelim_app(models.Model):
    _inherit = "prelim.app"

    @api.multi
    def action_approve(self):
        loan_app_obj = self.env['loan.application']
        appl_det_obj = self.env['applicant.details']
        #appl_det_comp_obj = self.env['applicant.details.company']
        current_date = datetime.datetime.now().date()
        res = super(prelim_app, self).action_approve()
        
        select_sql_clause = """SELECT count(id)  as count_loan from loan_application where  customer_acc_id ='""" + str(self.account_id1) + """'""" 
                    
        self.env.cr.execute(select_sql_clause)
        query_results = self.env.cr.dictfetchall()
        print query_results, "----------------------------",query_results[0].get('no_accoun'),len(query_results)
        
        if query_results[0].get('count_loan') != None:
            count_loan=str(query_results[0].get('count_loan')+1)
            while len(count_loan)<3:
                    count_loan='0' + count_loan 
        
        else:
            count_loan='000'



        loan_vals = {
            'priority':'medium',
            'date':current_date,
            'branch': self.branch_id.id,
            'sub_branch':self.sub_branch_id.id,

            'currency':self.currency.id,
            'requested_amt':self.loan_credit,
            'family_amt':self.friend_relative,

            'officer_id':self.officer.id,
            'appl_type':'individual',
            # 'office':self.officer.name,
            'partner_id':self.partner_id.id,
            'customer_acc_id':self.account_id1,
            'name':self.name,
            'fathername':self.fathername,
            'lastname':self.lastname,
            'national_id':self.national_id,
            'is_company_customer':self.is_company_customer,
            'appln_no':count_loan

        }
        
        current_date = datetime.datetime.now().date()

        if self._uid:
            loan_vals.update({'approved_by':self._uid,'approval_date':current_date})

        # loan_vals.update({'status': 'approve'})
        # _logger.info('=====================before create statement=====================' )
        loan_app_id  = loan_app_obj.create(loan_vals)
        # print 'loan_app_id=========================================',loan_app_id
        _logger.info('=====================loan_app_id %s======================' % loan_app_id)
        print"----------self-----------",self.partner_id
        if loan_app_id:
            if self.is_company_customer==-10:
                app_det_vals = {
                    'partner_id':self.partner_id.id or '',
                    'is_company_customer_det':-10,
                    'type':'primary',
                    'existing':'True',
                    'customer_no1':self.account_id1 or '',
                    'f_name': self.name or '',
                    'm_name':self.fathername or '',
                    'l_name':self.lastname or '',
                    'national_id': self.national_id or '',
                    'applicant_id':loan_app_id.id,
                    'mother_name': self.maiden_name or '',
                    'last_name_bef':self.last_name_bef or '',
                    'gender':self.gender or '' , 
                    'exp': self.exp or '' ,
                    'dependents': self.chdrn or '',
                    'no_of_people':self.tmember or '',
                    'social_sit':self.ssituation or '',
                    'education':self.educat or '',
                    'national_id':self.national_id or '',
                    'in_cont':'yes',
                    'marital_status':self.mstatus or '',
                    
                    'country':self.country_issuance.id or '',
                    'customer_type_name':  self.customer_type_name or '',
                    'industry_sector':self.industry_sector or '',
                    'industry_group':self.industry_group or '',
                    'industry_code' :self.industry_code or '',
                    'type_of_id1':self.national_id_type or '',
                    'passport_no':self.document_client_id or '',
                    'pas_issue_date':self.date_release or '',
                    'country_issuer':self.country_issuance.id or '', 
                    #'city_issued':self.city_id.id or '',
                    'nationality':self.citizenship or '',
                    'pas_exp_date':self.date_expiry or '',
                    'birthdate':self.birthday,
                    'country_birth':self.birth_country.id or '',
                    'city_birth':self.city_id.id or '',
                    'landline_no':self.phone or '',
                    'fax':self.fax or '',
                    'mobile_no':self.mobile or '',
                }
                app_det_ids = appl_det_obj.create(app_det_vals)
                _logger.info('=====================app_det_ids for individual %s=================' % app_det_ids)

            elif self.is_company_customer==-20:
                app_det_vals = {
                    'partner_id':self.partner_id.id or '',
                    'is_company_customer_det':-20,
                    'type': 'primary',
                    'existing': True,
                    'customer_no1': self.account_id1,
                    'f_name': self.name or '',
                    'l_name': self.detail_name_com or '',
                    'national_id': self.national_id or '',
                    'in_cont':'yes',
                    #'applicant_id_com': loan_app_id.id,
                    'applicant_id': loan_app_id.id,

                    'm_name':'',
                    'gender':'',
                    'mother_name':'',
                    'last_name_bef':'',
                    'marital_status':'',

                    'national_id':self.national_id or '',
                    'country':self.country_issuance.id or '',
                    'customer_type_name':  self.customer_type_name or '',
                    'industry_sector':self.industry_sector or '',
                    'industry_group':self.industry_group or '',
                    'industry_code':self.industry_code or '',
                    'type_of_id1':self.national_id_type or '',
                    'passport_no':self.document_client_id or '',
                    'pas_issue_date':self.date_release or '',
                    'country_issuer':self.country_issuance.id or '', 
                    #'city_issued':self.city_id.id or '',
                    'nationality':self.citizenship or '',
                    'pas_exp_date':self.date_expiry or '',
                    'birthdate':self.birthday,
                    'country_birth':self.birth_country.id or '',
                    'city_birth':self.city_id.id or '',
                    'landline_no':self.phone or '',
                    'fax':self.fax or '',
                    'mobile_no':self.mobile or '',
                }
                app_det_ids = appl_det_obj.create(app_det_vals)
                _logger.info('=====================app_det_ids for company%s======================' % app_det_ids)


        return res




