# -*- encoding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api


class Loandocumento(models.Model):
    _name = "saving.management.tipo.documento"

    name = fields.Char("Nombre de tipo de documento")
    ahorros_id = fields.Many2one("saving.management.saving", "Prestamo")
    documento = fields.Binary('Documento Adjunto')
    estado = fields.Selection(
        [('ingresado', 'Ingresado'),('proceso', 'Proceso de validacion'),('validada', 'Validado')], string='Estado de documento', default='ingresado')
    nota = fields.Text("Nota")
