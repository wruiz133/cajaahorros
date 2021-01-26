from odoo import api, fields, models, _
from tempfile import TemporaryFile
import base64
import csv
import StringIO
import time
import logging
logger = logging.getLogger(__name__)


class import_village(models.TransientModel):
    _name ='import.village'

    upload_transactions = fields.Binary(string='Select File', required=True)
    
    
    @api.multi
    def import_data(self):
        country_obj = self.env['res.country']
        district_obj = self.env['admin.district']
        commune_obj = self.env['admin.municipal']
        village_obj = self.env['admin.village']
        
        csv_datas = self.upload_transactions
        print "--------csv_datas-----------" , csv_datas
        
        fileobj = TemporaryFile('w+')
        fileobj.write(base64.decodestring(csv_datas))
        fileobj.seek(0)
        str_csv_data=fileobj.read()
        lis=csv.reader(StringIO.StringIO(str_csv_data), delimiter='\t')

        rownum = 0
        for row in lis:
            print "--------row-----------" , row
            if row == ['', '', '', '', '', '']:
                print "-------------1------"
                pass
            elif rownum==0:
                print "-------------rownum------",rownum
                header = row
                print "-------------header------",header
            else:
                print "--------row-----------" , row
                print "--------row-----------" , row[0].split(",")
                row_new = row[0].split(",")
                
                village_code = row_new[0]
                district_code = row_new[1]
                district = row_new[2]
                commune_code = row_new[3]
                country = row_new[6]
                village = row_new[7]
                
                country_id = country_obj.search([('name','=', country)])
                print "--------country_id-----------" , country_id
                
                district_id = district_obj.search([('district_code','=', district_code), ('circle_id','=',country_id.id)])
                print "--------district_id-----------" , district_id
                
                commune_id = commune_obj.search([('district_id','=', district_id.id), ('circle_id','=',country_id.id),('district_code','=', commune_code)])
                print "--------commune_id-----------" , commune_id
                
                vals = {
                    'circle_id' : country_id.id,
                    'district_id' : district_id.id,
                    'municipal_id' : commune_id.id,
                    'district_code' : village_code,
                    'name' : village,
                }
                
                village_id = village_obj.create(vals)
                print "--------village_id-----------" , village_id
                
            rownum+=1
             
# class product_code(models.Model):
#     _name = "product.code"
#
#     name = fields.Integer(string='Code')
#     quote_rate = fields.Float(string='Quoted Int Rate')
#     daily_rate = fields.Float(string='Daily Interest Rate')
#
#     calc_meth =fields.Char(string='Calculation Meth')
#     index_curr = fields.Many2one('res.currency',string='Index Currency')
#     pay_curr = fields.Many2one('res.currency',string='Payment Currency')
#
#     sch_type = fields.Char(string='Schedule Type')
#     term_length = fields.Char(string='Term Length')
#     pay_day = fields.Char(string='Payment Day')
#     rounding = fields.Char(string='Rounding')
#
#     proc_fees = fields.Float(string='Processing Fee')
#     grace_per = fields.Integer(string='Grace Period')