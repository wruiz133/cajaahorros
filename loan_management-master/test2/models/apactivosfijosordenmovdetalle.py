# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _ 
from datetime import datetime, timedelta 
import odoo.addons.decimal_precision as dp 
#from itertools import groupby 
#from odoo.tools.misc import formatLang 
#from odoo.exceptions import UserError 
#from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT 

class s_apactivosfijosordenmovdetalle(models.Model): 
    _name = 's.apactivosfijosordenmovdetalle' 
    _inherit = ['mail.thread']
    _log_access = True 
   # _rec_name = name 
   # _table = 's.apactivosfijosordenmovdetalle' 
   # _parent_name = "parent_id"   # _parent_store = True   # _parent_order = 'name'   # _order = 'parent_left'    _description = 'La clase s_apactivosfijosordenmovdetalle '
    valordepreciacionespecial = fields.Float(string='Valordepreciacionespecial', help='Valor de la depreciacion especial', required=1, track_visibility='onchange', size=8, digits=dp.get_precision('Valordepreciacionespecial' )) 
    valordepreciacionrevalorizacion = fields.Float(string='Valordepreciacionrevalorizacion', help='Valor de la depreciacion revalorizado', required=1, track_visibility='onchange', size=8, digits=dp.get_precision('Valordepreciacionrevalorizacion' )) 
    valordepreciacionmejoras = fields.Float(string='Valordepreciacionmejoras', help='Valor de la depreciacion mejoras', required=1, track_visibility='onchange', size=8, digits=dp.get_precision('Valordepreciacionmejoras' )) 
    fechacomp = fields.Datetime(string='Fechacomp', help='Fecha que se modifico', required=0, track_visibility='onchange' ) 
#@api.one
#def compute_user_todo_count(self): 
#    self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)]) 
#    user_todo_count      = fields.Integer('User To-Do Count', compute='compute_user_todo_count') 
