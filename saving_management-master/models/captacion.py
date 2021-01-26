# -*- encoding: utf-8 -*-
from odoo import models, fields, api


class Aportaciones(models.Model):
    _name = "saving.captacion"
    _order = 'fecha asc'

    cliente_id = fields.Many2one("res.partner", "Cliente", required=True, domain=[('customer', '=', True)])
    fecha = fields.Date("Fecha de pago", required=True)
    ahorros_id = fields.Many2one("saving.management.saving", "Prestamo", required=True)
    importe_pagado = fields.Float("Importe Pagado", required=True)
    observaciones = fields.Char("Observaciones")
    state = state = fields.Selection([
            ('borrador','Borrador'),
            ('cancelado','Cancelado'),
            ('done', 'Validado'),
        ], string='Estado', index=True)

    name = fields.Char("Número de pago")
    cuotas = fields.Many2many("saving.management.saving.cuota", string="Abono a Cuota(s)")
    cuota_ids = fields.One2many("saving.pagos.cuotas", "pago_id", "Cuotas Pagadas")
    asiento_id = fields.Many2one("account.move", "Asiento Contable")

class Aportaciones(models.Model):
    _name = "saving.pagos.cuotas" 
    _rec_name = 'numero_cuota'

    pago_id = fields.Many2one("saving.captacion", "Número de Pago", ondelete="cascade")
    monto_cuota = fields.Float("Monto de Cuota")
    mora = fields.Float("Mora")
    numero_cuota = fields.Integer("# de cuota", readonly=True)
    saldo_pendiente = fields.Float("Saldo de Cuota")

