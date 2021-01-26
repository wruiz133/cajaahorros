# -*- encoding: utf-8 -*-
import odoo.addons.decimal_precision as dp
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import Warning
import pdb


class WizardPagoCuotas(models.TransientModel):
    _name = 'loan.wizard.payment'
    _inherit = ['mail.thread']
    _description = 'Asistente de Pagos'
    _rec_name = 'prestamo_id'

    def _get_prestamo(self):
        contexto = self._context
        if 'active_id' in contexto:
            loan_obj = self.env["loan.management.loan"].browse(contexto['active_id'])
            return loan_obj

    # Obtiene la cuota mas anterior mororsa
    def get_primeracuotamora(self, prestamo_id):
        obj_prestamo = self.env["loan.management.loan"].search([('id', '=', prestamo_id)])
        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', prestamo_id), 
                        ('state', '=', 'morosa')])
        arreglo = []
        for valor in obj_cuota:
            arreglo.append(valor.numero_cuota)
        numero_cuota = (min(arreglo))
        saldo_pendiente = 0.0
        capital = 0.0
        monto_cuota = 0.0
        interes = 0.0
        mora = 0.0
        result = {}
        for cuota in obj_prestamo.cuota_ids:
            if numero_cuota == cuota.numero_cuota and cuota.state == 'morosa':
                numero_cuota = cuota.numero_cuota
                saldo_pendiente = cuota.saldo_pendiente
                capital = cuota.capital
                monto_cuota = cuota.monto_cuota
                mora = cuota.mora
                interes = cuota.interes
                #print "primeractamora"
                #print round(numero_cuota, 2)
                #print round(saldo_pendiente, 2)
                #print round(capital, 2)
                #print round(monto_cuota, 2)
                #print round(mora, 2)
                #print round(interes, 2)
        result["numero_cuota"] = numero_cuota
        result["monto_cuota"] = monto_cuota
        result["saldo_pendiente"] = saldo_pendiente
        result["capital"] = capital
        result["mora"] = mora
        result["interes"] = interes
        return result

    # Obtiene primera  cuota normalmente usado para abono a capital
    def get_ultimacuota(self, prestamo_id):
        obj_prestamo = self.env["loan.management.loan"].search([('id', '=', prestamo_id)])
        numero_cuota = 0
        saldo_pendiente = 0
        capital = 0
        monto_cuota = 0
        result = {}
        for cuota in obj_prestamo.cuota_ids:
            if numero_cuota < cuota.numero_cuota and cuota.state == 'novigente' or cuota.state == 'vigente':
                numero_cuota = cuota.numero_cuota
                saldo_pendiente = cuota.saldo_pendiente
                capital = cuota.capital
                monto_cuota = cuota.monto_cuota
        result["numero_cuota"] = numero_cuota
        result["monto_cuota"] = monto_cuota
        result["saldo_pendiente"] = saldo_pendiente
        result["capital"] = capital
        return result

    def pagar_cuotasmorosas(self, pago_mora):
        monto_disponible = pago_mora
        #print "Cuotas morosas"
        #print round(monto_disponible,2)
        capital = 0.0
        interes = 0.0
        mora = 0.0
        result = {}
        while monto_disponible > 0:
            cuota_morosa_dict = self.get_primeracuotamora(self.prestamo_id.id)
            #print "sale primeracuota"
            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id), 
            ('numero_cuota', '=', cuota_morosa_dict["numero_cuota"])])
            saldo_cuota = obj_cuota.saldo_pendiente
            resta_monto = 0.0
            #print "en while"
            #
            if round(monto_disponible, 10) > round(saldo_cuota, 10):
                obj_cuota.write({'state': 'pagada'})
                obj_cuota.write({'numero_deposito': self.numero_deposito})
                obj_cuota.write({'description': self.notas})
                for cuota in self.cuotas_ids:
                    if cuota.numero_cuota == cuota_morosa_dict["numero_cuota"]:
                        cuota.write({'state': 'pagada'})
                        cuota.monto_pago = cuota.saldo_pendiente
                        cuota.saldo_pendiente = 0.0
                resta_monto = monto_disponible - saldo_cuota
                if obj_cuota.interes > obj_cuota.monto_pagado:
                    interes = interes + (obj_cuota.interes - obj_cuota.monto_pagado)
                    capital = capital + obj_cuota.capital
                else:
                    capital = capital + (obj_cuota.capital - (obj_cuota.monto_pagado - obj_cuota.interes))
                mora = mora + obj_cuota.mora
                obj_cuota.mora = 0.0
                obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
                obj_cuota.saldo_pendiente = 0

            elif round(monto_disponible, 10) < round(saldo_cuota, 10):
                #print "interes segun ciclo < motopagado salida"
                #print round(obj_cuota.interes, 2)
                #print round(obj_cuota.monto_pagado, 2)
                #print round(monto_disponible, 2)
                #print round(mora, 2)
                #print "saldos modificados:"
                if obj_cuota.interes > obj_cuota.monto_pagado:
                    if monto_disponible > obj_cuota.interes:
                        interes = interes + (obj_cuota.interes - obj_cuota.monto_pagado)
                        disponible = monto_disponible - obj_cuota.interes
                        #print round(interes,2)
                        #print round(disponible,2)
                        #print round(obj_cuota.mora,2)
                        #print "excepcion else"
                        if round(disponible, 10) > round(obj_cuota.mora, 10) and obj_cuota.mora > 0.0:
                            mora = mora + obj_cuota.mora
                            disponible = disponible - obj_cuota.mora
                            capital = capital + disponible
                            obj_cuota.mora = 0.0
                        else:
                            mora = mora + disponible
                            #print round(mora,2)
                            obj_cuota.mora = obj_cuota.mora - disponible
                            #print round(obj_cuota.mora,2)
                            #print round(capital,2)
                            #wr ****** pone a falta para contabilizar ****
                            capital = round(capital,2) + round(disponible,2)
                            #print "fin > motopagado y saldos"

                    else:
                        interes = monto_disponible
                else:
                    if obj_cuota.mora > 0.0:
                        if monto_disponible > obj_cuota.mora:
                            mora = mora + obj_cuota.mora
                            capital = monto_disponible - obj_cuota.mora
                            obj_cuota.mora = 0.0
                        else:
                            mora = monto_disponible
                            obj_cuota.mora = obj_cuota.mora - monto_disponible
                    else:
                        capital = capital + monto_disponible

                resta_monto = 0
                obj_cuota.monto_pagado += monto_disponible
                obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - monto_disponible
                for cuota in self.cuotas_ids:
                    if cuota.numero_cuota == cuota_morosa_dict["numero_cuota"]:
                        cuota.saldo_pendiente = cuota.saldo_pendiente - monto_disponible
                        cuota.monto_pago = monto_disponible
            else:
                #print round(obj_cuota.interes,2)
                #print round(obj_cuota.monto_pagado,2)
                #print round(resta_monto,2)
                #print "if forzado"
                if obj_cuota.interes > obj_cuota.monto_pagado:
                    interes = interes + (obj_cuota.interes - obj_cuota.monto_pagado)
                    disponible = monto_disponible - obj_cuota.interes
                    if round(disponible, 10) > round(obj_cuota.mora, 10) and obj_cuota.mora > 0.0:
                        mora = mora + obj_cuota.mora
                        disponible = disponible - obj_cuota.mora
                        capital = capital + disponible
                        obj_cuota.mora = 0.0
                    else:
                        mora = mora + disponible
                        obj_cuota.mora = obj_cuota.mora - disponible
                else:
                    mora = mora + obj_cuota.mora
                    capital = capital + (monto_disponible - obj_cuota.mora)

                obj_cuota.write({'state': 'pagada'})
                obj_cuota.write({'numero_deposito': self.numero_deposito})
                obj_cuota.write({'description': self.notas})
                obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
                resta_monto = 0.0
                for cuota in self.cuotas_ids:
                    if cuota.numero_cuota == cuota_morosa_dict["numero_cuota"]:
                        cuota.write({'state': 'pagada'})
                        cuota.monto_pago = obj_cuota.saldo_pendiente
                        cuota.saldo_pendiente = 0.0
                        resta_monto = 0
                obj_cuota.mora = 0.0
                obj_cuota.saldo_pendiente = 0.0
            #print "fin restamonto"
            monto_disponible = resta_monto
        result["capital"] = capital
        result["interes"] = interes
        result["mora"] = mora
        #print "retorno pago mora inicio"
        #print round(capital,2)
        #print round(interes,2)
        #print round(mora,2)
        #print "fin retorno mora "
        return result

    def abono_cuotasvigentes(self, monto):
        pago = round(monto, 2)
        monto_vigente = round(self.monto_vigente, 2)
        capital = 0.0
        interes = 0.0
        result = {}
        # print "cuota vigente  pago.....   ",pago
        # print "cuota vigente monto vigente....",monto_vigente
        if pago == monto_vigente:
            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id), 
                        ('numero_cuota', '=', self.numero_cuota)])
            obj_cuota.write({'state': 'pagada'})
            obj_cuota.write({'numero_deposito': self.numero_deposito})
            obj_cuota.write({'description': self.notas})
            obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
            obj_cuota.saldo_pendiente = 0.0
            for cuota in self.cuotas_ids:
                if cuota.state == 'vigente' and cuota.numero_cuota == obj_cuota.numero_cuota:
                    cuota.monto_pago = cuota.saldo_pendiente
                    cuota.saldo_pendiente = 0
                    cuota.write({'state': 'pagada'})
            capital = obj_cuota.capital
            interes = obj_cuota.interes
        if pago < monto_vigente and pago > 0.0:
            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id), 
                        ('numero_cuota', '=', self.numero_cuota)])
            obj_cuota.monto_pagado += pago
            obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - pago
            for cuota in self.cuotas_ids:
                if cuota.state == 'vigente' and cuota.numero_cuota == obj_cuota.numero_cuota:
                    cuota.saldo_pendiente = cuota.saldo_pendiente - pago
                    cuota.monto_pago = pago
            if obj_cuota.interes > obj_cuota.monto_pagado:
                interes_restante = obj_cuota.interes - obj_cuota.monto_pagado
                if pago > interes_restante:
                    interes = interes_restante
                    capital = obj_cuota.capital - interes
                else:
                    interes = pago
            else:
                capital = pago

        result["capital"] = capital
        result["interes"] = interes
        return result

    def abono_capital(self, monto):
        # cuota_prestamo = round(self.prestamo_id.cuato_prestamo, 2)
        monto_disponible = round(monto, 2)
        while monto_disponible > 0:
            cuota_dict = self.get_ultimacuota(self.prestamo_id.id)
            # capital_cuota = round(cuota_dict["capital"], 2)
            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id), 
                ('numero_cuota', '=', cuota_dict["numero_cuota"])])
            saldo_cuota = round(cuota_dict["saldo_pendiente"], 2) # round(obj_cuota.saldo_pendiente, 2)
            cuota = round(cuota_dict["monto_cuota"], 2) # round(obj_cuota.monto_cuota, 2)
            capital_cuota = round(cuota_dict["capital"], 2) # round(obj_cuota.capital, 2)
            resta_monto = 0
            nro_cuota = round(cuota_dict["numero_cuota"], 2)
            #WHRC daba error para nro_cuota = 0
            if nro_cuota > 0.0:
                # print "saldo cuota....",saldo_cuota
                # print "cuota.....",cuota
                if saldo_cuota == cuota:
                    print ("cuota nro: ",nro_cuota," en abono capita monto disponible...",monto_disponible," en abono capital capital cuota ....",capital_cuota )
                    #tolerancia por precision WHRC
                    dif = monto_disponible - capital_cuota
                    if dif < 0.5 and dif > -0.5:
                        monto_disponible = capital_cuota
                    #
                    if monto_disponible > capital_cuota:
                        resta_monto = monto_disponible - capital_cuota
                        obj_cuota.saldo_pendiente = 0.0
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.write({'numero_deposito': self.numero_deposito})
                        obj_cuota.write({'description': self.notas})
                        obj_cuota.monto_pagado += capital_cuota

                    if monto_disponible < capital_cuota:
                        obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - monto_disponible
                        obj_cuota.monto_pagado += monto_disponible
                        resta_monto = 0

                    if monto_disponible == capital_cuota:
                        obj_cuota.saldo_pendiente = 0
                        obj_cuota.monto_pagado += obj_cuota.capital
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.write({'numero_deposito': self.numero_deposito})
                        obj_cuota.write({'description': self.notas})
                        resta_monto = 0

                else:
                    if obj_cuota.state == "vigente":
                        # WHR aplica pagos K en parciales pagados
                        abonos = (capital_cuota - saldo_cuota) + monto_disponible
                    else:
                        abonos = (cuota - saldo_cuota) + monto_disponible
                    # print "abonos...",abonos
                    print ("else: cuota nro: ",nro_cuota," abonos...",abonos,"  capital cuota ....",capital_cuota )
                    if abonos > capital_cuota:
                        obj_cuota.saldo_pendiente = 0
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.write({'numero_deposito': self.numero_deposito})
                        obj_cuota.write({'description': self.notas})
                        obj_cuota.monto_pagado = capital_cuota
                        # resta_monto = abonos - monto_disponible
                        resta_monto = abonos - capital_cuota
                    elif abonos < capital_cuota:
                        obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - monto_disponible
                        obj_cuota.monto_pagado += monto_disponible
                        resta_monto = 0
                    else:
                        obj_cuota.saldo_pendiente = 0
                        obj_cuota.monto_pagado += capital_cuota
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.write({'numero_deposito': self.numero_deposito})
                        obj_cuota.write({'description': self.notas})
                        resta_monto = 0
            monto_disponible = resta_monto
            print("itero abono a K con : ", monto_disponible)
    def fct_crearpago_prestamo(self, mensaje, move_id):
        # No posteando el abono a capítal
        obj_pago = self.env["loan.pagos"]
        values = {
            'cliente_id': self.prestamo_id.afiliado_id.id,
            'fecha': self.date_payment,
            'prestamo_id': self.prestamo_id.id,
            'importe_pagado': self.monto,
            'state': 'done',
            'observaciones': mensaje,
        }
        pago_id = obj_pago.create(values)
        #WHRCrelacionar asiento al abono de capital en loan_pagos
        if mensaje in ('Abono a Capital'):
            pago_id.write({'asiento_id': move_id})
        #Par todos los abonos comunes
        if self.cuotas_ids and pago_id:
            dict_cuotas = []
            for cuota in self.cuotas_ids:
                obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', self.prestamo_id.id), 
                        ('numero_cuota', '=', cuota.numero_cuota)])
                if cuota.monto_pago > 0.0:
                    dict_cuotas.append(obj_cuota.id)
            pago_id.write({'cuotas': [(6, 0, dict_cuotas)]})
            if move_id:
                pago_id.write({'asiento_id': move_id})
    @api.one
    def set_pagos(self):
        # print "entre???"
        if self.monto > 0:
            if not self.has_revision_saldo:
                raise Warning(_('Primero genere la revisión de saldos, para poder realizar pagos'))

            saldo_pago = round(self.saldo_pago, 2)
            # Primera condición monto a pagar es igual a saldo actual
            # print ("inicio: saldo pago  ",self.saldo_pago," monto vigente  ",monto_vigente)
            if self.monto == saldo_pago:
                # Primera condición saldo en mora y sin cuotas vigentes
                if self.saldo_mora == 0.0 and self.monto_vigente > 0:
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
                        #print round(obj_cuota.monto_cuota, 2)
                        #print round(obj_cuota.saldo_pendiente, 10)
                        #print round(obj_cuota.interes, 10)
                        #print round(obj_cuota.monto_pagado, 10)
                        #print round(obj_cuota.mora, 10)
                        #print round(obj_cuota.capital, 10)

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
                        #print "fin2"
                    move_id = self.generar_partida_contable(capital, interes, mora, self.monto)
                    if move_id:
                        self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

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
                    # print "termino por aqui"
                if self.saldo_mora > 0.0 and self.monto_vigente == 0.0:
                    values = self.pagar_cuotasmorosas(self.saldo_mora)
                    # print "en morosas.......  ",values
                    abono = (self.monto - self.saldo_mora)
                    # print "abono capital....  ",abono
                    values["capital"] = values["capital"] + abono
                    print ("K luego de pago mora  ",values["capital"]," abono entra abono_capital ",abono)
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
            # print ("fin: saldo pago  ",self.saldo_pago," monto vigente  ",monto_vigente)
            if self.saldo_pago == 0.0 and self.monto_vigente == 0.0:
                # cuota_prestamo = round(self.prestamo_id.cuato_prestamo, 2)
                capital = self.capital_prestamo()
                # print ("solo cuotas no vigentes monto  ",self.monto," capital  ",capital)
                if self.monto > capital:
                    raise Warning(_('Esta tratando de pagar mas del correspondiente del capital del prestamo actual'))
                self.abono_capital(self.monto)
                move_id = self.generar_partida_contable(self.monto, 0.0, 0.0, self.monto)
                # print "retorno desde contable  ",move_id
                if move_id:
                    self.fct_crearpago_prestamo("Abono a Capital", move_id)

            # Cambiar de estado de la cuota
            self.write({'state': 'pagada'})

        else:
            raise Warning(_('El monto a pagar debe de ser mayor que cero'))

    def capital_prestamo(self):
        capital = 0.0
        for prestamo in self.prestamo_id:
            for cuota in prestamo.cuota_ids:
                if cuota.state == 'novigente':
                    capital += cuota.capital
        return round(capital,2)

    @api.onchange('es_liquidacion')
    def actualiza_montoliquidar(self):
        if self.es_liquidacion:
            self.monto = self.prestamo_id.saldo_liquidar

    def generar_partida_contable(self, capital, interes, mora, monto):
        account_move = self.env['account.move']
        lineas = []
        #print "inicia...."
        #print interes
        monto_pago = round(monto,2) - round(interes,2)
        # ssi se trabaja con mora se habilitara
        #if mora > 0.0:
        #    vals_mora = {
        #       'debit': 0.0,
        #        'credit': mora,
        #        'amount_currency': 0.0,
        #        'name': 'Pago de Mora',
        #        'account_id': self.prestamo_id.tipo_prestamo_id.cuenta_intereses_mora.id,
        #        'partner_id': self.prestamo_id.afiliado_id.id,
        #        'date': self.date_payment,
        #    }
        #    lineas.append((0, 0, vals_mora))

        if capital >= 0.0 :
            vals_capital = {
                'debit': 0.0,
                'credit':monto_pago,
                'amount_currency': 0.0,
                'name': 'Pago de Capital',
                'account_id': self.prestamo_id.tipo_prestamo_id.cuenta_cartera.id,
                # 'account_id': self.prestamo_id.afiliado_id.property_account_receivable_id.id,
                'partner_id': self.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_capital))
        if interes > 0.0:
            vals_interes = {
                'debit': 0.0,
                'credit': round(interes,2),
                'amount_currency': 0.0,
                'name': 'Pago de intereses',
                'account_id': self.prestamo_id.tipo_prestamo_id.cuenta_intereses.id,
                'partner_id': self.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_interes))

        if monto > 0.0:
            vals_banco = {
                'debit': monto,
                'credit': 0.0,
                'amount_currency': 0.0,
                'name': 'Pago de prestamo',
                'account_id': self.journal_id.default_debit_account_id.id,
                'partner_id': self.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_banco))
        if interes > 0.0 or self.prestamo_id.interes_insoluto > 0.0:
            interes_insoluto = 0.0
            # si esta reliquidando esto se usa para acomodar el asiento por la diferencia no cobrada en interese
            # es por pagos de liquidacion adelantada WHRRC
            if self.es_liquidacion:
                self.monto = self.prestamo_id.saldo_liquidar
                interes_insoluto = self.prestamo_id.interes_insoluto
                self.prestamo_id.saldo_pendiente = 0.0
            # hilo de liquidacion total expone los valores por liquidar ssi marca liquidar
			# WR-LS  asiento proporcional del interes diferido
            vals_debit1 = {
				'debit': round(interes,2) + interes_insoluto,
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
				'credit': round(interes,2) + interes_insoluto,
				'amount_currency': 0.0,
				'name': 'Pago Cuentas por Cobrar Diferido Intereses',
				'account_id': self.prestamo_id.tipo_prestamo_id.cuenta_ingreso.id,
				'partner_id': self.prestamo_id.afiliado_id.id,
				'date': self.date_payment,
			}
            lineas.append((0, 0, vals_credit2))

            # print monto_pago
            # print interes
            # print monto
        values = {
            'journal_id': self.journal_id.id,
            'date': self.date_payment,
            'ref': 'Pago de prestamo' + ' ' + self.prestamo_id.name,
            'line_ids': lineas,
        }
       # pdb.set_trace()        
        id_move = account_move.create(values)
        # print "ultimo a informar id move....   ",id_move.id
        return id_move.id

    @api.one
    def generarsaldos(self):
        if self.prestamo_id:
            if self.cuotas_ids:
                for fee in self.cuotas_ids:
                    fee.unlink()
            obj_cuota_payment = self.env["loan.wizard.payment.lines"]
            for cuota in self.prestamo_id.cuota_ids:
                if cuota.state == 'vigente' or cuota.state == 'morosa':
                    vals = {
                        'numero_cuota': cuota.numero_cuota,
                        'pago_cuota_id': self.id,
                        'fecha_pago': cuota.fecha_pago,
                        'monto_cuota': cuota.monto_cuota,
                        'mora': cuota.mora,
                        'saldo_pendiente': cuota.saldo_pendiente,
                        'state': cuota.state,
                    }
                    id_cuota = obj_cuota_payment.create(vals)
            self.write({'state': 'saldo'})
            self.has_revision_saldo = True

    def _get_values(self):
        if self.cuotas_ids:
            for fee in self.cuotas_ids:
                if fee.state == 'vigente':
                    self.monto_vigente = self.monto_vigente + fee.saldo_pendiente
                    self.numero_cuota = fee.numero_cuota
                if fee.state == 'morosa':
                    self.saldo_mora = self.saldo_mora + fee.saldo_pendiente
                    #self.write({'cuotas_mora_num': [(4, fee.id, None)]})
            self.saldo_pago = self.monto_vigente + self.saldo_mora

    def get_currency(self):
        return self.env.user.company_id.currency_id.id

    # Información General
    date_payment = fields.Date(string="Fecha de Pago", required=True, default=fields.Date.today)
    prestamo_id = fields.Many2one("loan.management.loan", "Prestamo", default=_get_prestamo)
    monto = fields.Float("Monto a Pagar", required=True)
    capital = fields.Monetary("Capital", compute=_get_values)
    saldo_pago = fields.Monetary("Saldo Pendiente", compute=_get_values)
    has_revision_saldo = fields.Boolean("Revision de Saldos")
    # Mora de Prestamo
    saldo_mora = fields.Monetary("Saldo en Mora",compute=_get_values)
    currency_id = fields.Many2one("res.currency", "Moneda", domain=[('active', '=', True)], default=get_currency)
    # cuotas_mora_num = fields.Many2many("loan.management.loan.cuota", string="Cuotas en Mora")
    # Cuota Vigente
    monto_vigente = fields.Monetary("Monto Vigente", compute=_get_values)
    numero_cuota = fields.Integer("Cuota Vigente #", compute=_get_values)
    numero_deposito = fields.Char("Nro deposito")
    es_desgravamen = fields.Boolean("Liquida Desgravamen?")
    es_liquidacion = fields.Boolean("Liquidacion Total Contrato?")
    # Cuotas
    cuotas_ids = fields.One2many("loan.wizard.payment.lines", "pago_cuota_id", "Cuotas a pagar")
    existe_cuota_morosa = fields.Boolean("Cuotas en Mora")
    state = fields.Selection([('borrador', 'Borrador'), ('cancelada', 'Cancelado'), ('saldo', 'Revisión de Saldo'),('pagada', 'Pagada')], 
        readonly=True, string='Estado del Pago', default='borrador')
    notas = fields.Text("Observaciones")
    journal_id = fields.Many2one("account.journal", "Metodo de pago", required=True, domain=[('type', 'in', ['bank', 'cash'])])

    @api.multi
    def set_borrador(self):
        self.write({'state': 'borrador'})

    @api.multi
    def set_cancelar(self):
        self.write({'state': 'cancelada'})


class WizardPagoCuotasLines(models.TransientModel):
    _name = 'loan.wizard.payment.lines'

    pago_cuota_id = fields.Many2one("loan.wizard.payment", "Pago")
    currency_id = fields.Many2one("res.currency", "Moneda", related="pago_cuota_id.currency_id")
    fecha_pago = fields.Date("Fecha de Pago")
    monto_cuota = fields.Monetary("Monto de Cuota")
    capital = fields.Monetary("Capital")
    saldo_pendiente = fields.Monetary("Saldo de Pendiente")
    state = fields.Selection([('cotizacion', 'Cotizacion'), ('cancelada', 'Cancelada'), ('novigente', 'No vigente'), ('vigente', 'Vigente'),('morosa', 'Morosa'),('pagada', 'Pagada')], 
        readonly=True, string='Estado de cuota', default='cotizacion')
    description = fields.Text("Notas Generales")
    numero_cuota = fields.Integer("# de cuota", readonly=True)
    monto_pago = fields.Monetary("Monto Pagado")
    mora = fields.Monetary("Mora")
    numero_deposito = fields.Char("Nro deposito")

