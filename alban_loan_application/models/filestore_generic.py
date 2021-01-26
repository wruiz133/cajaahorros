import sys,os
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

# class FilestoreGeneric(models.Model):
class FilestoreGeneric(object):
    # _name = 'filestore.generic'
    def __init__(self, file_data='', extension='',file_name=''):
        self.file_data = file_data
        self.extension = extension
        self.file_name = file_name

    def check_size(self,file_data,extension):
        file_size = sys.getsizeof(file_data)

        allow_ext_lst = ['.jpeg', '.jpg', '.gif', '.doc', '.docx', '.xls', '.xlsx']
        flag = False
        if extension == '.pdf' and file_size > 3000000:
        # if extension == '.pdf' and file_size > 300000:
            flag = True
            raise UserError(_('File size exceeds the specified size limit!'
                              '\n Kindly upload files of proper size..'))
        else:
            for ext in allow_ext_lst:
                # print 'in the else loop of check_size'
                if extension == ext and file_size > 500000:
                # if self.extension == ext and file_size > 100000:
                    flag = True
                    raise UserError(_('File size exceeds the specified size limit!'
                                      '\n Kindly upload files of proper size..'))

        return flag

    # @api.multi
    def check_extension(self,file_name1):
        allow_ext_lst = ['.pdf', '.jpeg', '.jpg', '.gif', '.doc', '.docx', '.xls', '.xlsx']
        # file_name1 = self.filename
        flag = False
        if file_name1:
            extension = file_name1[file_name1.rfind('.'):]
            # self.type = extension +" document"
            if extension not in allow_ext_lst:
                flag = True
        return flag