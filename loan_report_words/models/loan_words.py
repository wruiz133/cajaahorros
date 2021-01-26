# -*- encoding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import Warning
from num2words import num2words


class Loan(models.Model):
    _inherit = "loan.management.loan"

    monto_en_letras = fields.Char("Monto en letras", store=True)


    @api.onchange('monto_solicitado')
    def calculatenumber(self):
        if self.monto_solicitado not in [False, None]:
            # se incluye los gastos de desgravamen
            #self.monto_neto_desembolso = self.monto_solicitado - self.gastos_papeleria
            print("ENTROOOOOOOOOOOOOOOOOO")
            self.monto_en_letras = num2words(self.monto_neto_desembolso, lang='es')
            print ("self.monto_en_letras:  ", self.monto_en_letras)

    @api.multi
    def reliquidacion_cron(self):
        print('INICIA CRON')
        obj_loan = self.env["loan.management.loan"].search([('monto_en_letras', 'in', [False, None])])
        if obj_loan:
            for record in obj_loan:
                # record.monto_en_letras = num2words(record.monto_solicitado,lang='es')
                record.monto_en_letras = num2words(record.monto_neto_desembolso, lang='es')
        print("FINALIZA EL CRON ")


