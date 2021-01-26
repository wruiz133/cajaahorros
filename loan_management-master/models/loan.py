# -*- encoding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import openerp.addons.decimal_precision as dp


class Loan_cargos(models.Model):
    _name = "loan.cargos"
    _inherit = ['mail.thread']

    name = fields.Selection([('cargos','Otros Cargos'),
                             ('legalizacion','Legalizacion'),
                             ('constante_local','Contante Local'),
                             ('seguro','Seguro'),
                             ('imp_solca','Impuesto SOLCA'),
                             ('imp_infa','Impuesto INFA'),
                             ('retencion_ahorros','Retencion Ahorros'),
                             ('retencion_aportes','Retencion Aportes'),
                             ('encaje_ahorros','Encaje ahorros'),
                             ('encaje_aportacion','Encaje cetificados de aportacion'),
                             ('total_fondos_propios','Total fondos propios'),
                             ], string = "Cargos" , required=True)
    cargos_id = fields.Many2one("loan.management.loan", "Loan")
    amount = fields.Float("Monto")

    
    
class Loan(models.Model):
    _name = "loan.management.loan"
    _order = 'fecha_solicitud asc'
    _inherit = ['mail.thread']

    def get_currency(self):
        return self.env.user.company_id.currency_id.id

    # @api.depends('cuota_ids')
    @api.one
    def get_saldo(self):
        for prestamo in self:
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
                    # WHRC aplica para liquidar prestamos en cualquier momento
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

            self.interes = interes
	        # campos clculados adicionales que dan mas informacion  WR
            self.monto_recaudado = saldo
            self.monto_insoluto = insoluto
            self.interes_insoluto = interes_insoluto
            self.saldo_liquidar = liquidar
            self.saldo_liquidarcap = liquidar
            # WR desgravamen > 0 ssi van desde 2019
            desgrava_fecha = (datetime.strptime(self.fecha_solicitud, '%Y-%m-%d'))
            # print "fecha es: %s",desgrava_fecha.year
            if desgrava_fecha.year >= 2019:
                self.gastos_papeleria = self.monto_solicitado * 0.01
            else:
                self.gastos_papeleria = 0.0
            # print "el valor al calculo desgravamen  ", self.gastos_papeleria
            self.mora_prestamo = mora
            # calculo neto para reporteo comprobate egreso
            self.monto_neto_desembolso = self.monto_solicitado - self.gastos_papeleria
            #verifica que todos las cuotas sean pagadas y liquida prestamo WHRC
            for line in self.cuota_ids:
                #print ("numerocuota despues:  ", line.numero_cuota, "  estado  ",line.state)
                if line.state == 'pagada':
                    done = True
                else:
                    nodone = False
            done = nodone
            #print("el valor done   ", done)
            self.prestamo_done = done
            if self.mora_prestamo > 0.0:
                self.prestamo_moroso = True
            if self.prestamo_done and self.cuota_ids:
                self.write({'state': 'liquidado'})
            # se liquida aun habiendo algun resto en alguna cuota
            if self.state == 'liquidado':
                self.saldo_pendiente = 0.0
            else:
                self.saldo_pendiente = self.total_monto - saldo

    @api.depends('encaje_aportacion','cuota_ids.state','cuota_ids.monto_cuota','cuota_ids.saldo_pendiente','total_monto')
    def get_saldo_p(self):
        recaudado = 0.0
        if self.state == 'liquidado':
            self.saldo_pendiente = 0.0
        else:
            for cuota in self.cuota_ids:
                if cuota.state == 'pagada':
                    recaudado += cuota.monto_cuota
                if cuota.state in ('vigente','morosa') and (cuota.monto_cuota - cuota.saldo_pendiente) > 0: #pp
                    recaudado += cuota.monto_pagado
            self.saldo_pendiente = self.total_monto - recaudado
            self.monto_recaudado = recaudado

    # Valores numericos
    total_interes = fields.Float("Total de interes", states={'cotizacion': [('readonly', False)]})
    total_monto = fields.Float("Importe Total", states={'cotizacion': [('readonly', False)]})
    cuato_prestamo = fields.Float("Cuota de prestamo", states={'cotizacion': [('readonly', False)]})
    monto_solicitado = fields.Float("Monto solicitado", required=True)
    saldo_pendiente = fields.Float("Saldo pendiente", readonly=True, store=True, compute='get_saldo_p')
    saldo_liquidarcap = fields.Float("LiquidarCapital", readonly=True, store=True, compute='get_saldo')
    mora_prestamo = fields.Float("Mora de prestamo", readonly=True, compute='get_saldo')
    # Control saldos whr
    monto_recaudado = fields.Float("Monto Cobrado", readonly=True, store=True, compute='get_saldo_p')
    monto_insoluto = fields.Float("Monto Insoluto", readonly=True, compute='get_saldo')
    saldo_liquidar = fields.Float("Saldo a Liquidar", readonly=True, compute='get_saldo')
    interes = fields.Float("Interes Pendiente", readonly=True, compute='get_saldo')
    interes_insoluto = fields.Float("Interes Insoluto", readonly=True, store=True, compute='get_saldo')
    # Gastos de prestamo
    gastos_papeleria = fields.Monetary("Desgravamen", compute='get_saldo')
    gasto_timbre = fields.Monetary("Mnto Reliquid.")
    monto_comision = fields.Monetary("Comisióm bancaria")
    total_desembolso = fields.Float("Monto a desembolsar")
    fecha_desembolso = fields.Date("Fecha de desembolso")
    referencia_desembolso = fields.Char("No. de Cheque/ Transferencia")
    notas_desembolso = fields.Text("Notas de desombolso")
    # Campos generales

    currency_id = fields.Many2one("res.currency", "Moneda", domain=[('active', '=', True)], default=get_currency)
    name = fields.Char("Numero de prestamo", required=True, default=lambda self: self.env['ir.sequence'].get('prestamo'))
    afiliado_id = fields.Many2one("res.partner", "Cliente", required=True, domain=[('customer', '=', True)], states={'cotizacion': [('readonly', False)]})
    fecha_solicitud = fields.Date("Fecha de solicitud", required=True, default=fields.Date.today, states={'cotizacion': [('readonly', False)]})
    fecha_aprobacion = fields.Date("Fecha de aprobación", states={'cotizacion': [('readonly', False)]})
    fecha_pago = fields.Date("Fecha Inicial(Pagos)", states={'cotizacion': [('readonly', False)]})
    currency_id = fields.Many2one("res.currency", "Moneda", default=lambda self: self.env.user.company_id.currency_id)
    # Parametros
    plazo_pago = fields.Integer("Plazo de pago", required=True, states={'cotizacion': [('readonly', False)]})
    periodo_plazo_pago = fields.Selection([('dias', 'Días'), ('meses', 'Meses')], string='Periodo', default='meses', required=True)
    tasa_interes = fields.Float("Tasa de interes", required=True)
    notas = fields.Text("Notas")
    state = fields.Selection([('cotizacion', 'Cotizacion'), 
                              ('progress', 'Esperando Aprobacion'), 
                              ('rechazado', 'Rechazado'), 
                              ('aprobado', 'Aprobado'),
                              ('desembolso', 'En desembolso'), 
                              ('progreso', 'En progreso'), 
                              ('liquidado', 'Liquidado')
                              ], string='Estado de prestamo',type='selection', default='cotizacion')
    tipo_prestamo_id = fields.Many2one("loan.management.loan.type", "Tipo de Prestamo", required=True, states={'cotizacion': [('readonly', False)]})
    cuota_ids = fields.One2many("loan.management.loan.cuota", "prestamo_id", "Cuotas de prestamo")
    doc_ids = fields.One2many("loan.management.tipo.documento", "prestamo_id", "Documentos de validacion")
    move_id = fields.Many2one('account.move', 'Asiento Contable', ondelete='restrict', readonly=True)
    #move_id = fields.Many2one('account.move', 'Asiento Contable', readonly=True, ondelete="cascade")
    journal_id = fields.Many2one("account.journal", "Banco", domain=[('type', '=', 'bank')])
	#WRLS
    monto_neto_desembolso = fields.Float("Desembolso Neto", compute='get_saldo',store=True)
    cuenta_desgravamen =  fields.Many2one('account.account', 'Cuenta de Desgravamen')
    seq_desembolso = fields.Char("Número Desembolso", default=lambda self: self.env['ir.sequence'].get('desembolso'), states={'draft': [('readonly', False)]})

    # Información de pagos
    pagos_ids = fields.One2many("loan.pagos", "prestamo_id", "Pagos de Cuotas")
    mora_id = fields.Many2one("loan.management.loan.mora", "Tasa Moratoria")
    prestamo_moroso = fields.Boolean("Prestamo en mora", compute='get_saldo')
    prestamo_done = fields.Boolean("Prestamo liquidado", compute='get_saldo')

    #HTC datos
    cargos_ids = fields.One2many("loan.cargos", "cargos_id", "Cargos Credito")

    
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
    
    encaje_aportacion = fields.Float("Encaje cetificados de aportacion")
    encaje_ahorros = fields.Float("Encaje ahorros")
    total_fondos_propios = fields.Float("Total fondos propios")
    
    
    grupo = fields.Selection([('cotizacion', 'Cotizacion'), 
                              ('progress', 'Esperando Aprobacion'), 
                              ], string='Estado de prestamo',  readonly=True, default='cotizacion')

    
    
    @api.onchange("tipo_prestamo_id")
    def _get_tasa_plazo(self):
        self.plazo_pago = self.tipo_prestamo_id.plazo_pago_id.numero_plazo
        self.tasa_interes = self.tipo_prestamo_id.tasa_interes_id.tasa_interes
        #self.periodo_plazo_pago = self.tipo_prestamo_id.tasa_interes_id.capitalizable

    # Generar partida de desembolso
    def generar_partida_contable(self):
        account_move = self.env['account.move']
        lineas = []
        vals_debit = {
            'debit': self.monto_solicitado,
            'credit': 0.0,
            'amount_currency': 0.0,
            'name': 'Desmbolso de prestamo - al Socio',
            # 'account_id': self.afiliado_id.property_account_receivable_id.id,
            'account_id': self.tipo_prestamo_id.cuenta_cartera.id,
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
            'account_id': self.tipo_prestamo_id.cuenta_ingreso.id,
            'partner_id': self.afiliado_id.id,
            'date': self.fecha_desembolso,
        }
        vals_credit2 = {
            'debit': 0.0,
            'credit': self.total_interes,
            'amount_currency': 0.0,
            'name': 'Cuentas por Pagar Diferido Intereses',
            'account_id': self.tipo_prestamo_id.cuenta_diferido.id,
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
            'ref': 'Desembolso de prestamo' + ' ' + self.name,
            'line_ids': lineas,
        }
        id_move = account_move.create(values)
        return id_move.id

    @api.multi
    def action_rechazar(self):
        # print "estado que entra al if      ", self.state
        if self.state in ('progreso','desembolso'):
            # raise Warning(_('El Prestamo pasa a estado BORRADOR!!!'))
            # borra siento de desembolso
            # print "ya entre...",self.move_id
            if self.pagos_ids:
                pagos = self.env['loan.pagos'].search([('prestamo_id','=',self.id)])
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
            obj_loan_cuota = self.env["loan.management.loan.cuota"]
            obj_loan_cuota_unlink = obj_loan_cuota.search([('prestamo_id', '=', self.id)])
            if self.cuota_ids:
                for delete in obj_loan_cuota_unlink:
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
        obj_loan_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.id)])
        for cuota in obj_loan_cuota:
            cuota.state = 'novigente'
        self.write({'state': 'aprobado'})
        #self.saldo_pendiente = self.total_monto
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

    def fct_cuotanivelada(self):
        obj_loan_cuota = self.env["loan.management.loan.cuota"]
        obj_loan_cuota_unlink = obj_loan_cuota.search([('prestamo_id', '=', self.id)])
        if self.cuota_ids:
            for delete in obj_loan_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        rate_monthly = 0.0
        annuity_factor = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_prestamo_id.tasa_interes_id.capitalizable == 'anual':
            rate_monthly = (self.tasa_interes / 12.0) / 100.0
            annuity_factor = (rate_monthly * ((1 + rate_monthly) ** self.plazo_pago)) / (((1 + rate_monthly) ** self.plazo_pago) - 1)
            self.cuato_prestamo = self.monto_solicitado * annuity_factor
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'prestamo_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuato_prestamo,
            'saldo_pendiente': self.cuato_prestamo,
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
                capital = self.cuato_prestamo - interest
                values["interes"] = interest
                values["capital"] = capital
                saldo_acumulado = self.monto_solicitado - capital
                values["saldo_prestamo"] = saldo_acumulado
                values["fecha_pago"] = cuota_fecha
            if plazo > 1:
                interest = saldo_acumulado * rate_monthly
                capital = self.cuato_prestamo - interest
                values["interes"] = interest
                values["capital"] = capital
                saldo_acumulado = saldo_acumulado - capital
                values["saldo_prestamo"] = saldo_acumulado
                cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=1)
                values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            id_cuota = obj_loan_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()


    def fct_cuotaplana(self):
        obj_loan_cuota = self.env["loan.management.loan.cuota"]
        obj_loan_cuota_unlink = obj_loan_cuota.search([('prestamo_id', '=', self.id)])
        if self.cuota_ids:
            for delete in obj_loan_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_prestamo_id.tasa_interes_id.capitalizable == 'anual':
            self.cuato_prestamo = (self.monto_solicitado * (1 + (self.tasa_interes / 100.0))) / self.plazo_pago
            interest = (self.monto_solicitado * (self.tasa_interes / 100)) / self.plazo_pago
            capital = self.monto_solicitado / self.plazo_pago
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'prestamo_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuato_prestamo,
            'saldo_pendiente': self.cuato_prestamo,
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
            if plazo == 1:
                values["interes"] = interest
                values["capital"] = capital
                saldo_acumulado = self.monto_solicitado - capital
                values["saldo_prestamo"] = saldo_acumulado
                values["fecha_pago"] = cuota_fecha
            if plazo > 1:
                values["interes"] = interest
                values["capital"] = capital
                saldo_acumulado = saldo_acumulado - capital
                values["saldo_prestamo"] = saldo_acumulado
                cuota_fecha = cuota_fecha + relativedelta(day=cuota_fecha.day, months=1)
                values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            id_cuota = obj_loan_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()



    def fct_cuotaalemana(self):
        obj_loan_cuota = self.env["loan.management.loan.cuota"]
        obj_loan_cuota_unlink = obj_loan_cuota.search([('prestamo_id', '=', self.id)])
        if self.cuota_ids:
            for delete in obj_loan_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_prestamo_id.tasa_interes_id.capitalizable == 'anual':
            cuota_capital = self.monto_solicitado/self.plazo_pago
            self.cuato_prestamo = (cuota_capital * (1 + (self.tasa_interes / 100.0)))
            interest = (cuota_capital * (self.tasa_interes / 100))
            capital = cuota_capital
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'prestamo_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuato_prestamo,
            'saldo_pendiente': self.cuato_prestamo,
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
            values["saldo_prestamo"] = saldo_acumulado-capital
            values["capital"] = capital
            values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            values["monto_cuota"] = capital + values["interes"] 
            values["saldo_pendiente"] = capital + values["interes"] 

            id_cuota = obj_loan_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()
        
    def fct_cuotafrancesa(self):
        obj_loan_cuota = self.env["loan.management.loan.cuota"]
        obj_loan_cuota_unlink = obj_loan_cuota.search([('prestamo_id', '=', self.id)])
        if self.cuota_ids:
            for delete in obj_loan_cuota_unlink:
                delete.unlink()
        plazo = 1
        cuota_fecha = datetime.now()
        interest = 0.0
        saldo_acumulado = 0.0
        capital = 0.0
        if self.tipo_prestamo_id.tasa_interes_id.capitalizable == 'anual':
            cuota_capital = self.monto_solicitado/self.plazo_pago
            self.cuato_prestamo = (cuota_capital * (1 + (self.tasa_interes / 100.0)))
            interest = (cuota_capital * (self.tasa_interes / 100))
            capital = cuota_capital
        else:
            raise Warning(_('No se han definido tasas capitalizables mensuales y quincenales'))

        values = {
            'prestamo_id': self.id,
            'afiliado_id': self.afiliado_id.id,
            'monto_cuota': self.cuato_prestamo,
            'saldo_pendiente': self.cuato_prestamo,
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
            values["saldo_prestamo"] = saldo_acumulado-capital
            values["capital"] = capital
            values["fecha_pago"] = cuota_fecha
            values["numero_cuota"] = plazo
            values["monto_cuota"] = capital + values["interes"] 
            values["saldo_pendiente"] = capital + values["interes"] 

            id_cuota = obj_loan_cuota.create(values)
            plazo +=  1
        self.get_calculadora_emi()



    @api.one
    def get_generar_cuotas(self):
        if self.plazo_pago <= 0:
            raise Warning(_('Los plazos de pago deben ser mayor que 1'))
        elif self.tipo_prestamo_id.metodo_calculo == 'cuotanivelada':
            self.fct_cuotanivelada()
        elif self.tipo_prestamo_id.metodo_calculo == 'plana':
            self.fct_cuotaplana()
        elif self.tipo_prestamo_id.metodo_calculo == 'alemana':
            self.fct_cuotaalemana()
        elif self.tipo_prestamo_id.metodo_calculo == 'francesa':
            self.fct_cuotafrancesa()

    @api.model
    def _calcular_cuota(self, valor_prestamo, interes, plazo_tiempo):
        cuota = (valor_prestamo * (1 + interes / 100.0)) / plazo_tiempo
        return cuota

    @api.model
    def _calcular_capital_cuota(self, valor_prestamo, plazo_tiempo):
        capital = valor_prestamo / plazo_tiempo
        return capital

    @api.model
    def _calcular_interes_cuota(self, valor_prestamo, interes, plazo_tiempo):
        interes = (valor_prestamo * interes / 100.0) / plazo_tiempo
        return interes


class Loanline(models.Model):
    _name = "loan.management.loan.cuota"
    _rec_name = 'numero_cuota'


    prestamo_id = fields.Many2one("loan.management.loan", "Numero de prestamo", readonly=True, ondelete="cascade")
    currency_id = fields.Many2one("res.currency", "Moneda", domain=[('active', '=', True)], related="prestamo_id.currency_id")
    afiliado_id = fields.Many2one("res.partner", "Cliente", required=True)
    # bic_id = fields.Many2one("res.bank","Codigo Banco")
    cuenta_banco = fields.Char("Cuenta banco Socio", compute = '_get_cuenta_banco', store=True)
    fecha_pago = fields.Date("Fecha de Pago")
    monto_cuota = fields.Monetary("Monto de Cuota")
    capital = fields.Monetary("Capital")
    interes = fields.Monetary("Interes")
    mora = fields.Monetary("Mora")
    saldo_prestamo = fields.Monetary("Saldo Pendiente")
    state = fields.Selection(
        [('cotizacion', 'Cotizacion'), ('cancelada', 'Cancelada'), ('novigente', 'No vigente'), ('vigente', 'Vigente'),
        ('morosa', 'Morosa'),('pagada', 'Pagada')], string='Estado de cuota', default='cotizacion')
    description = fields.Text("Notas Generales")
    numero_cuota = fields.Integer("# de cuota", readonly=True)
    saldo_pendiente = fields.Monetary("Saldo de Cuota")
    monto_pagado = fields.Monetary("Monto Pagado")
    numero_deposito = fields.Char("NroDeposito", default='000000', help ="Cadena caracteres,referencia al deposito")

    @api.depends("afiliado_id")
    #@api.onchange("afiliado_id")
    #@api.one
    def _get_cuenta_banco(self):
        obj_cuenta_banco =self.env['res.partner.bank'].search([('partner_id', '=', self.afiliado_id.id)])
        for cban in obj_cuenta_banco:
        #self.cuenta_banco = obj_cuenta_banco.bank_id.bic
            self.cuenta_banco = cban.bank_id.bic
        # print("cuenta ban: ",self.cuenta_banco)