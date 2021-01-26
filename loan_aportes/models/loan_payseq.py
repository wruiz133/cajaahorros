#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

#aumenta el fk al loan.aportaciones contra el modelo
class SecuenciaEgreso(models.Model):
    _name = "account.payment"
    _inherit = 'account.payment'

    outfund_seq = fields.Char("Nro Egreso")
    @api.multi
    def post(self):
        """ escribe el secuencial de desembolso en facturas de proveedor WHRC  """
        for rec in self:
            if any(inv.state == 'open' for inv in rec.invoice_ids):
                # print("si entro aqui ",rec.partner_type, "  y ",rec.payment_type)
                if rec.partner_type == 'supplier' and rec.payment_type == 'outbound':
                    seq = 'desembolso'
                    rec.outfund_seq = self.env['ir.sequence'].next_by_code(seq)
                    return super(SecuenciaEgreso, self).post() #llama para el resto de ejecucion

                if not rec.outfund_seq:
                    raise UserError(_("You have to define a sequence for desembolso in your company."))
            else:
                return super(SecuenciaEgreso, self).post() #pasa el control al original
