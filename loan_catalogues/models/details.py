# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import Warning


class details(models.Model):
    _name = "loan.details"
    _description = "Loan Detalles"

    loan_aportaciones_id = fields.Many2one("loan.aportaciones","Loan Aportaciones", store=True)
    catalogues_id = fields.Many2one("loan.catalogues", "Loan Catalogues", store=True)
    name_num = fields.Integer("loan.catalogues", related="catalogues_id.name_num",store=True)#Nombre numeérico si se requiere que el item de catálogo sea numérico
    value = fields.Float("Value", store=True)
    customer_id = fields.Many2one("res.partner","Customer", store=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    

