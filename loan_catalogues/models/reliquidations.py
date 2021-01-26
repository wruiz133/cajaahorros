# -*- encoding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import Warning
#from num2words import num2words


class WizardPagoCuotas(models.TransientModel):
    _inherit = 'loan.wizard.payment'

    @api.one
    def generarsaldos(self):
        #pinta el detalle de las cuotas que se liquidaran desde boton revisar saldo
        #si existe prestamo y tiene cuotas lo limplia para volver a cargar
        if self.prestamo_id:
            if self.cuotas_ids:
                for fee in self.cuotas_ids:
                    fee.unlink()
            obj_cuota_payment = self.env["loan.wizard.payment.lines"]
            contexto = self._context
            if 'active_id' in contexto:
                loan_obj = self.env["loan.management.loan"].browse(contexto['active_id'])
                if loan_obj.gasto_timbre == 0:
                    loan_obj.end_reliquidation = True
                else:
                    loan_obj.end_reliquidation = False
            for cuota in self.prestamo_id.cuota_ids:
                #amplia a reliquidacion o desgravamen, eso presenta todas las cuotas no pagadas a liquidar
                if cuota.state == 'vigente' or cuota.state == 'morosa':
                    vals = {
                        'numero_cuota': cuota.numero_cuota,
                        'pago_cuota_id': self.id,
                        'fecha_pago': cuota.fecha_pago,
                        'capital':cuota.capital,
                        'monto_cuota': cuota.monto_cuota,
                        'mora': cuota.mora,
                        'saldo_pendiente': cuota.saldo_pendiente,
                        'state': cuota.state,
                    }
                    id_cuota = obj_cuota_payment.create(vals)
                    #and loan_obj.end_reliquidation
                # print "carga de prestamos........"
                # print "reliquidacion ", loan_obj.is_reliquidation
                # print "end reliquidacion ", loan_obj.end_reliquidation
                if  (loan_obj.is_reliquidation and loan_obj.end_reliquidation)  or self.es_desgravamen:
                    if cuota.state == 'novigente':
                        vals = {
                            'numero_cuota': cuota.numero_cuota,
                            'pago_cuota_id': self.id,
                            'fecha_pago': cuota.fecha_pago,
                            'capital':cuota.capital,
                            'monto_cuota': cuota.monto_cuota,
                            'mora': cuota.mora,
                            'saldo_pendiente': cuota.saldo_pendiente,
                            'state': cuota.state,
                        }
                        id_cuota = obj_cuota_payment.create(vals)
            self.write({'state': 'saldo'})
            self.has_revision_saldo = True
            self.monto = self.saldo_pago

    def _get_values(self):
        # print "en get_values.."
        contexto = self._context
        if 'active_id' in contexto:
            loan_obj = self.env["loan.management.loan"].browse(contexto['active_id'])
            if loan_obj.gasto_timbre == 0 or self.es_desgravamen:
                loan_obj.end_reliquidation = True
            else:
                loan_obj.end_reliquidation = False
        if self.cuotas_ids:
            for fee in self.cuotas_ids:
                if fee.state == 'vigente':
                    self.monto_vigente = self.monto_vigente + fee.saldo_pendiente
                    self.numero_cuota = fee.numero_cuota
                if fee.state == 'morosa':
                    self.saldo_mora = self.saldo_mora + fee.saldo_pendiente
                    #self.write({'cuotas_mora_num': [(4, fee.id, None)]})
                if (loan_obj.is_reliquidation and loan_obj.end_reliquidation) or self.es_desgravamen:
                    if fee.state == 'novigente':
                        self.capital = self.capital + fee.capital
            self.saldo_pago = self.monto_vigente + self.saldo_mora + self.capital

    #WHRC-LS se sobre escribe y ssi es reliquidacion, sino contabiliza normal el pago
    def generar_partida_contable(self, capital, interes, mora, monto):
        #refactoriza el codigo para tomar el dato calculado del interes y descontar para el asiento liquidador
        contexto = self._context
        if 'active_id' in contexto:
            loan_obj = self.env["loan.management.loan"].browse(contexto['active_id'])
            #and loan_obj.end_reliquidation
            if loan_obj.gasto_timbre == 0:
                loan_obj.end_reliquidation = True
            else:
                loan_obj.end_reliquidation = False
            if self.monto > 0.0 and loan_obj.is_reliquidation and loan_obj.end_reliquidation:
                #se cambia la posicion de la actualizacion de campos y el valor que llega al asiento
                loan_obj.write({'gasto_timbre': self.monto - interes})
                loan_obj.write({'total_desembolso': loan_obj.monto_solicitado - loan_obj.gasto_timbre})

        account_move = self.env['account.move']
        lineas = []
        monto_pago = round(monto, 2) - round(interes, 2)

        #ssi existe reliquidacion se pone un asiento solo de intereses
        # print "reliquidacion ",loan_obj.is_reliquidation
        # print "end reliquidacion ",loan_obj.end_reliquidation
        if loan_obj.is_reliquidation and loan_obj.end_reliquidation:
        #if loan_obj.is_reliquidation:
            #se contabiliza solo el interes ya que la deuda pasa al desembolso
            #actualiza la bandera para que el reliquidador contabilize cuotas normales
            loan_obj.write({'end_reliquidation': False})
            # print "deeeeesssspues     "
            # print "reliquidacion ",loan_obj.is_reliquidation
            # print "end reliquidacion ",loan_obj.end_reliquidation
            if interes > 0.0:
                # WR-LS  asiento proporcional del interes diferido
                vals_debit1 = {
                    'debit': round(interes, 2),
                    'credit': 0.0,
                    'amount_currency': 0.0,
                    'name': 'Amortizacion Pasivo Diferido',
                    'account_id': self.prestamo_id.tipo_prestamo_id.cuenta_diferido.id,
                    'partner_id': self.prestamo_id.afiliado_id.id,
                    'date': self.date_payment,
                }
                lineas.append((0, 0, vals_debit1))

                vals_credit2 = {
                    'debit': 0.0,
                    'credit': round(interes, 2),
                    'amount_currency': 0.0,
                    'name': 'Pago Cuentas por Cobrar Diferido Intereses',
                    'account_id': self.prestamo_id.tipo_prestamo_id.cuenta_ingreso.id,
                    'partner_id': self.prestamo_id.afiliado_id.id,
                    'date': self.date_payment,
                }
                lineas.append((0, 0, vals_credit2))

            values = {
                'journal_id': self.journal_id.id,
                'date': self.date_payment,
                'ref': 'Pago de prestamo' + ' ' + self.prestamo_id.name,
                'line_ids': lineas,
            }
        else:
            #WHRC-LS se aplica la funcionalidad del padre en caso de no ser reliquidacion
            return super(WizardPagoCuotas, self).generar_partida_contable(capital, interes, mora, monto)
        # pdb.set_trace()
        id_move = account_move.create(values)
        return id_move.id

    # Información General
    capital = fields.Monetary("Capital", compute=_get_values)
    saldo_pago = fields.Monetary("Saldo Pendiente", compute=_get_values)
    saldo_mora = fields.Monetary("Saldo en Mora", compute=_get_values)
    monto_vigente = fields.Monetary("Monto Vigente", compute=_get_values)
    numero_cuota = fields.Integer("Cuota Vigente #", compute=_get_values)

    @api.one
    def set_pagos(self):
        # contexto del prestamo en curso
        contexto = self._context
        if 'active_id' in contexto:
            loan_obj = self.env["loan.management.loan"].browse(contexto['active_id'])
        if self.monto > 0:
            if not self.has_revision_saldo:
                raise Warning(_('Primero genere la revisión de saldos, para poder realizar pagos'))

            saldo_pago = round(self.saldo_pago, 2)
            # Primera condición monto a pagar es igual a saldo actual
            print ("inicio: saldo pago  ",saldo_pago," monto   ",self.monto)
            if self.monto == saldo_pago:
                # WHRC-LS se requiere para pagar cuotas SOLO en estado de no vigentes pero en reliquidacion
                if self.saldo_mora == 0.0 and self.monto_vigente == 0.0 and loan_obj.is_reliquidation:
                    move_id = False
                    for cuota in self.cuotas_ids:
                        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id),
                                                                               ('numero_cuota', '=', cuota.numero_cuota)])

                        cuota.saldo_pendiente = 0.0
                        cuota.monto_pago = self.monto
                        cuota.write({'state': 'pagada'})
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.write({'numero_deposito': self.numero_deposito})
                        obj_cuota.write({'description': self.notas})
                        obj_cuota.monto_pagado += self.monto
                    # print("nro cuota ",obj_cuota.numero_cuota, " monto cuota  ",obj_cuota.monto_cuota,"  saldo pendiente  ",obj_cuota.saldo_pendiente)
                    # verifica ultima cuota regula y llama a contabilizar
                    if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                        interes_pagados = obj_cuota.monto_cuota - obj_cuota.saldo_pendiente
                        capital = 0.0
                        interes = 0.0
                        if obj_cuota.interes > interes_pagados:
                            interes = obj_cuota.interes - interes_pagados
                            if self.monto > interes:
                                capital = self.monto - interes
                            else:
                                interes = self.monto
                        else:
                            capital = self.monto
                        move_id = self.generar_partida_contable(capital, interes, 0.0, self.monto)
                    else:
                        move_id = self.generar_partida_contable(obj_cuota.capital, obj_cuota.interes, 0.0, self.monto)
                    obj_cuota.saldo_pendiente = 0.0
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)
                #  saldo moroso cero y con cuota vigente (siempre hay solo una vigente)
                if self.saldo_mora == 0.0 and self.monto_vigente > 0:
                    # entrada pago cuota vigente ssi es pago normal
                    if not loan_obj.is_reliquidation:
                        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id),
                                                                                   ('numero_cuota', '=', self.numero_cuota)])
                        move_id = False
                        for cuota in self.cuotas_ids:
                            cuota.saldo_pendiente = 0.0
                            cuota.monto_pago = self.monto
                            cuota.write({'state': 'pagada'})
                            obj_cuota.write({'state': 'pagada'})
                            obj_cuota.write({'numero_deposito': self.numero_deposito})
                            obj_cuota.write({'description': self.notas})
                            obj_cuota.monto_pagado += self.monto
                    # entrada ssi es vigente con reliquidacion
                    if loan_obj.is_reliquidation:
                        move_id = False
                        for cuota in self.cuotas_ids:
                            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id),
                                                                                   ('numero_cuota', '=', cuota.numero_cuota)])

                            cuota.saldo_pendiente = 0.0
                            cuota.monto_pago = self.monto
                            cuota.write({'state': 'pagada'})
                            obj_cuota.write({'state': 'pagada'})
                            obj_cuota.write({'numero_deposito': self.numero_deposito})
                            obj_cuota.write({'description': self.notas})
                            obj_cuota.monto_pagado += self.monto
                    # print("2 monto cuota  ",obj_cuota.monto_cuota,"  saldo pendiente  ",obj_cuota.saldo_pendiente)
                    if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                        interes_pagados = obj_cuota.monto_cuota - obj_cuota.saldo_pendiente
                        capital = 0.0
                        interes = 0.0
                        if obj_cuota.interes > interes_pagados:
                            interes = obj_cuota.interes - interes_pagados
                            if self.monto > interes:
                                capital = self.monto - interes
                            else:
                                interes = self.monto
                        else:
                            capital = self.monto
                        move_id = self.generar_partida_contable(capital, interes, 0.0, self.monto)
                    else:
                        move_id = self.generar_partida_contable(obj_cuota.capital, obj_cuota.interes, 0.0, self.monto)
                    obj_cuota.saldo_pendiente = 0.0
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

                if self.saldo_mora > 0.0 and self.monto_vigente == 0.0:
                    monto_pagar = self.monto
                    interes = 0.0
                    capital = 0.0
                    mora = 0.0
                    for cuota in self.cuotas_ids:
                        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id),
                                                                                   ('numero_cuota', '=', cuota.numero_cuota)])
                        if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                            if obj_cuota.interes > obj_cuota.monto_pagado:
                                interes = obj_cuota.interes - obj_cuota.monto_pagado
                                mora = mora + (obj_cuota.mora)
                                capital = capital + (obj_cuota.capital)
                            else:
                                mora = mora + obj_cuota.mora
                                capital = capital + (obj_cuota.saldo_pendiente - obj_cuota.mora)
                        else:
                            interes = interes + (obj_cuota.interes - obj_cuota.monto_pagado)
                            capital = capital + obj_cuota.capital
                            mora = mora + obj_cuota.mora
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.write({'numero_deposito': self.numero_deposito})
                        obj_cuota.write({'description': self.notas})
                        obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
                        obj_cuota.saldo_pendiente = 0.0
                        cuota.monto_pago = cuota.saldo_pendiente
                        cuota.saldo_pendiente = 0.0
                        obj_cuota.mora = 0.0
                        cuota.write({'state': 'pagada'})
                    move_id = self.generar_partida_contable(capital, interes, mora, self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)
                # pago morosas y vigentes
                if self.saldo_mora > 0.0 and self.monto_vigente > 0.0:
                    interes = 0.0
                    capital = 0.0
                    mora = 0.0
                    for cuota in self.cuotas_ids:
                        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id),
                                                                                   ('numero_cuota', '=', cuota.numero_cuota)])
                        if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                            if obj_cuota.interes > obj_cuota.monto_pagado:
                                interes = obj_cuota.interes - obj_cuota.monto_pagado
                                mora = mora + (obj_cuota.mora)
                                capital = capital + (obj_cuota.capital)
                            else:
                                mora = mora + obj_cuota.mora
                                capital = capital + (obj_cuota.saldo_pendiente - obj_cuota.mora)
                        else:
                            interes = interes + (obj_cuota.interes - obj_cuota.monto_pagado)
                            capital = capital + obj_cuota.capital
                            mora = mora + obj_cuota.mora
                        cuota.monto_pago = cuota.saldo_pendiente
                        cuota.saldo_pendiente = 0.0
                        cuota.write({'state': 'pagada'})
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.write({'numero_deposito': self.numero_deposito})
                        obj_cuota.write({'description': self.notas})
                        obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
                        obj_cuota.saldo_pendiente = 0.0
                        obj_cuota.mora = 0.0
                    move_id = self.generar_partida_contable(capital, interes, mora, self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

            # Segunda Condición grande de monto a pagar es menor que el saldo
            if self.monto < saldo_pago:
                if self.saldo_mora == 0.0 and self.monto_vigente > 0:
                    obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id),
                                                                               ('numero_cuota', '=', self.numero_cuota)])
                    # Primero se paga interes despues se paga capital
                    move_id = False
                    capital = 0.0
                    interes = 0.0
                    if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                        interes_pagados = obj_cuota.monto_cuota - obj_cuota.saldo_pendiente
                        if obj_cuota.interes > interes_pagados:
                            interes = obj_cuota.interes - interes_pagados
                            if self.monto > interes:
                                capital = self.monto - interes
                            else:
                                interes = self.monto
                        else:
                            capital = self.monto
                    else:
                        if self.monto > obj_cuota.interes:
                            interes = obj_cuota.interes
                            capital = self.monto - interes
                        else:
                            interes = self.monto

                    move_id = self.generar_partida_contable(capital, interes, 0.0, self.monto)
                    for cuota in self.cuotas_ids:
                        cuota.saldo_pendiente = cuota.saldo_pendiente - self.monto
                        cuota.monto_pago = self.monto
                    obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - self.monto
                    obj_cuota.monto_pagado += self.monto

                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

                if self.saldo_mora > 0.0 and self.monto_vigente == 0.0:
                    cuota_dict = self.pagar_cuotasmorosas(self.monto)
                    move_id = self.generar_partida_contable(cuota_dict["capital"], cuota_dict["interes"], cuota_dict["mora"], self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

                if self.saldo_mora > 0.0 and self.monto_vigente > 0.0:
                    monto_disponible = self.monto
                    saldo_mora = round(self.saldo_mora, 2)
                    dict_values = {}
                    values = {}
                    if monto_disponible > saldo_mora:
                        valor = monto_disponible - saldo_mora
                        dict_values = self.pagar_cuotasmorosas(self.saldo_mora)
                        values = self.abono_cuotasvigentes(valor)
                        dict_values["capital"] = dict_values["capital"] + values["capital"]
                        dict_values["interes"] = dict_values["interes"] + values["interes"]
                    else:
                        dict_values = self.pagar_cuotasmorosas(monto_disponible)
                    move_id = self.generar_partida_contable(round(dict_values["capital"], 2), round(dict_values["interes"], 2), dict_values["mora"], self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

            # Tercer caso monto a pagar es mayor que saldo por tanto se abonara a capital
            if self.monto > saldo_pago and saldo_pago != 0.0:
                #raise Warning(_('El Monto a pagar es mayor que el saldo adeudado, primero realice el pago del saldo pe y luego realice un abono a capital'))

                if self.saldo_mora == 0.0 and self.monto_vigente > 0:
                    obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id),
                                                                               ('numero_cuota', '=', self.numero_cuota)])
                    values = self.abono_cuotasvigentes(self.monto_vigente)
                    abono = (self.monto - self.monto_vigente)
                    values["capital"] = values["capital"] + abono
                    self.abono_capital(abono)
                    move_id = self.generar_partida_contable(round(values["capital"], 2), round(values["interes"], 2), 0.0, self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

                if self.saldo_mora > 0.0 and self.monto_vigente == 0.0:
                    values = self.pagar_cuotasmorosas(self.saldo_mora)
                    abono = (self.monto - self.saldo_mora)
                    values["capital"] = values["capital"] + abono
                    self.abono_capital(abono)
                    move_id = self.generar_partida_contable(round(values["capital"], 2), round(values["interes"], 2), 0.0, self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

                if self.saldo_mora > 0.0 and self.monto_vigente > 0.0:
                    values = self.pagar_cuotasmorosas(self.saldo_mora)
                    vals = self.abono_cuotasvigentes(self.monto_vigente)
                    abono = (self.monto - self.saldo_mora - self.monto_vigente)
                    values["capital"] = values["capital"] + vals["capital"] + abono
                    values["interes"] = values["interes"] + vals["interes"]
                    self.abono_capital(abono)
                    move_id = self.generar_partida_contable(values["capital"], values["interes"], 0.0, self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

            # Abono a capital sin mora y sin cuotas vigentes
            print ("fin: saldo pago  ",self.saldo_pago," monto vigente  ",self.monto_vigente)
            if self.saldo_pago == 0.0 and self.monto_vigente == 0.0:
                # cuota_prestamo = round(self.prestamo_id.cuato_prestamo, 2)
                capital = self.capital_prestamo()
                print ("solo cuotas no vigentes monto  ",self.monto," capital  ",capital)
                if self.monto > capital:
                    raise Warning(_('Esta tratando de pagar mas del correspondiente del capital del prestamo actual'))
                self.abono_capital(self.monto)
                #print "llamo a la contable-----***** "
                move_id = self.generar_partida_contable(self.monto, 0.0, 0.0, self.monto)
                if move_id:
                    self.fct_crearpago_prestamo("Abono a Capital", move_id)
            #
        else:
            raise Warning(_('El monto a pagar debe de ser mayor que cero'))

class Loan(models.Model):
    _inherit = "loan.management.loan"


    def _get_default_end_reliquidation(self):
        self.end_reliquidation = True
    def _get_default_is_reliquidation(self):
        self.is_reliquidation = True

    lista_cuotas_activod = fields.Many2one("loan.management.loan", "Prestamo Reliquidado")
    is_reliquidation = fields.Boolean("Es reliquidación?", store=True)
    end_reliquidation = fields.Boolean("Fin reliquidación?", store=True)
    #monto_en_letras = fields.Char("Monto en letras", store=True)

    @api.multi
    def action_aprobar(self):
        obj_loan_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.id)])
        for cuota in obj_loan_cuota:
            cuota.state = 'novigente'
        self.write({'state': 'aprobado'})
        # self.saldo_pendiente = self.total_monto
        #print "%" * 50
        #print "self.gasto_timbre :", self.gasto_timbre
        if self.gasto_timbre > 0.0:
            #print "cuando se reliquida"
            #print "self.monto_solicitado :", self.monto_solicitado
            self.total_desembolso = self.monto_solicitado - self.gasto_timbre  # - self.gastos_papeleria - self.gasto_timbre
        else:
            #print "cuando no se reliquida"
            #print "self.monto_solicitado :", self.monto_solicitado
            self.total_desembolso = self.monto_solicitado
        self.fecha_aprobacion = datetime.now()
    # Generar partida de desembolso
    def generar_partida_contable(self):
        #print "contable heredada"
        account_move = self.env['account.move']
        lineas = []
        print "cuatro"
        vals_debit = {
            'debit': self.monto_solicitado,
            'credit': 0.0,
            'amount_currency': 0.0,
            'name': 'Desmbolso de prestamo a socios',
            'account_id': self.tipo_prestamo_id.cuenta_cartera.id,
            #'account_id': self.afiliado_id.property_account_receivable_id.id,
            'partner_id': self.afiliado_id.id,
            'date': self.fecha_desembolso,
        }
        #saca del banco la diferencia entre desgravamen y reliquidacion (aplica reliquidacion)
        vals_credit = {
            'debit': 0.0,
            'credit': self.monto_solicitado - self.gastos_papeleria - self.gasto_timbre,
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
        #ssi hay reliquidacion WR
        if self.gasto_timbre > 0 and self.is_reliquidation:
            vals_credit3 = {
                'debit': 0.0,
                'credit': self.gasto_timbre,
                'amount_currency': 0.0,
                'name': 'Reliquidacion prestamo' + ' ' + self.lista_cuotas_activod.name,
                'account_id': self.afiliado_id.property_account_receivable_id.id,
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
        if self.gasto_timbre > 0 and self.is_reliquidation:
            lineas.append((0, 0, vals_credit3))
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
    #esto iva ssi el reporte se disparaba desde este modulo
    # @api.onchange('monto_solicitado')
    # def calculatenumber(self):
    #     self.monto_en_letras = num2words(self.monto_solicitado,lang='es')
    #
    # @api.model
    # def reliquidacion_cron(self):
    #     print('Cron Reliquidaciones')
    #
    #     obj_loan = self.env["loan.management.loan"].search([('monto_en_letras', 'in', (False,None))])
    #     for record in obj_loan:
    #         record.monto_en_letras = num2words(record.monto_solicitado,lang='es')
