# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class loan_catalogues(models.Model):
    """Tabla que almacena catálogos"""
    _name = "loan.catalogues"
    _description = "Loan Catalogues"

    code = fields.Char("Catalogue Code")
    name = fields.Char("Catalogue Name")  # Nombre Del Catálogo
    name_num = fields.Integer("Catalogue Name Numeric")  # Nombre numérico si se requiere que el item de catálogo sea numérico
    parent_id = fields.Many2one("loan.catalogues", "Related Catalogue", select=True)  # relación recursiva
    parent_name = fields.Char("loan.catalogues", related="parent_id.code", store=True, readonly=True)  # almacena código del catálogo padre
    child_ids = fields.One2many("loan.catalogues", "parent_id", "Catalogue")  #
    parent = fields.Boolean("Is parent?")  # se debe marcar si es el catálogo principal
    account_portfolio_id = fields.Many2one("account.account", "Cta. Cartera")
    account_provizion_id = fields.Many2one("account.account", "Cta. Provisión")