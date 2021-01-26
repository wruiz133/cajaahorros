# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details. 
from odoo import api, fields, models, _ 
from datetime import datetime, timedelta 
import odoo.addons.decimal_precision as dp 
#from itertools import groupby 
#from odoo.tools.misc import formatLang 
#from odoo.exceptions import UserError 
#from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT 

class s_persona(models.Model): 
    _name = 's.persona' 
    _inherit = ['mail.thread']
    _log_access = True 
   # _rec_name = name 
   # _table = 's.persona' 
   # _parent_name = "parent_id"   # _parent_store = True   # _parent_order = 'name'   # _order = 'parent_left'    _description = 'La clase s_persona '
    estadocivil_id = fields.Integer(string='Estadocivil id', help='Estado civil de la persona soltero casada divorciada viuda unin libre o de hecho. ', required=1, track_visibility='onchange', size=9 ) 
    estado_id = fields.Boolean(string='Estado id', help='Estado puede ser activo inactivo', required=1, track_visibility='onchange' ) 
    name = fields.Char(string='Estado id', help='Estado puede ser activo inactivo', required=1, track_visibility='onchange' ) 
    fecha_nacimiento = fields.Datetime(string='Fecha nacimiento', help='Fecha nacimiento ao mes da', required=1, track_visibility='onchange' ) 
    persona_id = fields.Integer(string='Persona id', help='Identificador unico de persona', required=0, track_visibility='onchange', size=9 ) 
    sexo_id = fields.Integer(string='Sexo id', help='Sexo de la person masculino o femenino.', required=1, track_visibility='onchange', size=9 ) 
#@api.one
#def compute_user_todo_count(self): 
#    self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)]) 
#    user_todo_count      = fields.Integer('User To-Do Count', compute='compute_user_todo_count') 
