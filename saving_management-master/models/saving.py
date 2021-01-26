# -*- encoding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import openerp.addons.decimal_precision as dp


class saving_cargos(models.Model):
    _name = "saving.recargos"
    _inherit = ['mail.thread']

    name = fields.Selection([('cargos','Otros Cargos'),
                             ('legalizacion','Legalizacion'),
                             ('constante_local','Constante Local'),
                             ('seguro','Seguro'),
                             ('imp_solca','Impuesto SOLCA'),
                             ('imp_infa','Impuesto INFA'),
                             ('retencion_ahorros','Retencion Ahorros'),
                             ('retencion_aportes','Retencion Aportes'),
                             ('encaje_ahorros','Encaje ahorros'),
                             ('encaje_aportacion','Encaje cetificados de aportacion'),
                             ('total_fondos_propios','Total fondos propios'),
                             ], string = "ReCargos" , required=True)
    cargos_id = fields.Many2one("saving.management.saving", "Saving")
    amount = fields.Float("Monto")

    
    
class Saving(models.Model):
    _name = "saving.management.saving"
    _order = 'fecha_solicitud asc'
    _inherit = ['mail.thread']

    def get_currency(self):
        return self.env.user.company_id.currency_id.id

    # @api.depends('cuota_ids')
    @api.one
    def get_saldo(self):
        for ahorro in self:
            saldo = 0.0
            mora = 0.0
            insoluto = 0.0
            liquidar = 0.0
            interes = 0.0
            interes_insoluto = 0.0
            parcial = 0.0
            done = False
            nodone = True
            for line in self.cuota_ids:
                # print "numerocuota:  ", line.numero_cuota
                if line.state == 'pagada':
                    saldo += line.monto_cuota
                    #interes += line.interes
                    done = True
                if line.state in ('vigente','morosa'):
                    # WHRC aplica para liquidar ahorros en cualquier momento
                    if line.monto_pagado > 0:
                        parcial = line.monto_cuota - line.monto_pagado
                    else:
                        parcial = line.monto_cuota
                    liquidar += parcial
                    done = False
                if line.state == 'novigente' and self.state not in ('liquidado'):
                    insoluto += line.capital
                    liquidar += line.capital
                    interes_insoluto += line.interes
                    done = False
                if line.state not in ('pagada') :
                    done = False
                    interes += line.interes
                mora += line.mora

            #self.interes = interes
	        # campos clculados adicionales que dan mas informacion  WR
            self.monto_recaudado = saldo
            self.monto_insoluto = insoluto
            self.interes_insoluto = interes_insoluto
            self.saldo_liquidar = liquidar
            # WR desgravamen > 0 ssi van desde 2019
            desgrava_fecha = (datetime.strptime(self.fecha_solicitud, '%Y-%m-%d'))
            fecha_pago = desgrava_fecha.replace(day=1) + relativedelta(months=1) + timedelta(days=-1)
            self.fecha_pago = fecha_pago
            # print "fecha es: %s",desgrava_fecha.year
            if desgrava_fecha.year >= 2019:
                self.gastos_papeleria = self.monto_solicitado * 0.01
            else:
                self.gastos_papeleria = 0.0
            # print "el valor al calculo desgravamen  ", self.gastos_papeleria
            self.mora_ahorro = mora
            # calculo neto para reporteo comprobate egreso
            self.monto_neto_desembolso = self.monto_solicitado - self.gastos_papeleria
            #verifica que todos las cuotas sean pagadas y liquida ahorro WHRC
            for line in self.cuota_ids:
                # print ("numerocuota despues:  ", line.numero_cuota, "  estado  ",line.state)
                if line.state == 'pagada':
                    done = True
                else:
                    nodone = False
            done = nodone
            # print "el valor done   ", done
            self.ahorro_done = done
            if self.mora_ahorro > 0.0:
                self.ahorro_moroso = True
            if self.ahorro_done and self.cuota_ids:
                self.write({'state': 'liquidado'})
            # se liquida aun habiendo algun resto en alguna cuota
            if self.state == 'liquidado':
                # print "entro aqui ..."
                self.saldo_pendiente = 0.0
            else:
                self.saldo_pendiente = self.total_monto - saldo
    # funciones default

    # Valores numericos

    total_interes = fields.Float("Total de interes", states={'cotizacion': [('readonly', False)]})
    total_monto = fields.Float("Importe Total", states={'cotizacion': [('readonly', False)]})
    cuota_ahorro = fields.Float("Cuota de ahorro", states={'cotizacion': [('readonly', False)]})
    monto_solicitado = fields.Float("Monto ", required=True, default = 0.1)
    saldo_pendiente = fields.Float("Saldo pendiente", readonly=True,store=True, compute='get_saldo')
    mora_ahorro = fields.Float("Mora de ahorro", readonly=True, compute='get_saldo')
    # Control saldos whr
    monto_recaudado = fields.Float("Monto Cobrado", readonly=True, store=True, compute='get_saldo')
    monto_insoluto = fields.Float("Monto Insoluto", readonly=True, compute='get_saldo')
    saldo_liquidar = fields.Float("Saldo a Liquidar", readonly=True, compute='get_saldo')
    interes = fields.Float("Interes", readonly=True)
    interes_insoluto = fields.Float("Interes Insoluto", readonly=True, store=True)
    # Gastos de ahorro
    gastos_papeleria = fields.Monetary("Desgravamen", compute='get_saldo')
    gasto_timbre = fields.Monetary("Mnto Reliquid.")
    monto_comision = fields.Monetary("Comisióm bancaria")
    total_desembolso = fields.Float("Monto a desembolsar")
    fecha_desembolso = fields.Date("Fecha de desembolso", default=fields.Date.today)
    referencia_desembolso = fields.Char("No. de Cheque/ Transferencia")
    notas_desembolso = fields.Text("Notas de desombolso")
    # Campos generales fields.Date.today

    currency_id = fields.Many2one("res.currency", "Moneda", domain=[('active', '=', True)], default=get_currency)
    name = fields.Char("Numero de ahorro", required=True, default=lambda self: self.env['ir.sequence'].next_by_code('ahorros'))
    afiliado_id = fields.Many2one("res.partner", "Cliente", required=True, domain=[('customer', '=', True)], states={'cotizacion': [('readonly', False)]})
    fecha_solicitud = fields.Date("Fecha de solicitud", required=True, default=fields.Date.today, states={'cotizacion': [('readonly', False)]})
    fecha_aprobacion = fields.Date("Fecha de aprobación", states={'cotizacion': [('readonly', False)]})
    fecha_pago = fields.Date("Fecha Inicial(Pagos)", states={'cotizacion': [('readonly', False)]})
    fecha_capitaliza = fields.Date("Al: ", readonly=True)
    currency_id = fields.Many2one("res.currency", "Moneda", default=lambda self: self.env.user.company_id.currency_id)
    # Parametros
    plazo_pago = fields.Integer("Plazo Fondo Ahorro", required=True, states={'cotizacion': [('readonly', False)]})
    periodo_plazo_pago = fields.Selection([('dias', 'Días'), ('meses', 'Meses'), ('anios', 'Anual')], string='Capitalizacion', default='meses', required=True)
    tasa_interes = fields.Float("Tasa Interes Anual", required=True)
    notas = fields.Text("Notas")
    state = fields.Selection([('cotizacion', 'Cotizacion'), 
                              ('progress', 'Esperando Aprobacion'), 
                              ('rechazado', 'Rechazado'), 
                              ('aprobado', 'Aprobado'),
                              ('desembolso', 'En desembolso'),
                              ('progreso', 'En progreso'),
                              ('liquidado', 'Liquidado')
                              ], string='Estado de ahorro',type='selection', default='cotizacion')
    tipo_ahorro_id = fields.Many2one("saving.management.saving.type", "Tipo de ahorro", required=True, states={'cotizacion': [('readonly', False)]})
    cuota_ids = fields.One2many("saving.management.saving.cuota", "ahorros_id", "Cuotas de ahorro")
    cuotasaving_ids = fields.One2many("saving.management.saving.cuota", "ahorros_id", "Depositos-retiros")
    doc_ids = fields.One2many("saving.management.tipo.documento", "ahorros_id", "Documentos de validacion")
    move_id = fields.Many2one('account.move', 'Asiento Contable', ondelete='restrict', readonly=True)
    #move_id = fields.Many2one('account.move', 'Asiento Contable', readonly=True, ondelete="cascade")
    journal_id = fields.Many2one("account.journal", "Banco",default=lambda self: self.env['account.journal'].browse(9), domain=[('type', '=', 'bank')])
	#WRLS
    monto_neto_desembolso = fields.Float("Desembolso Neto", compute='get_saldo',store=True)
    cuenta_desgravamen =  fields.Many2one('account.account','Cuenta Desgravamen',default=lambda self: self.env['account.account'].browse(1188))
    seq_desembolso = fields.Char("Número Desembolso", default=lambda self: self.env['ir.sequence'].next_by_code('desembolso'), states={'draft': [('readonly', False)]})
    forma_producto = fields.Selection("Forma Ahorro", related='tipo_ahorro_id.tipo_producto', store=True)

    # Información de pagostipo_ahorro_id
    pagos_ids = fields.One2many("saving.captacion", "ahorros_id", "Pagos de Cuotas")
    mora_id = fields.Many2one("saving.management.saving.mora", "Tasa Impuesto",default=lambda self: self.env['saving.management.saving.mora'].browse(1) )
    ahorro_moroso = fields.Boolean("ahorro en mora", compute='get_saldo')
    ahorro_done = fields.Boolean("ahorro liquidado", compute='get_saldo')
    cierre = fields.Boolean("cierre ", default=False, help='cierre de la libreta ahorros')
    #HTC datos
    cargos_ids = fields.One2many("saving.recargos", "cargos_id", "Cargos Credito")

    
    #tir = fields.Float("TIR" )
    #tea = fields.Float("TEA" )
    
    cargos = fields.Float("Otros cargos")
    legalizacion = fields.Float("Legalizacion")
    constante_local = fields.Float("Cont Local")
    seguro = fields.Float("Seguros")
    imp_solca = fields.Float("Imp. SOLCA")
    imp_infa = fields.Float("Imp. INFA")
    imp_infa = fields.Float("Imp. INFA")
    retencion_ahorros = fields.Float("Ret. ahorros")
    retencion_aportes = fields.Float("Ret. aportes")
    saldo_libreta =  fields.Float("Saldo Libreta: ")
    
    encaje_aportacion = fields.Float("Encaje cetificados de aportacion")
    encaje_ahorros = fields.Float("Encaje ahorros")
    total_fondos_propios = fields.Float("Total fondos propios")
    
    
    grupo = fields.Selection([('cotizacion', 'Cotizacion'), 
                              ('progress', 'Esperando Aprobacion'), 
                              ], string='Estado de ahorro',  readonly=True, default='cotizacion')

    @api.onchange("fecha_solicitud")
    def fecha_onchange(self):
        fecha0 = datetime.strptime(self.fecha_solicitud, '%Y-%m-%d')
        fecha1 = fecha0.replace(day=1) + relativedelta(months=1) + timedelta(days=-1)
        self.fecha_pago = fecha1
    @api.onchange("monto_solicitado")
    def monto_solicitado_onchange(self):
        if self.tipo_ahorro_id.monto_maximo > 0.0 and self.monto_solicitado > self.tipo_ahorro_id.monto_maximo:
            raise Warning(_('Tipo AHORRO! permite {}'.format(self.tipo_ahorro_id.monto_maximo)))

    @api.onchange("tipo_ahorro_id")
    def _get_tasa_plazo(self):
        self.plazo_pago = self.tipo_ahorro_id.plazo_pago_id.numero_plazo
        self.tasa_interes = self.tipo_ahorro_id.tasa_interes_id.tasa_interes
        #self.periodo_plazo_pago = self.tipo_ahorro_id.tasa_interes_id.capitalizable

    # Generar partida de desembolso
    def generar_partida_contable(self):
        account_move = self.env['account.move']
        lineas = []
        if self.tipo_ahorro_id.tipo_producto == 'pf':
            vals_debit = {
                'debit': self.monto_solicitado,
                'credit': 0.0,
                'amount_currency': 0.0,
                'name': 'Captacion de ahorro - banco',
                # 'account_id': self.afiliado_id.property_account_receivable_id.id,
                'account_id': self.journal_id.default_debit_account_id.id,
                'partner_id': self.afiliado_id.id,
                'date': self.fecha_desembolso,
            }

            vals_credit = {
                'debit': 0.0,
                'credit': self.monto_solicitado - self.gastos_papeleria,
                'amount_currency': 0.0,
                'name': 'Captacion de ahorro -socio',
                'account_id': self.tipo_ahorro_id.cuenta_cartera.id,
                'partner_id': self.afiliado_id.id,
                'date': self.fecha_desembolso,
            }
            #otra cuenta seguro desgravamen WRLS
            vals_credit1 = {
                'debit': 0.0,
                'credit': self.gastos_papeleria,
                'amount_currency': 0.0,
                'name': 'Seguro Desgravamen ahorro',
                'account_id': self.cuenta_desgravamen.id,
                'partner_id': self.afiliado_id.id,
                'date': self.fecha_desembolso,
            }
        if self.tipo_ahorro_id.tipo_producto == 'ap':
            vals_debit = {
                'debit': self.monto_solicitado,
                'credit': 0.0,
                'amount_currency': 0.0,
                'name': 'Desmbolso de prestamo - al Socio',
                # 'account_id': self.afiliado_id.property_account_receivable_id.id,
                'account_id':  self.tipo_ahorro_id.cuenta_cartera.id,
                'partner_id': self.afiliado_id.id,
                'date': self.fecha_desembolso,
            }

            vals_credit = {
                'debit': 0.0,
                'credit': self.monto_solicitado - self.gastos_papeleria,
                'amount_currency': 0.0,
                'name': 'Desmbolso de prestamo',
                'account_id': self.journal_id.default_debit_account_id.id,
                'partner_id': self.afiliado_id.id,
                'date': self.fecha_desembolso,
            }
            #otra cuenta seguro desgravamen WRLS
            vals_credit1 = {
                'debit': 0.0,
                'credit': self.gastos_papeleria,
                'amount_currency': 0.0,
                'name': 'Seguro Desgravamen prestamo',
                'account_id': self.cuenta_desgravamen.id,
                'partner_id': self.afiliado_id.id,
                'date': self.fecha_desembolso,
            }
        #Asiento presuntivo diferido para intereses WRLS
        vals_debit1 = {
            'debit': self.total_interes,
            'credit': 0.0,
            'amount_currency': 0.0,
            'name': 'Cuentas por Cobrar Diferido Intereses',
            'account_id': self.tipo_ahorro_id.cuenta_ingreso.id,
            'partner_id': self.afiliado_id.id,
            'date': self.fecha_desembolso,
        }
        vals_credit2 = {
            'debit': 0.0,
            'credit': self.total_interes,
            'amount_currency': 0.0,
            'name': 'Cuentas por Pagar Diferido Intereses',
            'account_id': self.tipo_ahorro_id.cuenta_diferido.id,
            'partner_id': self.afiliado_id.id,
            'date': self.fecha_desembolso,
        }
        lineas.append((0, 0, vals_debit))
        lineas.append((0, 0, vals_credit))
        lineas.append((0, 0, vals_credit1))
        lineas.append((0, 0, vals_debit1))
        lineas.append((0, 0, vals_credit2))
        
        values = {
            'journal_id': self.journal_id.id,
            'date': self.fecha_desembolso,
            'ref': 'Desembolso de ahorro' + ' ' + self.name,
            'line_ids': lineas,
        }
        id_move = account_move.create(values)
        return id_move.id

    @api.multi
    def action_rechazar(self):
        # print "estado que entra al if      ", self.state
        if self.state in ('progreso','desembolso'):
            # raise Warning(_('El ahorro pasa a estado BORRADOR!!!'))
            # borra siento de desembolso
            # print "ya entre...",self.move_id
            if self.pagos_ids:
                pagos = self.env['saving.captacion'].search([('ahorros_id','=',self.id)])
                # borro los asientos contables
                for record in pagos:
                    contable = self.env['account.move'].search([('id','=',record.asiento_id.id)])
                    # print "identificador asiento pago  ",record.asiento_id.id
                    if record.asiento_id.id:
                        contable.unlink() # borra el asiento
                    record.unlink() # borra registro detalle pago
            if self.move_id:
                contable = self.env['account.move'].search([('id','=',self.move_id.id)])
                for delete in contable:
                   delete.unlink()
            # borra pagos registrados
            # borrar tabla de amortizacion
            obj_saving_cuota = self.env["saving.management.saving.cuota"]
            obj_saving_cuota_unlink = obj_saving_cuota.search([('ahorros_id', '=', self.id)])
            if self.cuota_ids:
                for delete in obj_saving_cuota_unlink:
                    delete.unlink()
        self.write({'state': 'rechazado'})

    @api.multi
    def action_borrador(self):
        self.write({'state': 'cotizacion'})

    @api.multi
    def action_desembolso(self):
        self.write({'state': 'desembolso'})

    @api.multi
    def generar_contabilidad(self):
        if self.total_desembolso <= 0:
            raise Warning(_('El monto de desembolso debe de ser mayor que cero'))
        if not self.journal_id.default_debit_account_id:
            raise Warning(_('No existe cuenta asociada al banco, revise las parametrizaciones contables del diario'))
        self.write({'move_id': self.generar_partida_contable()})
        self.write({'state': 'progreso'})
        """DCLS"""
        if not self.referencia_desembolso:
            self.write({'referencia_desembolso': str(self.move_id.id)})

    @api.multi
    def action_aprobar(self):
        obj_saving_cuota = self.env["saving.management.saving.cuota"].search([('ahorros_id', '=', self.id)])
        for cuota in obj_saving_cuota:
            if self.tipo_ahorro_id.tipo_producto == 'pf':
                cuota.state = 'vigente'
            if self.tipo_ahorro_id.tipo_producto == 'av':
                cuota.state = cuota.state
            else:
                cuota.state = 'novigente'
        self.write({'state': 'aprobado'})
        self.total_desembolso = self.monto_solicitado #- self.gastos_papeleria - self.gasto_timbre
        self.fecha_aprobacion = datetime.now()

    @api.multi
    def action_solicitar_aprobacion(self):
        if self.monto_solicitado <= 0:
            raise Warning(_('El monto solicitado debe de ser mayor que cero'))
        self.write({'state': 'progress'})

    @api.one
    def get_calculadora_emi(self):
        self.total_interes = 0.0
        for fee in self.cuota_ids:
            self.total_interes += fee.interes

        self.total_monto = self.monto_solicitado + self.total_interes

    def fct_cuotanivelada_pf(self):
        obj_saving_cuota = self.env["saving.management.saving.cuota"]
        obj_saving_cuota_unlink = obj_saving_cuota.search([('ahorros_id', '=', self.id)])
        self.periodo_plazo_pago = 'anios'
        if self.cuota_ids:
            for delete in obj_saving_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        rate_monthly = 0.0
        annuity_factor = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_ahorro_id.tasa_interes_id.capitalizable == 'anual':
            rate_monthly = (self.tasa_interes) / 100.0
            annuity_factor = (rate_monthly * ((1 + rate_monthly) ** self.plazo_pago)) / (((1 + rate_monthly) ** self.plazo_pago) - 1)
            self.cuota_ahorro = self.monto_solicitado * annuity_factor
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'ahorros_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuota_ahorro,
            'saldo_pendiente': self.cuota_ahorro,
            'state': 'cotizacion',
            'mora': 0.0,
        }
        if not self.fecha_pago:
            cuota_fecha = (datetime.strptime(self.fecha_solicitud, '%Y-%m-%d'))
            cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=12)
        else:
            cuota_fecha = (datetime.strptime(self.fecha_pago, '%Y-%m-%d'))
            cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=12)
        while plazo <= self.plazo_pago:
            #if cuota_fecha.day <= 15:
                # values["fecha_pago"] = cuota_fecha + relativedelta(day=30, months=plazo)
            # else:
                # values["fecha_pago"] = cuota_fecha + relativedelta(day=15, months=plazo)

            if plazo == 1:
                interest = self.monto_solicitado * rate_monthly
                capital = self.cuota_ahorro - interest
                values["interes"] = interest
                values["capital"] = capital
                saldo_acumulado = self.monto_solicitado + interest
                values["saldo_ahorro"] = saldo_acumulado
                values["fecha_pago"] = cuota_fecha
            if plazo > 1:
                interest = saldo_acumulado * rate_monthly
                capital = self.cuota_ahorro - interest
                values["interes"] = interest
                values["capital"] = capital
                saldo_acumulado = saldo_acumulado + interest
                values["saldo_ahorro"] = saldo_acumulado
                cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=12)
                values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            id_cuota = obj_saving_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()
    # ahorro programado: tabla propuesta en funcion del monto que se desee alcanzr en un timpo
    def fct_cuotanivelada_ap(self):
        obj_saving_cuota = self.env["saving.management.saving.cuota"]
        obj_saving_cuota_unlink = obj_saving_cuota.search([('ahorros_id', '=', self.id)])
        if self.cuota_ids:
            for delete in obj_saving_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        rate_monthly = 0.0
        annuity_factor = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_ahorro_id.tasa_interes_id.capitalizable == 'anual':
            rate_monthly = (self.tasa_interes / 12.0) / 100.0
            # value_present =  self.monto_solicitado / ((1 + rate_monthly) ** self.plazo_pago))
            # annuity_factor = (rate_monthly * ((1 + rate_monthly) ** self.plazo_pago)) / (((1 + rate_monthly) ** self.plazo_pago) - 1)
            annuity_factor = rate_monthly / (((1 + rate_monthly) ** self.plazo_pago) - 1)
            self.cuota_ahorro = self.monto_solicitado * annuity_factor
            interest = self.monto_solicitado * rate_monthly
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'ahorros_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuota_ahorro,
            'saldo_pendiente': self.cuota_ahorro,
            'state': 'cotizacion',
            'mora': 0.0,
        }
        if not self.fecha_pago:
            cuota_fecha = (datetime.strptime(self.fecha_solicitud, '%Y-%m-%d'))
        else:
            cuota_fecha = (datetime.strptime(self.fecha_pago, '%Y-%m-%d'))
        while plazo <= self.plazo_pago:
            #if cuota_fecha.day <= 15:
                # values["fecha_pago"] = cuota_fecha + relativedelta(day=30, months=plazo)
            # else:
                # values["fecha_pago"] = cuota_fecha + relativedelta(day=15, months=plazo)

            if plazo == 1:
                interest = self.monto_solicitado * rate_monthly
                capital = self.cuota_ahorro
                values["interes"] = 0 # interest
                values["capital"] = capital
                # saldo_acumulado = self.monto_solicitado - capital
                saldo_acumulado = self.cuota_ahorro
                values["saldo_ahorro"] = saldo_acumulado
                values["fecha_pago"] = cuota_fecha
                values["monto_cuota"] = self.monto_solicitado / self.plazo_pago
                values["saldo_pendiente"] = self.monto_solicitado / self.plazo_pago
            if plazo > 1:
                interest = saldo_acumulado * rate_monthly
                capital = self.cuota_ahorro
                values["interes"] = interest
                values["capital"] = capital
                values["monto_cuota"] = self.monto_solicitado / self.plazo_pago
                values["saldo_pendiente"] = self.monto_solicitado / self.plazo_pago
                # saldo_acumulado = saldo_acumulado - capital
                saldo_acumulado = saldo_acumulado + self.cuota_ahorro + interest
                values["saldo_ahorro"] = saldo_acumulado
                cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=1)
                values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            id_cuota = obj_saving_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()

    def fct_cuotaplana(self):
        # se aplica interes a meses por hoy
        # se toma todos los depositos/retiros u capitalia que hay siempre que
        # no se hayan contabilizado o capitalizado
        # calcula la tabla dependiendo de las fechas mensuales
        # obj_saving_cuota = self.env["saving.management.saving.cuota"]
        # obj_saving_cuota_unlink = obj_saving_cuota.search([('ahorros_id', '=', self.id)])
        # if self.cuota_ids:
        #     for delete in obj_saving_cuota_unlink:
        #         delete.unlink()
        if self.cierre:
            raise Warning(_('Ahorro cerrado; no precede calculo alguno'))
        fecha1 = datetime.strptime(self.fecha_pago, '%Y-%m-%d')
        fecha3 = fecha1.replace(day=1) + relativedelta(months=1) + timedelta(days=-1)
        #self.fecha_pago = fecha3
        print('fecha 3  {}'.format(fecha3))
        cuota_fecha = datetime.now()
        saldo_acumulado = 0.0
        suma_saldo = 0.0
        capital = 0.0
        nrocuota = 1
        tasa = 0.0
        acum_interes = 0.0
        self.interes_insoluto = self.interes
        values = {
            'ahorros_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            #'monto_cuota': self.cuota_ahorro,
            #'saldo_pendiente': self.cuota_ahorro,
            #'state': 'cotizacion',
        }
        for line in self.cuota_ids:
            # calcula el interes sea ahorro o retiro relativedelta(day=fecha3.day, months=1)

            fecha2 = datetime.strptime(line.fecha_pago, '%Y-%m-%d')
            dias = abs(fecha2 - fecha3).days
            interest = 0.0
            # cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day,months=12)
            #self.plazo_pago = dias
            #cuota_fecha = line.fecha_pago
            if fecha2 <= fecha3:
                if self.tipo_ahorro_id.tasa_interes_id.capitalizable == 'anual':
                    #saldo_acumulado = (line.monto_cuota * (1 + (self.tasa_interes / 100.0))) / self.plazo_pago
                    tasa = self.tasa_interes / 100.00
                    if line.registro_tipo == 'deposito' :
                        saldo_acumulado = line.deposito
                        interest = (line.deposito * tasa * (dias/360.00))
                    if line.registro_tipo == 'retiro':
                        saldo_acumulado = line.retiro
                        interest = (line.retiro * tasa * (dias/360.00))
                    #capital = line.monto_cuota / self.plazo_pago
                else:
                    raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))
                # actualiza linea de deposito o retiro
                # print("****tasa  {}  propor inte {} dias {}".format(interest,(dias/360.00),dias))
                if  nrocuota == 1:
                    if line.registro_tipo == 'deposito':
                        values["interes"] = interest
                        values["c_liquidacion"] = True
                        saldo_acumulado = saldo_acumulado + interest
                        acum_interes += interest
                    if line.registro_tipo == 'retiro':
                        values["interes_contra"] = interest
                        values["c_liquidacion"] = True
                        saldo_acumulado = -(saldo_acumulado + interest)
                        acum_interes += -interest
                    #values["capital"] = capital

                    values["saldo_ahorro"] = saldo_acumulado
                    suma_saldo += saldo_acumulado
                    values["saldo_acumulado"] = suma_saldo
                    #values["fecha_pago"] = cuota_fecha
                if  nrocuota > 1:
                    if line.registro_tipo == 'deposito':
                        saldo_acumulado = saldo_acumulado + interest
                        acum_interes += interest
                        values["interes"] = interest
                        values["interes_contra"] = 0.0
                        values["c_liquidacion"] = True
                    if line.registro_tipo == 'retiro':
                        values["interes_contra"] = interest
                        saldo_acumulado = -(saldo_acumulado + interest)
                        acum_interes += -interest
                        values["interes"] = 0.0
                        values["c_liquidacion"] = True
                    #values["capital"] = capital
                    # saldo_acumulado = saldo_acumulado + interest
                    values["saldo_ahorro"] = saldo_acumulado
                    suma_saldo += saldo_acumulado
                    values["saldo_acumulado"] = suma_saldo
                    #cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=1)
                    #values["fecha_pago"] = cuota_fecha
                values["numero_cuota"] = nrocuota
                #print("values ********** {} ".format(suma_saldo))
                id_cuota = line.write(values)
                nrocuota +=  1
        # genera entrada sobre saldo pra siguiente capitaliacion,
        # check cierre entonces no
        # depende de self.periodo_plazo_pago 1,3,6,12
        if self.periodo_plazo_pago == 'meses':
            meses = 1
        elif self.periodo_plazo_pago == 'anios':
            meses = 12
        self.fecha_pago = fecha3 + relativedelta(day=fecha3.day, months=meses)
        # fecha siguiente aplicar capitalizacion
        self.fecha_capitaliza = fecha3
        print("interes_acumulado en capitalizacion ********** {} ".format(acum_interes))
        # valores acomodados al perfil
        self.interes = acum_interes
        self.saldo_libreta = suma_saldo
        self.monto_solicitado = suma_saldo
        self.write({'state': 'progreso'})

        self.get_calculadora_emi()

    def fct_cuotaalemana(self):
        obj_saving_cuota = self.env["saving.management.saving.cuota"]
        obj_saving_cuota_unlink = obj_saving_cuota.search([('ahorros_id', '=', self.id)])
        if self.cuota_ids:
            for delete in obj_saving_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_ahorro_id.tasa_interes_id.capitalizable == 'anual':
            cuota_capital = self.monto_solicitado/self.plazo_pago
            self.cuota_ahorro = (cuota_capital * (1 + (self.tasa_interes / 100.0)))
            interest = (cuota_capital * (self.tasa_interes / 100))
            capital = cuota_capital
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'ahorro_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuota_ahorro,
            'saldo_pendiente': self.cuota_ahorro,
            'mora': 0.0,
            #'capital':capital,
            #'interes':interes,
            'state': 'cotizacion',
        }
        if not self.fecha_pago:
            cuota_fecha = (datetime.strptime(self.fecha_solicitud, '%Y-%m-%d'))
        else:
            cuota_fecha = (datetime.strptime(self.fecha_pago, '%Y-%m-%d'))
        while plazo <= self.plazo_pago:
            saldo_acumulado = self.monto_solicitado - ((plazo-1) * capital)
            interest = capital * (self.tasa_interes / 100)
            cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=1)
            if plazo == 1:
                values["interes"] = interest
            else:
                values["interes"] = ((saldo_acumulado)*(self.tasa_interes / 100))/self.plazo_pago
            values["saldo_ahorro"] = saldo_acumulado-capital
            values["capital"] = capital
            values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            values["monto_cuota"] = capital + values["interes"] 
            values["saldo_pendiente"] = capital + values["interes"] 

            id_cuota = obj_saving_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()
        
    def fct_cuotafrancesa(self):
        obj_saving_cuota = self.env["saving.management.saving.cuota"]
        obj_saving_cuota_unlink = obj_saving_cuota.search([('ahorros_id', '=', self.id)])
        if self.cuota_ids:
            for delete in obj_saving_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_ahorro_id.tasa_interes_id.capitalizable == 'anual':
            cuota_capital = self.monto_solicitado/self.plazo_pago
            self.cuota_ahorro = (cuota_capital * (1 + (self.tasa_interes / 100.0)))
            interest = (cuota_capital * (self.tasa_interes / 100))
            capital = cuota_capital
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'ahorro_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuota_ahorro,
            'saldo_pendiente': self.cuota_ahorro,
            'mora': 0.0,
            #'capital':capital,
            #'interes':interes,
            'state': 'cotizacion',
        }
        if not self.fecha_pago:
            cuota_fecha = (datetime.strptime(self.fecha_solicitud, '%Y-%m-%d'))
        else:
            cuota_fecha = (datetime.strptime(self.fecha_pago, '%Y-%m-%d'))
        while plazo <= self.plazo_pago:
            saldo_acumulado = self.monto_solicitado - ((plazo-1) * capital)
            interest = capital * (self.tasa_interes / 100)
            cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=1)
            if plazo == 1:
                values["interes"] = interest
            else:
                values["interes"] = ((saldo_acumulado)*(self.tasa_interes / 100))/self.plazo_pago
            values["saldo_ahorro"] = saldo_acumulado-capital
            values["capital"] = capital
            values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            values["monto_cuota"] = capital + values["interes"] 
            values["saldo_pendiente"] = capital + values["interes"] 

            id_cuota = obj_saving_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()

    @api.one
    def get_generar_cuotas(self):
        if self.plazo_pago <= 0:
            raise Warning(_('Los plazos de pago deben ser mayor que 1'))
        elif self.tipo_ahorro_id.metodo_calculo == 'cuotanivelada':
            if self.tipo_ahorro_id.tipo_producto == 'av':
                self.fct_cuotaplana()
            elif self.tipo_ahorro_id.tipo_producto == 'pf':
                self.fct_cuotanivelada_pf()
            elif self.tipo_ahorro_id.tipo_producto == 'ap':
                self.fct_cuotanivelada_ap()
            #self.fct_cuotanivelada()
        elif self.tipo_ahorro_id.metodo_calculo == 'plana':
            self.fct_cuotaplana()
        elif self.tipo_ahorro_id.metodo_calculo == 'alemana':
            self.fct_cuotaalemana()
        elif self.tipo_ahorro_id.metodo_calculo == 'francesa':
            self.fct_cuotafrancesa()

    @api.model
    def _calcular_cuota(self, valor_ahorro, interes, plazo_tiempo):
        cuota = (valor_ahorro * (1 + interes / 100.0)) / plazo_tiempo
        return cuota

    @api.model
    def _calcular_capital_cuota(self, valor_ahorro, plazo_tiempo):
        capital = valor_ahorro / plazo_tiempo
        return capital

    @api.model
    def _calcular_interes_cuota(self, valor_ahorro, interes, plazo_tiempo):
        interes = (valor_ahorro * interes / 100.0) / plazo_tiempo
        return interes


class Savingline(models.Model):
    _name = "saving.management.saving.cuota"
    _rec_name = 'numero_cuota'
    _order = 'fecha_pago asc'


    ahorros_id = fields.Many2one("saving.management.saving", "Numero de ahorro", readonly=True, ondelete="cascade")
    forma_producto = fields.Selection("Forma Ahorro", related='ahorros_id.forma_producto', store=True)
    currency_id = fields.Many2one("res.currency", "Moneda", domain=[('active', '=', True)], related="ahorros_id.currency_id")
    afiliado_id = fields.Many2one("res.partner", "Cliente", required=True)
    # bic_id = fields.Many2one("res.bank","Codigo Banco")
    cuenta_banco = fields.Char("Cuenta banco Socio", compute = '_get_cuenta_banco', store=True)
    fecha_pago = fields.Date("Fecha",default=fields.Date.today, required=True)
    monto_cuota = fields.Monetary("Renta o Anualidad")
    capital = fields.Monetary("Capital")
    interes = fields.Monetary("Interes")
    mora = fields.Monetary("Impuesto")
    saldo_ahorro = fields.Monetary("Cuota Neta")
    saldo_acumulado = fields.Monetary("Saldo Acumulado")
    state = fields.Selection(
        [('cotizacion', 'Cotizacion'), ('cancelada', 'Cancelada'), ('novigente', 'No vigente'), ('vigente', 'Vigente'),('deposito', 'Deposito'),('retiro', 'Retiro'),
        ('capitaliza', 'Capitalizacion'),('morosa', 'Morosa'),('pagada', 'Pagada')], string='Estado de cuota', default='cotizacion')
    description = fields.Text("Notas Generales")
    numero_cuota = fields.Integer("# Cuota", readonly=True)
    saldo_pendiente = fields.Monetary("Saldo Renta")
    monto_pagado = fields.Monetary("Monto Pagado")
    numero_deposito = fields.Char("NroDeposito", default='000000', help ="Cadena caracteres,referencia al deposito")
    registro_tipo = fields.Selection(
        [('deposito', 'Deposito'), ('retiro', 'Retiro'),('capitaliza', 'Capitalizacion')], string='Registro Tipo: ', default='deposito')
    deposito = fields.Monetary("Depositos")
    interes_contra = fields.Monetary("Interes contra")
    retiro = fields.Monetary("Retiros")
    c_liquidacion = fields.Boolean("Capitalizado", default=False)
    contabilizado = fields.Boolean("Contabilizado", default=False)

    @api.model
    def create(self, vals):
        registro_tipo = vals.get("registro_tipo")
        estado = "cotizacion"
        if registro_tipo == 'retiro':
            estado = "retiro"
        if registro_tipo == 'capitaliza':
            estado = "capitaliza"
        if registro_tipo == 'deposito':
            estado = "deposito"
        vals["state"] = estado
        print('en create cuota ===========> {}'.format(self.ahorros_id.saldo_libreta))
        return super(Savingline, self).create(vals)

    @api.onchange("fecha_pago")
    def fecha_pago_depends(self):
        if self.fecha_pago <= self.ahorros_id.fecha_capitaliza:
            raise Warning(_('La fecha debe ser mayor que {}'.format(self.ahorros_id.fecha_capitaliza)))
    @api.onchange("retiro")
    def retiro_onchange(self):
        if self.retiro > self.saldo_acumulado and self.saldo_acumulado > 0:
             raise Warning(_('No puede retirar esa cantidad, saldo fondos {}'.format( self.saldo_acumulado)))
    @api.depends("afiliado_id")
    @api.onchange("afiliado_id")
    def socio_onchange(self):
        self.afiliado_id = self.ahorros_id.afiliado_id.id
        self.saldo_acumulado = self.ahorros_id.saldo_libreta
        if self.ahorros_id.fecha_capitaliza:
            fecha4 = datetime.strptime(self.ahorros_id.fecha_capitaliza, '%Y-%m-%d')
            self.fecha_pago = fecha4 + timedelta(days=1) # suma 1 dia
            fecha3 = fecha4.replace(day=1) + relativedelta(months=1) + timedelta(days=-1)
            self.ahorros_id.fecha_pago = fecha3

    #@api.one
    def _get_cuenta_banco(self):
        obj_cuenta_banco =self.env['res.partner.bank'].search([('partner_id', '=', self.afiliado_id.id)])
        for cban in obj_cuenta_banco:
        #self.cuenta_banco = obj_cuenta_banco.bank_id.bic
            self.cuenta_banco = cban.bank_id.bic
        # print("cuenta ban: ",self.cuenta_banco)