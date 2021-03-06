# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _ 
from datetime import datetime, timedelta 
import odoo.addons.decimal_precision as dp 
#from itertools import groupby 
#from odoo.tools.misc import formatLang 
#from odoo.exceptions import UserError 
#from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT 

class s_apactivosfijosordenmov(models.Model): 
    _name = 's.apactivosfijosordenmov' 
    _inherit = ['mail.thread']
    _log_access = True 
   # _rec_name = name 
   # _table = 's.apactivosfijosordenmov' 
   # _parent_name = "parent_id"   # _parent_store = True   # _parent_order = 'name'   # _order = 'parent_left'    _description = 'La clase s_apactivosfijosordenmov '
    numorden = fields.Integer(string='Numorden', help='Número de orden', required=0, track_visibility='onchange', size=8 ) 
    fecha = fields.Date(string='Fecha', help='Fecha', required=0, track_visibility='onchange' ) 
#@api.one
#def compute_user_todo_count(self): 
#    self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)]) 
#    user_todo_count      = fields.Integer('User To-Do Count', compute='compute_user_todo_count') 
