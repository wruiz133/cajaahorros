# -*- encoding: utf-8 -*-
from odoo import models, fields, api


class savingType(models.Model):
    _name = "saving.management.saving.type"
    _inherit = ['mail.thread']

    name = fields.Char("Tipo de Prestamo", required=True)
    active = fields.Boolean(string="Prestamo Activo", default=True)
    description = fields.Text("Notas Generales")
    monto_maximo = fields.Float("Monto Maximo", help="Monto maximo para el prestamo", required=True)
    monto_minimo = fields.Float("Monto Minimo", help="Monto minimo para el prestamo", required=True)
    plazo_pago_id = fields.Many2one("saving.management.saving.plazo", "Plazo de tiempo", required=True)
    tasa_interes_id = fields.Many2one("saving.management.saving.interes", "Tasa de Interes", required=True)
    metodo_calculo = fields.Selection([('cuotanivelada', 'Nivelada o Francesa'),
                                       ('plana', 'Cuota Plana'),
                                       ('alemana', 'Alemana'),
                                       ], 
        string='Metodo de Cálculo', default='cuotanivelada', required=True)
    tipo_producto = fields.Selection([('av', 'Ahorro a la Vista'),
                                       ('pf', 'Ahorro Plazo Fijo'),
                                       ('ap', 'Ahorro Programado'),
                                       ],
        string='Tipo Producto', default='av', required=True)
    #cuenta_ingreso =  fields.Many2one('account.account', 'Cuenta de Ingresos')
    cuenta_diferido =  fields.Many2one('account.account', 'Diferido pasivo')
    cuenta_ingreso =  fields.Many2one('account.account', 'Diferidos activo')
    cuenta_intereses_mora =  fields.Many2one('account.account', 'Impuesto', required=True)
    cuenta_intereses =  fields.Many2one('account.account', 'Interes', required=True)
    cuenta_cartera = fields.Many2one('account.account', 'Cuenta Cartera Socio ', required=True)


class savingPlazo(models.Model):
    _name = "saving.management.saving.plazo"

    name = fields.Char("Nombre de Plazo")
    numero_plazo = fields.Integer("Numero de plazos", required=True)
    active = fields.Boolean(string="Activo", default=True)
    tipo_plazo = fields.Selection([('anual', 'Años'),('quincenal', 'Quincenas'), ('mensual', 'Meses'), ('diario', 'Diario')], string='Periodos', default='mensual')

    @api.model
    def create(self, vals):
        plazo = vals.get("numero_plazo")
        tipo = vals.get("tipo_plazo")
        description = ""
        if tipo == 'quincenal':
            description = "Quincenas"
        if tipo == "mensual":
            description = "Meses"
        if tipo == "anual":
            description = "Años"

        vals["name"] = str(plazo) + " " + description
        return super(savingPlazo, self).create(vals)


class savingInteres(models.Model):
    _name = "saving.management.saving.interes"

    name = fields.Char("Nombre de Tasa")
    tasa_interes = fields.Float("Tasa de interes (%)", required=True)
    capitalizable = fields.Selection([('anual', 'Anual'),('quincenal', 'Quincenal'), ('mensual', 'Mensual'), ('anual', 'Anual')],
        string='Capitalizacion', default='anual')
    active = fields.Boolean(string="Activo", default=True)

    @api.model
    def create(self, vals):
        capitalizable = vals.get("capitalizable")
        tasa = vals.get("tasa_interes")
        vals["name"] = str(tasa) + "%" + " " + capitalizable
        return super(savingInteres, self).create(vals)

