# -*- encoding: utf-8 -*-
import odoo
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
#import  UserError

class WizardCalcularValidar(models.TransientModel):
    """Wizard para realizar la creacion de aportes y validar la transaccion masiva"""
    _name = 'loan.wizard.calcular.validar'
    _description = 'Wizar Calcula Apotes y Valida Transaccion '

    @api.multi
    def CalcularValidarTransaccion(self):
        #print "#" * 20
        #print "Ingersando al wizard de crear y validar transaccion con seleccion masiva"
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for record in self.env['loan.aportaciones'].browse(active_ids):
            #print "record.state: ", record.state
            if record.state in ('draft','done'):
                record.set_values()
                #ejecuta el calculo distribucion y construye asiento contable
                record.action_ingresar()
            else:
                raise UserError(_("Hay aportaciones que ya estan ingresados o cancelados"))
        return {'type': 'ir.actions.act_window_close'}

# class WizardAsientoAporteDistribuido(models.TransientModel):
#     """Wizard para realizar la creacioncontabilizacion de aportes  masiva"""
#     _name = 'loan.wizard.contabilizar'
#     _description = 'Wizar Contabiliza Apotes '
#
#     @api.multi
#     def AporteDistribuidoAsiento(self):
#         #print "#" * 20
#         #print "Ingersando al wizard de crear y validar transaccion con seleccion masiva"
#         context = dict(self._context or {})
#         active_ids = context.get('active_ids', []) or []
#         for record in self.env['loan.aportaciones'].browse(active_ids):
#             #print "record.state: ", record.state
#             if record.state in ('draft','done'):
#                 # ejecuta la contabilizacion del asiento distribuido, llama action_ingresar de la raiz
#                 # pero este llama a contabilizar y entonces se ejecuta el metodo sobreescrito
#                 record.action_ingresar()
#             else:
#                 raise UserError(_("Hay aportaciones que ya estan ingresados o cancelados"))
#         return {'type': 'ir.actions.act_window_close'}

class WizardContabilizaAporEsp(models.TransientModel):
    """Wizard para realizar la creacion de aportes y validar la transaccion masiva"""
    _name = 'loan.wizard.contabiliza.spc'
    _description = 'Wizar Calculacontabiliza Transaccion Esp '

    # para accion batch en aportaciones especiales
    @api.multi
    def ContabilizaTranEspec(self):
        #toma el contexto a seleccionar
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for record in self.env['loan.aportaciones.esp'].browse(active_ids):
            #print "record.state: ", record.state
            if record.state in ('draft','done'):
                record.action_ingresar()
                # ejecuta la contabilizacion, tiene mismo nombre de funcion pero esta en otro modelo
            else:
                raise UserError(_("Hay aportaciones especiales que ya estan ingresados o cancelados"))
        return {'type': 'ir.actions.act_window_close'}
