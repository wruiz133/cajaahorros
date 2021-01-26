# -*- encoding: utf-8 -*-
from odoo import models, fields, api


class LoanMora(models.Model):
    _name = "saving.management.saving.mora"
    _inherit = ['mail.thread']

    name = fields.Char("IRenta ", required=True)
    active = fields.Boolean(string="Tasa IR Activa", default=True)
    description = fields.Text("Notas Generales")
    dias_mora = fields.Integer("Dias de Mora")
    tasa_mora = fields.Float("Tasa impuesto renta", help="Tasa IR", required=True)

    # Cuenta contables
    cuenta_mora = fields.Many2one('account.account', 'Cta Impt Renta', required=True)
