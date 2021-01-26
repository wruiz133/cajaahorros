# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning



class Aportaciones(models.Model):
    _inherit = "loan.aportaciones"

    details_ids = fields.One2many("loan.details", "loan_aportaciones_id", "Loan Detalles")

    # @api.onchange("monto_aportacion")
    @api.multi
    def set_values(self):
        lista = []
        # crea el objeto en details.py, aqui recorre catalogo y llena details
        #obj_catalogues = self.env['loan.catalogues'].search([('parent_name', '=', 'CLASSIFICATION')])
        domain = [('parent_name', '=', 'CLASSIFICATION')]
        fields = ['id','name_num']
        obj_catalogues = self.env['loan.catalogues'].search_read(domain, fields)
        obj_details = self.env['loan.details']
        if self.details_ids:
            for rec in self.details_ids:
                rec.unlink()
        if self.monto_aportacion > 0:
            for cat in obj_catalogues:
                values = dict(loan_aportaciones_id=self.id,
                              catalogues_id=cat['id'],
                              #name_num=cat['name_num'],  esto da problemas de tiempo de respuesta lentisimo
                              value=self.monto_aportacion * float(float(cat['name_num']) / 100),
                              customer_id=self.cliente_id.id,
                              )
                obj_details.create(values)
                #lista.append(values)  esta por ver como se contruye la lista apropiada
            #obj_details.create(lista)

    def generar_partida_contable(self):
        lineas = []
        account_move = self.env['account.move']
        print "uno"
        #recorre details que lleno antes y desde este metodo cotabiliza todos los detalles del asiento
        for details in self.details_ids:
            # print "voy vy ", details.catalogues_id.account_portfolio_id.id
            vals_credit = {
                'debit': 0.0,
                'credit': details.value,
                'amount_currency': 0.0,
                'name': details.catalogues_id.name,
                # 'account_id': self.cliente_id.property_account_payable_id.id,
                'account_id': details.catalogues_id.account_portfolio_id.id,
                'partner_id': self.cliente_id.id,
                'date': self.fecha,
                'account_provizion_id':details.catalogues_id.account_provizion_id.id,

            }
            lineas.append((0, 0, vals_credit))
        #print "listado de 5 clasificaiones"
        #print lineas
        vals_debit = {
            'debit': self.monto_aportacion,
            'credit': 0.0,
            'amount_currency': 0.0,
            'name': 'Aportación de cliente',
            'account_id': self.journal_id.default_debit_account_id.id,
            'partner_id': self.cliente_id.id,
            'date': self.fecha,
        }
        lineas.append((0, 0, vals_debit))
        # lineas.append((0, 0, vals_credit))
        aport = self.name
        values = {
            'journal_id': self.journal_id.id,
            'date': self.fecha,
            'ref': 'Aportación de cliente',
            'line_ids': lineas,
            'partner_id': self.cliente_id.id,
        }
        id_move = account_move.create(values)
        return id_move.id