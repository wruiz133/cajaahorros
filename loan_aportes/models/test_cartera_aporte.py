#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp


#aumenta el fk al loan.aportaciones contra el modelo
class Aportaciones(models.Model):
    _inherit = "loan.aportaciones"

    cartera_test_id = fields.Many2one("cartera.aportes.test", "Aportantes", states={'draft': [('readonly', False)]})
    #nro_deposito = fields.Char("Numero del Deposito")

#modelo para receptar los noaportantes dentro de un periodo
class HrPayslipRun(models.Model):
    _name = 'cartera.aportes.test'
    _description = 'Cartera Aportes Test'

    name = fields.Char(required=True, readonly=True, states={'draft': [('readonly', False)]})
    aportes_ids = fields.One2many('loan.aportaciones', 'cartera_test_id', string='Estado Cartera', readonly=True,
        states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('close', 'Close'),
        ('nopay', 'Nopay'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')
    date_start = fields.Date(string='Date From', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, default=time.strftime('%Y-%m-01'))
    date_end = fields.Date(string='Date To', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    credit_amount = fields.Float(string='Monto Aporte',
        states={'draft': [('readonly', False)]},
        help="El monto es la aportacion general del mes establecido para cada socio")
    nopay_list_ids = fields.One2many('loan.noaporta', 'noaporta_id', string='No Pagaron Aporte')

    @api.multi
    def draft_cartera_aportes_test(self):
        return self.write({'state': 'draft'})

    @api.multi
    def close_cartera_aportes_test(self):
        return self.write({'state': 'close'})

#modelo que es llamado para registro de no aportantes dado una lista
class Naportaciones(models.Model):
    _name = "loan.noaporta"

    noaporta_id = fields.Many2one("cartera.aportes.test", "No Aportantes", ondelete="cascade", required=True, states={'draft': [('readonly', False)]})
    cliente_id = fields.Many2one("res.partner", "Cliente", required=True, states={'draft': [('readonly', False)]})
    monto_aportacion = fields.Float("Monto de aportación", required=True, states={'draft': [('readonly', False)]})
    fechai = fields.Date("Fecha de aportación", required=True, states={'draft': [('readonly', False)]})
    fechaf = fields.Date("Fecha de aportación", required=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
            ('draft','Borrador'),
            ('cancel','Cancelada'),
            ('done','Ingresada'),
            ('nopay', 'NoPagada'),
            ('Pay', 'Pagada'),
        ], string='Estado', index=True, default='draft')

