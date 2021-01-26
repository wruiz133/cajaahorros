# -*- encoding: utf-8 -*-
from odoo import models, fields, api

class Customer(models.Model):
    _inherit = "res.partner"

    def open_partner_history_loan(self):
        '''
        This function returns an action that display invoices/refunds made for the given partners.
        '''
        action = self.env.ref('loan_management-master.loan_prestamo_esperando_aprobacion_action')
        result = action.read()[0]
        result['domain'] = [('partner_id', 'child_of', self.ids)]
        return result


    @api.one
    def get_ahorros(self):
        saldo_aportaciones = 0.0
        saldo_ahorros = 0.0
        for line in self.aportaciones_ids:
            if line.state == 'done':
                if line.tipo_aportacion == 'aportacion':
                    saldo_aportaciones += line.monto_aportacion
                else:
                    saldo_ahorros += line.monto_aportacion
        self.total_ahorros = saldo_ahorros
        self.total_aportaciones = saldo_aportaciones
        self.saldo_cliente = self.total_ahorros + self.total_aportaciones

    prestamos_ids = fields.One2many("loan.management.loan", "afiliado_id", "Prestamos de Cliente" )
    identidad = fields.Char("Identidad")
    rtn = fields.Char("RTN")
    aportaciones_ids = fields.One2many("loan.aportaciones", "cliente_id", "Prestamos de Cliente", domain=[('state', '=', 'done')])
    total_ahorros = fields.Monetary("Ahorros", compute=get_ahorros)
    total_aportaciones = fields.Monetary("Aportaciones", compute=get_ahorros)
    saldo_cliente = fields.Monetary("Saldo de Cliente", compute=get_ahorros)
