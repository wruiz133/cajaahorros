# -*- encoding: utf-8 -*-
import odoo.addons.decimal_precision as dp
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import Warning
import pdb;
import time
from datetime import datetime, timedelta
from dateutil import relativedelta


class WizardPagoCuotasBatch(models.Model):
    _name = 'loan.wizard.payment.batch'
    _inherit = ['mail.thread']
    _description = 'Asistente de Pagos'
    _rec_name = 'prestamo_id'

    def _get_prestamo(self):
        contexto = self._context
        if 'active_id' in contexto:
            loan_obj = self.env["loan.management.loan"].browse(contexto['active_id'])
            return loan_obj
        #return ""

    # Obtiene la cuota mas anterior mororsa
    def get_primeracuotamora(self, prestamo_id,cuota):
        obj_prestamo = self.env["loan.management.loan"].search([('id', '=', cuota.prestamo_id.id)])
        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
                        ('state', '=', 'morosa')])
        #pdb.set_trace()
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
        result["numero_cuota"] = numero_cuota
        result["monto_cuota"] = monto_cuota
        result["saldo_pendiente"] = saldo_pendiente
        result["capital"] = capital
        result["mora"] = mora
        result["interes"] = interes
        return result

    # Obtiene primera  cuota normalmente usado para abono a capital
    def get_ultimacuota(self, prestamo_id,obj_couta):
        obj_prestamo = self.env["loan.management.loan"].search([('id', '=', obj_couta.prestamo_id.id)])
        #pdb.set_trace()
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

    def pagar_cuotasmorosas(self, pago_mora,cuota):
        #pdb.set_trace()
        monto_disponible = pago_mora
        capital = 0.0
        interes = 0.0
        mora = 0.0
        result = {}
        while monto_disponible > 0:
            cuota_morosa_dict = self.get_primeracuotamora(cuota.prestamo_id.id,cuota)
            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
            ('numero_cuota', '=', cuota_morosa_dict["numero_cuota"])])
            saldo_cuota = obj_cuota.saldo_pendiente
            resta_monto = 0.0
            if round(monto_disponible, 10) > round(saldo_cuota, 10):
                obj_cuota.write({'state': 'pagada'})
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
                if obj_cuota.interes > obj_cuota.monto_pagado:
                    if monto_disponible > obj_cuota.interes:
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

            monto_disponible = resta_monto
        result["capital"] = capital
        result["interes"] = interes
        result["mora"] = mora
        return result

    def abono_cuotasvigentes(self, monto,cuota):
        #pdb.set_trace()
        pago = round(monto, 2)
        monto_vigente = round(self.monto_vigente, 2)
        capital = 0.0
        interes = 0.0
        result = {}
        if pago == monto_vigente:
            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
                        ('numero_cuota', '=', self.numero_cuota)])
            obj_cuota.write({'state': 'pagada'})
            obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
            obj_cuota.saldo_pendiente = 0.0
         #   for cuota in self.cuotas_ids:
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

    def abono_capital(self, monto,obj_couta):
        # cuota_prestamo = round(self.prestamo_id.cuato_prestamo, 2)
        monto_disponible = round(monto, 2)
        #pdb.set_trace()
        while monto_disponible > 0:
            cuota_dict = self.get_ultimacuota(obj_couta.prestamo_id.id,obj_couta)
            # capital_cuota = round(cuota_dict["capital"], 2)
            obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', obj_couta.prestamo_id.id), 
                ('numero_cuota', '=', cuota_dict["numero_cuota"])])
            saldo_cuota = round(cuota_dict["saldo_pendiente"], 2) # round(obj_cuota.saldo_pendiente, 2)
            cuota = round(cuota_dict["monto_cuota"], 2) # round(obj_cuota.monto_cuota, 2)
            capital_cuota = round(cuota_dict["capital"], 2) # round(obj_cuota.capital, 2)
            resta_monto = 0
            if saldo_cuota == cuota:
                if monto_disponible > capital_cuota:
                    resta_monto = monto_disponible - capital_cuota
                    obj_cuota.saldo_pendiente = 0
                    obj_cuota.write({'state': 'pagada'})
                    obj_cuota.monto_pagado += capital_cuota

                if monto_disponible < capital_cuota:
                    obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - monto_disponible
                    obj_cuota.monto_pagado += monto_disponible
                    resta_monto = 0

                if monto_disponible == capital_cuota:
                    obj_cuota.saldo_pendiente = 0
                    obj_cuota.monto_pagado += obj_cuota.capital
                    obj_cuota.write({'state': 'pagada'})
                    resta_monto = 0

            else:
                abonos = (cuota - saldo_cuota) + monto_disponible
                if abonos > capital_cuota:
                    obj_cuota.saldo_pendiente = 0
                    obj_cuota.write({'state': 'pagada'})
                    obj_cuota.monto_pagado = capital_cuota
                    resta_monto = abonos - monto_disponible
                elif abonos > capital_cuota:
                    obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - monto_disponible
                    obj_cuota.monto_pagado += monto_disponible
                    resta_monto = 0
                else:
                    obj_cuota.saldo_pendiente = 0
                    obj_cuota.monto_pagado += capital_cuota
                    obj_cuota.write({'state': 'pagada'})
                    resta_monto = 0
            monto_disponible = resta_monto

    def fct_crearpago_prestamo(self, mensaje, move_id,obj_couta):
        # No posteando el abono a capítal
        #pdb.set_trace()
        obj_pago = self.env["loan.pagos"]
        values = {
            'cliente_id': obj_couta.prestamo_id.afiliado_id.id,
            'fecha': self.date_payment,
            'prestamo_id': obj_couta.prestamo_id.id,
            'importe_pagado': obj_couta.monto_cuota,
            'state': 'done',
            'observaciones': mensaje,
        }
        pago_id = obj_pago.create(values)
        ##pdb.set_trace()
        if obj_couta.id and pago_id:
            dict_cuotas = []
            for cuota in obj_couta:
                obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
                        ('numero_cuota', '=', cuota.numero_cuota)])
                if cuota.monto_cuota > 0.0:
                    dict_cuotas.append(obj_cuota.id)
            pago_id.write({'cuotas': [(6, 0, dict_cuotas)]})
            if move_id:
                pago_id.write({'asiento_id': move_id})

    @api.one
    def set_pagos(self):
        if self.monto > 0:
            #pdb.set_trace()
            if not self.has_revision_saldo:
                raise Warning(_('Primero genere la revisión de saldos, para poder realizar pagos'))

            saldo_pago = round(self.saldo_pago, 2)
            monto = round(self.monto, 2)
            # Primera condición monto a pagar es igual a saldo actual
            if monto == saldo_pago:
                # Primera condición saldo en mora y sin cuotas vigentes
                if self.saldo_mora == 0.0 and self.monto_vigente > 0:
                    for cuotas_id in self.cuotas_ids:
                        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuotas_id.prestamo_id.id), 
                            ('numero_cuota', '=', cuotas_id.numero_cuota)])
                        move_id = False
                        for cuota in self.cuotas_ids:
                            cuota.saldo_pendiente = 0.0
                            cuota.monto_pago = monto
                            cuota.write({'state': 'pagada'})
                            obj_cuota.write({'state': 'pagada'})
                            obj_cuota.monto_pagado += monto
                        if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                            interes_pagados = obj_cuota.monto_cuota - obj_cuota.saldo_pendiente
                            capital = 0.0
                            interes = 0.0
                            if obj_cuota.interes > interes_pagados:
                                interes = obj_cuota.interes - interes_pagados
                                if monto > interes:
                                    capital = monto - interes
                                else:
                                    interes = monto
                            else:
                                capital = monto
                            move_id = self.generar_partida_contable(capital, interes, 0.0, self.monto,obj_cuota)
                        else:
                            move_id = self.generar_partida_contable(obj_cuota.capital, obj_cuota.interes, 0.0, self.monto,obj_cuota)
                        obj_cuota.saldo_pendiente = 0.0
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id,obj_cuota)

                if self.saldo_mora > 0.0 and self.monto_vigente == 0.0:
                    monto_pagar = monto
                    interes = 0.0
                    capital = 0.0
                    mora = 0.0
                    for cuota in self.cuotas_ids:
                        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
                            ('numero_cuota', '=', cuota.numero_cuota)])
                        # print "cuota.prestamo_id.id  ", cuota.prestamo_id.id
                        # print("cuota.numero_cuota  ",cuota.numero_cuota)
                        if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                            if obj_cuota.interes > obj_cuota.monto_pagado:
                                interes = obj_cuota.interes - obj_cuota.monto_pagado
                                mora = mora + (obj_cuota.mora)
                                capital = capital + (obj_cuota.capital)
                            else:
                                mora = mora + obj_cuota.mora
                                capital = capital + (obj_cuota.saldo_pendiente - obj_cuota.mora)
                        else:
                            # print "antes interes",interes
                            interes = interes + (obj_cuota.interes - obj_cuota.monto_pagado)
                            capital = capital + obj_cuota.capital
                            mora = mora + obj_cuota.mora
                        obj_cuota.write({'state': 'pagada'})
                        obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
                        obj_cuota.saldo_pendiente = 0.0
                        cuota.monto_pago = cuota.saldo_pendiente
                        cuota.saldo_pendiente = 0.0
                        obj_cuota.mora = 0.0
                        print "interes", interes
                        cuota.write({'state': 'pagada'})
                        move_id = self.generar_partida_contable(capital, interes, mora, monto,obj_cuota)
                        interes = 0.0
                        capital = 0.0
                        mora = 0.0
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id,obj_cuota)

                if self.saldo_mora > 0.0 and self.monto_vigente > 0.0:
                    interes = 0.0
                    capital = 0.0
                    mora = 0.0
                    for cuota in self.cuotas_ids:
                        obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
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
                        obj_cuota.monto_pagado += obj_cuota.saldo_pendiente
                        obj_cuota.saldo_pendiente = 0.0
                        obj_cuota.mora = 0.0
                        move_id = self.generar_partida_contable(capital, interes, mora, monto,obj_cuota)
                        interes = 0.0
                        capital = 0.0
                        mora = 0.0
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id,obj_cuota)

            # Segunda Condición grande de monto a pagar es menor que el saldo
            if monto < saldo_pago:
                for cuota in self.cuotas_ids:
                    obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
                        ('numero_cuota', '=', cuota.numero_cuota)])
                    if self.saldo_mora == 0.0 and self.monto_vigente > 0:
                        # Primero se paga interes despues se paga capital
                        move_id = False
                        capital = 0.0
                        interes = 0.0
                        if obj_cuota.monto_cuota > obj_cuota.saldo_pendiente:
                            interes_pagados = obj_cuota.monto_cuota - obj_cuota.saldo_pendiente
                            if obj_cuota.interes > interes_pagados:
                                interes = obj_cuota.interes - interes_pagados
                                if monto > interes:
                                    capital = monto - interes
                                else:
                                    interes = monto
                            else:
                                capital = monto
                        else:
                            if monto > obj_cuota.interes:
                                interes = obj_cuota.interes
                                capital = monto - interes
                            else:
                                interes = monto

                        move_id = self.generar_partida_contable(capital, interes, 0.0, monto,obj_cuota)
                        capital = 0.0
                        interes = 0.0
                        for cuota in self.cuotas_ids:
                            cuota.saldo_pendiente = cuota.saldo_pendiente - monto
                            cuota.monto_pago = monto
                        obj_cuota.saldo_pendiente = obj_cuota.saldo_pendiente - monto
                        obj_cuota.monto_pagado += monto
    
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id,obj_cuota)
        
                    if self.saldo_mora > 0.0 and self.monto_vigente == 0.0:
                        cuota_dict = self.pagar_cuotasmorosas(monto,obj_cuota)
                        move_id = self.generar_partida_contable(cuota_dict["capital"], cuota_dict["interes"], cuota_dict["mora"], monto,obj_cuota)
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id,obj_cuota)
        
                    if self.saldo_mora > 0.0 and self.monto_vigente > 0.0:
                        monto_disponible = monto
                        saldo_mora = round(self.saldo_mora, 2)
                        dict_values = {}
                        values = {}
                        if monto_disponible > saldo_mora:
                            valor = monto_disponible - saldo_mora
                            dict_values = self.pagar_cuotasmorosas(self.saldo_mora,cuota)
                            values = self.abono_cuotasvigentes(valor,obj_cuota)
                            dict_values["capital"] = dict_values["capital"] + values["capital"]
                            dict_values["interes"] = dict_values["interes"] + values["interes"]
                        else:
                            dict_values = self.pagar_cuotasmorosas(monto_disponible,cuota)
                        move_id = self.generar_partida_contable(round(dict_values["capital"], 2), round(dict_values["interes"], 2), dict_values["mora"], monto,obj_cuota)
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id, obj_cuota)

            # Tercer caso monto a pagar es mayor que saldo por tanto se abonara a capital
            if monto > saldo_pago and saldo_pago != 0.0:
                raise Warning(_('El Monto a pagar es mayor que el saldo adeudado, primero realice el pago del saldo pendiente y luego realice un abono a capital'))
                for cuota in self.cuotas_ids:
                    obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
                        ('numero_cuota', '=', self.numero_cuota)])

                    if self.saldo_mora == 0.0 and self.monto_vigente > 0:
                        values = self.abono_cuotasvigentes(self.monto_vigente,obj_cuota)
                        abono = (monto - self.monto_vigente)
                        values["capital"] = values["capital"] + abono
                        self.abono_capital(abono,obj_cuota)
                        move_id = self.generar_partida_contable(round(values["capital"], 2), round(values["interes"], 2), 0.0, monto,obj_cuota)
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id,obj_cuota)
        
                    if self.saldo_mora > 0.0 and self.monto_vigente == 0.0:
                        values = self.pagar_cuotasmorosas(self.saldo_mora,obj_cuota)
                        abono = (monto - self.saldo_mora)
                        values["capital"] = values["capital"] + abono
                        self.abono_capital(abono,obj_cuota)
                        move_id = self.generar_partida_contable(round(values["capital"], 2), round(values["interes"], 2), 0.0, monto,obj_cuota)
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id,obj_cuota)
        
                    if self.saldo_mora > 0.0 and self.monto_vigente > 0.0:
                        values = self.pagar_cuotasmorosas(self.saldo_mora,obj_cuota)
                        vals = self.abono_cuotasvigentes(self.monto_vigente.obj_cuota)
                        abono = (monto - self.saldo_mora - self.monto_vigente)
                        values["capital"] = values["capital"] + vals["capital"] + abono
                        values["interes"] = values["interes"] + vals["interes"]
                        self.abono_capital(abono)
                        move_id = self.generar_partida_contable(values["capital"], values["interes"], 0.0, monto,obj_cuota)
                        if move_id:
                            self.fct_crearpago_prestamo("Pago de cuota(s)", move_id)

            # Abono a capital sin mora y sin cuotas vigentes
            for cuota in self.cuotas_ids:
                obj_cuota = self.env["loan.management.loan.cuota"].search([('prestamo_id', '=', cuota.prestamo_id.id), 
                    ('numero_cuota', '=', self.numero_cuota)])
                if self.saldo_pago == 0.0 and self.monto_vigente == 0.0:
                    # cuota_prestamo = round(self.prestamo_id.cuato_prestamo, 2)
                    capital = self.capital_prestamo(obj_cuota)
                    if monto > capital:
                        raise Warning(_('Esta tratando de pagar mas del correspondiente del capital del prestamo actual'))
                    self.abono_capital(monto,obj_cuota)
                    move_id = self.generar_partida_contable(monto, 0.0, 0.0, monto,obj_cuota)
                    if move_id:
                        self.fct_crearpago_prestamo("Abono a Capital", move_id)
    
                # Cambiar de estado
                self.write({'state': 'pagada'})

        else:
            raise Warning(_('El monto a pagar debe de ser mayor que cero'))

    def capital_prestamo(self,obj_cuota):
        #pdb.set_trace()
        capital = 0.0
        for prestamo in obj_cuota.prestamo_id:
            for cuota in prestamo.cuota_ids:
                if cuota.state == 'novigente':
                    capital += cuota.capital
        return capital

    def generar_partida_contable(self, capital, interes, mora, monto,obj_cuota):
        #pdb.set_trace()
        account_move = self.env['account.move']
        lineas = []
        # print "/" * 100
        # print round(mora, 10)
        # print round(capital, 10)
        # print ("interes ",round(interes, 10))
        # print("monto_cuota   ", round(obj_cuota.monto_cuota, 10))
        # aqui se toman las parciales
        monto_pago = round(obj_cuota.monto_cuota,2) - round(interes,2)
        print("socio en proceso :   ", obj_cuota.prestamo_id.afiliado_id.name)
        print "monto a pago    ", monto_pago
        print "monto_cuota   ", round(obj_cuota.monto_cuota,2)
        # print "/" * 100
        
        # if mora > 0.0:
        #     vals_mora = {
        #         'debit': 0.0,
        #         'credit': mora,
        #         'amount_currency': 0.0,
        #         'name': 'Masivo: Pago de Mora Cuota ' + str(obj_cuota.numero_cuota),
        #         'account_id': obj_cuota.prestamo_id.tipo_prestamo_id.cuenta_intereses_mora.id,
        #         'partner_id': obj_cuota.prestamo_id.afiliado_id.id,
        #         'date': self.date_payment,
        #     }
        #     lineas.append((0, 0, vals_mora))

        if capital > 0.0:
            vals_capital = {
                'debit': 0.0,
                'credit': monto_pago,
                'amount_currency': 0.0,
                'name': 'Masivo: Pago de Capital Cuota' + str(obj_cuota.numero_cuota),
                'account_id':  obj_cuota.prestamo_id.tipo_prestamo_id.cuenta_cartera.id,
                # 'account_id': obj_cuota.prestamo_id.afiliado_id.property_account_receivable_id.id,
                'partner_id': obj_cuota.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_capital))

        if interes > 0.0:
            vals_interes = {
                'debit': 0.0,
                'credit': round(interes,2),
                'amount_currency': 0.0,
                'name': 'Masivo: Pago de intereses Cuota '+ str(obj_cuota.numero_cuota),
                'account_id': obj_cuota.prestamo_id.tipo_prestamo_id.cuenta_intereses.id,
                'partner_id': obj_cuota.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_interes))

        if monto > 0.0:
            vals_banco = {
                'debit': round(obj_cuota.monto_cuota,2),
                'credit': 0.0,
                'amount_currency': 0.0,
                'name': self.prestamo_id+' de prestamo '+ obj_cuota.prestamo_id.name,
                'account_id': obj_cuota.prestamo_id.journal_id.default_debit_account_id.id,
                'partner_id': obj_cuota.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_banco))

        if interes > 0.0:
            # WR-LS  asiento proporcional del interes diferido 3/09/2019
            vals_debit1 = {
                'debit': round(interes, 2),
                'credit': 0.0,
                'amount_currency': 0.0,
                'name': 'Masivo: Amortizacion Pasivo Diferido Cuota ' + str(obj_cuota.numero_cuota),
                'account_id': obj_cuota.prestamo_id.tipo_prestamo_id.cuenta_diferido.id,
                'partner_id': obj_cuota.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_debit1))

            vals_credit2 = {
                'debit': 0.0,
                'credit': round(interes, 2),
                'amount_currency': 0.0,
                'name': 'Masivo: Pago Cuentas por Cobrar Diferido Intereses Cuota ' + str(obj_cuota.numero_cuota),
                'account_id': obj_cuota.prestamo_id.tipo_prestamo_id.cuenta_ingreso.id,
                'partner_id': obj_cuota.prestamo_id.afiliado_id.id,
                'date': self.date_payment,
            }
            lineas.append((0, 0, vals_credit2))
        # print "Linea ", lineas
        values = {
            'journal_id': obj_cuota.prestamo_id.journal_id.id,
            'date': self.date_payment,
            'ref': self.prestamo_id+ ' ' + obj_cuota.prestamo_id.name,
            'line_ids': lineas,
        }
        ##pdb.set_trace()
        id_move = account_move.create(values)
        print ("socio pasa:   ",obj_cuota.prestamo_id.afiliado_id.name)
        return id_move.id

    @api.one
    def generarsaldosbatch(self):
       # #pdb.set_trace()
        #pdb.set_trace()
        # obj_cuota_ids = self.env["loan.management.loan.cuota"].search([('state', '=',self.state_cuota),
        #                                                                ('fecha_pago','>=',self.date_start),
        #                                                                ('fecha_pago','<=',self.date_end)])
        obj_cuota_ids = self.env["loan.management.loan.cuota"].search(['&','|',('state', '=',self.state_cuota),('state', 'in',('vigente','morosa')),
                                                                       ('fecha_pago','>=',self.date_start),
                                                                       ('fecha_pago','<=',self.date_end),
                                                                       ('cuenta_banco','in',(self.bic,None))])

  #      for cuota_vigentes_id in obj_cuota_ids:
  #          if cuota_vigentes_id:
   #             for fee in cuota_vigentes_id:
    #                fee.unlink()
        obj_cuota_payment = self.env["loan.wizard.payment.lines.batch"]
        for cuota in obj_cuota_ids:
            if cuota.state == 'vigente' or cuota.state == 'morosa':
                vals = {
                    'prestamo_id': cuota.prestamo_id.id,
                    'afiliado_id': cuota.afiliado_id.id,
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

    @api.depends('cuotas_ids')
    def _get_values(self):
        ##pdb.set_trace()
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
        ##pdb.set_trace()
        return self.env.user.company_id.currency_id.id

    # Información General
    date_payment = fields.Date(string="Fecha de Pago", required=True, default=fields.Date.today)
    prestamo_id = fields.Char("Pago prestamos", required=True, default=lambda self: self.env['ir.sequence'].get('pago'))
    #prestamo_id = fields.Many2one("loan.management.loan", "Prestamo", required=False)
    monto = fields.Float("Monto a Pagar", required=True)
    saldo_pago = fields.Monetary("Saldo Pendiente", compute=_get_values)
    has_revision_saldo = fields.Boolean("Revision de Saldos")
    # Mora de Prestamo
    saldo_mora = fields.Monetary("Saldo en Mora",compute=_get_values)
    currency_id = fields.Many2one("res.currency", "Moneda", domain=[('active', '=', True)], default=get_currency)
    # cuotas_mora_num = fields.Many2many("loan.management.loan.cuota", string="Cuotas en Mora")
    # Cuota Vigente
    monto_vigente = fields.Monetary("Monto Vigente", compute=_get_values)
    numero_cuota = fields.Integer("Cuota Vigente #", compute=_get_values)
    # Cuotas
    cuotas_ids = fields.One2many("loan.wizard.payment.lines.batch", "pago_cuota_id", "Cuotas a pagar")
    existe_cuota_morosa = fields.Boolean("Cuotas en Mora")
    state = fields.Selection([('borrador', 'Borrador'), ('cancelada', 'Cancelado'), ('saldo', 'Revisión de Saldo'),('pagada', 'Pagada')], 
        readonly=True, string='Estado del Pago', default='borrador')
    state_cuota = fields.Selection(
        [('novigente', 'No vigente'), ('vigente', 'Vigente'),('morosa', 'Morosa'),('moroyvige', 'Todas')], string='Estado de cuota', default='moroyvige')
    #para tomar dentro del rango de fechas y estado como criterios
    date_start = fields.Date(string='Date From', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, default=time.strftime('%Y-%m-01'))
    date_end = fields.Date(string='Date To', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    notas = fields.Text("Observaciones")
    journal_id = fields.Many2one("account.journal", "Metodo de pago", required=True, domain=[('type', 'in', ['bank', 'cash'])])
    bic_id = fields.Many2one("res.bank", "Codigo Banco", required=True)
    bic = fields.Char("Codigo Banco", related='bic_id.bic')

    @api.multi
    def set_borrador(self):
        self.write({'state': 'borrador'})

    @api.multi
    def set_cancelar(self):
        self.write({'state': 'cancelada'})


class WizardPagoCuotasLinesBatch(models.Model):
    _name = 'loan.wizard.payment.lines.batch'

    pago_cuota_id = fields.Many2one("loan.wizard.payment.batch", "Pago")
    prestamo_id = fields.Many2one("loan.management.loan", "Prestamo", required=False)
    afiliado_id = fields.Many2one("res.partner", "Afiliado")
    currency_id = fields.Many2one("res.currency", "Moneda", related="pago_cuota_id.currency_id")
    fecha_pago = fields.Date("Fecha de Pago")
    monto_cuota = fields.Monetary("Monto de Cuota")
    saldo_pendiente = fields.Monetary("Saldo de Pendiente")
    state = fields.Selection([('cotizacion', 'Cotizacion'), ('cancelada', 'Cancelada'), ('novigente', 'No vigente'), ('vigente', 'Vigente'),('morosa', 'Morosa'),('pagada', 'Pagada')], 
        readonly=True, string='Estado de cuota', default='cotizacion')
    description = fields.Text("Notas Generales")
    numero_cuota = fields.Integer("# de cuota", readonly=True)
    monto_pago = fields.Monetary("Monto Pagado")
    mora = fields.Monetary("Mora")

