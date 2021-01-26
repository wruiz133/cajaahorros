from odoo import models, fields, api,_
import datetime
import base64
from odoo.exceptions import UserError,ValidationError
import os,sys

import logging
#import lien_details
import filestore_generic
logger = logging.getLogger(__name__)


class collateral_details(models.Model):
    _inherit = "collateral.details"

    @api.multi
    def create_files(self, res_id):
        # lien_obj = self.env['lien.details']
        loan_config_ids = self.env['loan.config.directory'].search([])[0]
        store_path = loan_config_ids.parent_directory + '/' + loan_config_ids.collateral_directory + '/' + \
                     loan_config_ids.collateral_sub_directory + '/' + res_id.name + "/"
        if res_id.doc_det_ids:
            for doc_id in res_id.doc_det_ids:
                file_data = doc_id.doc_file
                if doc_id.filename:
                    file_name1 = doc_id.filename

                    extension = file_name1[file_name1.rfind('.'):]

                    extension2 = os.path.splitext(file_name1)[0][0:].strip()

                    filepath = os.path.join(store_path, extension2 + extension)
                    file = base64.b64decode(file_data)
                    flag = filestore_generic.FilestoreGeneric(file, extension).check_size(file,extension)

                    if not flag:

                        with open(filepath, "wb") as f:
                            f.write(file)
                            os.chmod(filepath, 0777)
                            f.close()

        return True

    @api.multi
    def create_directory_duplicate(self):
        loan_config_ids = self.env['loan.config.directory'].search([])[0]

        path = loan_config_ids.parent_directory+'/'

        path1 = path+ loan_config_ids.collateral_directory+'/'

        path2 = path1 + loan_config_ids.collateral_sub_directory+'/'

        path3 = path2 + self.name+"/"

        directory1 = os.path.dirname(path1)
        directory2 = os.path.dirname(path2)
        directory3 = os.path.dirname(path3)

        if not os.path.exists(directory1):

            os.mkdir(directory1)
            os.chmod(directory1, 0777)
        if not os.path.exists(directory2):
            os.mkdir(directory2)
            os.chmod(directory2, 0777)
        if not os.path.exists(directory3):
            os.mkdir(directory3)
            os.chmod(directory3, 0777)

        return True


    @api.multi
    def create_directory(self,directory_name):
        loan_config_ids = self.env['loan.config.directory'].search([])[0]

        path1 = loan_config_ids.parent_directory+'/'

        path2 = path1 + loan_config_ids.collateral_directory+'/'

        path3 = path2 + loan_config_ids.collateral_sub_directory+"/"

        path4 = path3 + directory_name+ "/"

        directory1 = os.path.dirname(path1)
        directory2 = os.path.dirname(path2)
        directory3 = os.path.dirname(path3)
        directory4 = os.path.dirname(path4)

        if os.path.exists(directory1):
            if not os.path.exists(directory2):
                os.mkdir(directory2)
                os.chmod(directory2, 0777)
            if not os.path.exists(directory3):
                os.mkdir(directory3)
                os.chmod(directory3, 0777)

            if not os.path.exists(directory4):
                os.mkdir(directory4)
                os.chmod(directory4, 0777)
        return True

    @api.model
    def create(self,vals):
        res = super(collateral_details, self).create(vals)

        self.create_directory(res.name)
        self.create_files(res)
        return res

    @api.multi
    def write(self, vals):
        res = super(collateral_details,self).write(vals)

        self.create_directory_duplicate()
        self.create_files(self)

        return res


class loan_application(models.Model):
    _inherit = "loan.application"

    @api.multi
    @api.depends("is_company_customer", "appln_no","customer_acc_id")
    def create_directory_duplicate(self):
        loan_config_ids = self.env['loan.config.directory'].search([])[0]

        path = loan_config_ids.parent_directory+'/'+loan_config_ids.loan_directory+'/'
        path2 = ''

        if self.is_company_customer == -10:
            path2 = path + loan_config_ids.loan_indiv_directory + "/"
        elif self.is_company_customer == -20:
            path2 = path + loan_config_ids.loan_compa_directory + "/"
        else:
            path2 = path + loan_config_ids.loan_indiv_directory + "/"

        path3 = path2 + self.customer_acc_id +"-"+ self.appln_no + "/"

        directory = os.path.dirname(path)
        directory2 = os.path.dirname(path2)
        directory3 = os.path.dirname(path3)
        # self.create_loan_directory()

        if not os.path.exists(directory):
            os.mkdir(directory)
            os.chmod(directory, 0777)
        if not os.path.exists(directory2):
            os.mkdir(directory2)
            os.chmod(directory2, 0777)
        if not os.path.exists(directory3):
            os.mkdir(directory3)
            os.chmod(directory3, 0777)
        return True

    @api.multi
    @api.depends("is_company_customer","appln_no","customer_acc_id")
    def create_directory(self,is_company_customer,directory_name):
        loan_config_ids = self.env['loan.config.directory'].search([])[0]

        path1 = loan_config_ids.parent_directory+'/'

        path2 = path1 + loan_config_ids.loan_directory+"/"

        path3 = ""

        if self.is_company_customer == -10:
            path3 = path2+loan_config_ids.loan_indiv_directory+"/"
        elif self.is_company_customer == -20:
            path3 = path2+loan_config_ids.loan_compa_directory+"/"
        else:
            path3 = path2+loan_config_ids.loan_indiv_directory+"/"
        
        path4 = path3 + directory_name + "/"

        directory1 = os.path.dirname(path1)
        directory2 = os.path.dirname(path2)
        directory3 = os.path.dirname(path3)
        directory4 = os.path.dirname(path4)

        if os.path.exists(directory1):
            if not os.path.exists(directory2):

                os.mkdir(directory2)
                os.chmod(directory2, 0777)
            if not os.path.exists(directory3):

                os.mkdir(directory3)
                os.chmod(directory3, 0777)

            if not os.path.exists(directory4):

                os.mkdir(directory4)
                os.chmod(directory4, 0777)
        return True

    @api.model
    def create(self,vals):
        res = super(loan_application,self).create(vals)
        appl_no = res.customer_acc_id +"-"+ res.appln_no
        if  res.is_company_customer == -10:
            appl_type = "Individual"
        elif res.is_company_customer == -20:
            appl_type = "Company"
        else:
            appl_type = "Individual"

        self.create_directory(appl_type,appl_no)
        self.create_files(res)

        return res

    @api.multi
    def write(self,vals):
        res = super(loan_application, self).write(vals)
        self.create_directory_duplicate()
        self.create_files(self)
        return res

    @api.multi
    def create_files(self,res_id):
        loan_config_ids = self.env['loan.config.directory'].search([])[0]

        store_path = ''
        if res_id.is_company_customer == -10:
            store_path = loan_config_ids.parent_directory + "/" + loan_config_ids.loan_directory + '/' \
                         + loan_config_ids.loan_indiv_directory + "/" + res_id.customer_acc_id + "-"+ res_id.appln_no + "/"
        elif res_id.is_company_customer == -20:
            store_path = loan_config_ids.parent_directory + "/" + loan_config_ids.loan_directory + '/' \
                         + loan_config_ids.loan_compa_directory + "/" + res_id.customer_acc_id +"-"+ res_id.appln_no + "/"
        else:
            store_path = loan_config_ids.parent_directory + "/" + loan_config_ids.loan_directory + '/' \
                         + loan_config_ids.loan_indiv_directory + "/" + res_id.customer_acc_id +"-"+ res_id.appln_no + "/"
        if res_id.doc_det_ids:
            for doc_id in res_id.doc_det_ids:
                file_data = doc_id.doc_file

                file_name1 = doc_id.filename
                extension = file_name1[file_name1.rfind('.'):]

                extension2 = os.path.splitext(file_name1)[0][0:].strip()

                filepath = os.path.join(store_path, extension2 + extension)
                file = base64.b64decode(file_data)
                flag = filestore_generic.FilestoreGeneric(file,extension).check_size(file,extension)


                if not flag:
                    with open(filepath, "wb") as f:
                        f.write(file)

                        f.close()

        return True

class document_details(models.Model):
    _inherit = "document.details"

    # @api.multi
    # def check_extension(self):
    #
    #     allow_ext_lst = ['.pdf', '.jpeg', '.jpg', '.gif', '.doc', '.docx', '.xls', '.xlsx']
    #     file_name1 = self.filename
    #     flag = False
    #     if file_name1:
    #
    #         extension = file_name1[file_name1.rfind('.'):]
    #
    #         if extension not in allow_ext_lst:
    #             flag = True
    #
    #     return flag

    @api.model
    def create(self, vals):
        res = super(document_details, self).create(vals)
        # flag = self.check_extension()
        flag = filestore_generic.FilestoreGeneric(res.filename).check_extension(res.filename)
        # self.check_size()
        if flag:
            raise UserError(_('You cannot upload files other than those specified.'))

        return res

    @api.multi
    def write(self, vals):
        res = super(document_details, self).write(vals)
        # flag = self.check_extension()
        flag = filestore_generic.FilestoreGeneric(self.filename).check_extension(self.filename)
        if flag:
            raise UserError(_('You cannot upload files other than those specified.'))
        return res
