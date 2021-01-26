# -*- coding: utf-8 -*-

import base64
from odoo import http, _
from odoo.http import request
from odoo import models,registry, SUPERUSER_ID
from odoo.addons.website_portal.controllers.main import website_account

class website_account(website_account):

    @http.route()
    def account(self, **kw):
        """ Add ticket documents to main account page """
        response = super(website_account, self).account(**kw)
        partner = request.env.user.partner_id
        loan = request.env['partner.loan.details']
        loan_count = loan.sudo().search_count([
        ('partner_id', 'child_of', [partner.commercial_partner_id.id])
          ])
        response.qcontext.update({
        'loan_count': loan_count,
        })
        return response
        
    @http.route(['/my/loans', '/my/loans/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_loan(self, page=1, **kw):
        response = super(website_account, self)
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        loan_obj = http.request.env['partner.loan.details']
        domain = [
            ('partner_id', 'child_of', [partner.commercial_partner_id.id])
        ]
        # count for pager
        loan_count = loan_obj.sudo().search_count(domain)
        # pager
        pager = request.website.pager(
            url="/my/loans",
            total=loan_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        loans = loan_obj.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'loans': loans,
            'page_name': 'loan',
            'pager': pager,
            'default_url': '/my/loans',
        })
        return request.render("odoo_customer_supplier_loan.display_loans", values)
       
    @http.route(['/my/loan/<model("partner.loan.details"):loan>'], type='http', auth="user", website=True)
    def my_loan(self, loan=None, **kw):
        pdf = request.env['report'].sudo().get_pdf([loan.id], 'odoo_customer_supplier_loan.partner_loan_report_qweb', data=None)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=pdfhttpheaders)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
