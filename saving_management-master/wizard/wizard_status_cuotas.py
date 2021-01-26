# -*- encoding: utf-8 -*-
import odoo.addons.decimal_precision as dp
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import Warning


class WizardStatusCuotas(models.TransientModel):
    _name = 'saving.wizard.generar.cuotas'
    _description = 'Asistente de Status de Cuotas'
    _rec_name = 'prestamo_id'

    def _get_prestamo(self):
        contexto = self._context
        if 'active_id' in contexto:
            saving_obj = self.env["saving.management.saving"].browse(contexto['active_id'])
            return saving_obj

    # Información General
    date_generation = fields.Date(string="Fecha de Generación", required=True, default=fields.Date.today)
    prestamo_id = fields.Many2one("saving.management.saving", "Prestamo", default=_get_prestamo)
    lista_prestamos = fields.Many2one("saving.management.saving", "Prestamo Numero", default = prestamo_id)
    @api.multi
    def generar_status_cuotas(self, prestamo_id):
        date_generation = fields.Date.today()
        if self.date_generation:
            date_generation = self.date_generation
        # WR:llave para uno o todos los que cumplen el search, se aumenta el campo de seleccion por prestamo
        # print "prestamo_id=%s " % self.lista_prestamos.id
        print("si entro con dato prestamo_id   ",prestamo_id)
        if prestamo_id:
            # viene del contexto
            prestamos_obj = self.env["saving.management.saving"].search([('id', '=', self.lista_prestamos.id)])
        if self.lista_prestamos.id in (False, None):
            # si no escoge prestamo de la lista
            prestamos_obj = self.env["saving.management.saving"].search([('state', '=', 'progreso')])
        for prestamo in prestamos_obj:
            for cuota in prestamo.cuota_ids:
                if date_generation > cuota.fecha_pago and not cuota.state == 'pagada' and not cuota.saldo_pendiente == 0.0:
                    fecha_run = (datetime.strptime(date_generation, '%Y-%m-%d'))
                    fecha_cuota = (datetime.strptime(cuota.fecha_pago, '%Y-%m-%d'))
                    diferencia_fecha = (fecha_run - fecha_cuota).days #relativedelta(day=fecha_cuota.day, months=fecha_cuota.month)
                    mora = 0.0
                    if cuota.registro_tipo == 'deposito':
                        mora = ((cuota.interes * (prestamo.mora_id.tasa_mora / 100)) / 30) * diferencia_fecha
                    if cuota.registro_tipo == 'retiro':
                        mora = ((cuota.interes_contra * (prestamo.mora_id.tasa_mora / 100)) / 30) * diferencia_fecha
                    if round(cuota.saldo_pendiente, 10) >= round(cuota.monto_cuota, 10):
                        #print "Cuota de prestamo igual a saldo"
                        # mora = ((cuota.monto_cuota * (prestamo.mora_id.tasa_mora / 100)) / 30) * diferencia_fecha
                        cuota.saldo_pendiente = cuota.monto_cuota #+ mora
                        # cuota.mora = cuota.saldo_pendiente - cuota.monto_cuota
                        cuota.mora = mora
                    else:
                        # mora = ((cuota.saldo_pendiente * (prestamo.mora_id.tasa_mora / 100)) / 30) * diferencia_fecha
                        cuota.saldo_pendiente = cuota.saldo_pendiente + mora
                        cuota.mora = mora
                    cuota.write({'state': 'morosa'})
                if date_generation == cuota.fecha_pago and not cuota.state == 'pagada' and not cuota.saldo_pendiente == 0.0:
                    cuota.write({'state': 'vigente'})
                    cuota.mora = 0.0
                    # evitar sobre escribir cuando se ha pagado parcial en estado no vigente WHRC
                    if round(cuota.saldo_pendiente,2) == round(cuota.monto_cuota,2):
                        cuota.saldo_pendiente = cuota.monto_cuota
        prestamos_obj.write({'state': 'desembolso'})
class WizardGeneratePlanCuotas(models.TransientModel):
    """DCLS""" 
    _name = 'saving.wizard.generar.plan.cuotas'
    _description = 'Asistente Generar Plan Cuotas'
    
    @api.multi
    def generate_plan_cuotas(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['saving.management.saving'].browse(active_ids):
            if record.state not in ('cotizacion'):
                raise UserError(_("Selected saving(s) cannot be confirmed as they are not in 'Aprobado' state."))
            
            record.get_generar_cuotas()
        return {'type': 'ir.actions.act_window_close'}

class WizardAprobarPlan(models.TransientModel):
    """DCLS""" 
    _name = 'saving.wizard.approve'
    _description = 'Asistente Aprobar Plan Cuotas'
    
    @api.multi
    def generate_approve(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['saving.management.saving'].browse(active_ids):
            if record.state not in ('progress','desembolso'):
                raise UserError(_("Selected saving(s) cannot be confirmed."))
            
            record.action_aprobar()
        return {'type': 'ir.actions.act_window_close'}
    
    
class WizardGenerarContabilidad(models.TransientModel):
    """DCLS""" 
    _name = 'saving.wizard.generate.accounting'
    _description = 'Asistente Generar Contabilidad'
    
    @api.multi
    def generate_accounting(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['saving.management.saving'].browse(active_ids):
            if record.state not in ('aprobado','desembolso'):
                raise UserError(_("Selected saving(s) cannot be confirmed."))
            
            record.generar_contabilidad()
        return {'type': 'ir.actions.act_window_close'}
       