# -*- coding: utf-8 -*-

import time

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import Warning

class PartnerLoanInstallmentDetails(models.Model):
    _inherit = 'partner.loan.installment.details'
    
    bank_journal_id = fields.Many2one(
        'account.journal',
        'Bank/Cash Journal',
    )
    bank_account_id = fields.Many2one(
        'account.account',
        'Bank/Cash Account',
        related="bank_journal_id.default_debit_account_id",
        stored=True,
    )
    recievable_account_id = fields.Many2one(
        'account.account',
        'Interest Receivable Account',
        related="loan_id.interest_receivable_account_id",
        stored=True,
    )
    total_amt_move_id = fields.Many2one(
        'account.move',
        'Loan Installment Entry',
        readonly=True, 
        copy=False
    )
    
    
    
    @api.multi
    def book_interest_new(self):
        move_pool = self.env['account.move']  
        for install in self:
            vals = {}
            timenow = time.strftime('%Y-%m-%d')
            address_id = install.partner_id or False
            partner_id = address_id and address_id and address_id.id or False
            
            if not partner_id:
                raise Warning(_('Please configure Home Address On partner.')) 
            
            move = {
                'narration': install.name,
                'date': install.date_from,
                'ref': install.name,
                'journal_id': install.bank_journal_id.id,
            }
            if install.interest_amt > 0.0:
                credit_account_id = install.recievable_account_id
                if not install.bank_journal_id:
                    raise Warning(_('Please configure Bank Journal.'))
                if not credit_account_id:
                    raise Warning(_('Please configure Debit/Credit accounts on the Journal %s ') % (install.bank_journal_id.name))
                credit_account_id = credit_account_id.id
                debit_account_id = install.bank_account_id.id or False
                if not debit_account_id:
                    raise Warning(_('Please configure debit account of partner'))
                
                debit_line = (0, 0, {
                        'name': _('Interest of Installment No. %s of %s') % (install.install_no,install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': debit_account_id,
                        'journal_id': install.bank_journal_id.id,
                        'debit': install.interest_amt,
                        'credit': 0.0,
                    })
                credit_line = (0, 0, {
                        'name': _('Interest of Installment No. %s of %s') % (install.install_no,install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': credit_account_id,
                        'journal_id':  install.bank_journal_id.id,
                        'debit': 0.0,
                        'credit':install.interest_amt,
                    })
                move.update({'line_ids': [debit_line, credit_line]})
                move_id = move_pool.create(move)
                date_from = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
                if not install.date_from:
                    vals.update(int_move_id=move_id.id, date_from=date_from)
                else:
                    vals.update(int_move_id=move_id.id)
                install.write(vals)
        return True
    
    @api.multi
    def action_pay_installment(self):
        move_pool = self.env['account.move']  
        for install in self:
            vals = {}
            
            timenow = time.strftime('%Y-%m-%d')
            address_id = install.partner_id or False
            partner_id = address_id and address_id and address_id.id or False
            
            if not partner_id:
                raise Warning(_('Please configure Home Address On partner.')) 
            
            move = {
                'narration': install.name,
                'date': install.date_from,
                'ref': install.name,
                'journal_id': install.bank_journal_id.id,
            }
            move_principle = {
                'narration': install.name,
                'date': install.date_from,
                'ref': install.name,
                'journal_id': install.bank_journal_id.id,
            }

            if not install.bank_journal_id:
                raise Warning(_('Please configure Bank Journal.'))
                
            if install.interest_amt == 0.0:
                credit_account_id = install.loan_id.partner_loan_account.id or False
                debit_account_id = install.bank_account_id.id or False
                if not credit_account_id:
                    raise Warning(_('Please configure Debit/Credit accounts on the Journal %s ') % (install.bank_journal_id.name))
                if not debit_account_id:
                    raise Warning(_('Please configure debit account of partner'))
                debit_line = (0, 0, {
                        'name': _('Installment of %s') % (install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': debit_account_id,
                        'journal_id': install.bank_journal_id.id,
                        'debit': install.total,
                        'credit': 0.0,
                    })
                credit_line = (0, 0, {
                        'name': _('Installment of %s') % (install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': credit_account_id,
                        'journal_id':  install.bank_journal_id.id,
                        'debit': 0.0,
                        'credit':install.total,
                    })
                    
            if install.interest_amt > 0.0:
                debit_account_id = install.bank_account_id.id or False
                credit_account_id = install.loan_id.partner_loan_account.id or False
                if not credit_account_id:
                    raise Warning(_('Please configure Debit/Credit accounts on the Journal %s ') % (install.bank_journal_id.name))
                if not debit_account_id:
                    raise Warning(_('Please configure debit account of partner'))
                    
                debit_line = (0, 0, {
                        'name': _('Installment of %s') % (install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': debit_account_id,
                        'journal_id': install.bank_journal_id.id,
                        'debit': install.total,
                        'credit': 0.0,
                    })
                credit_line = (0, 0, {
                        'name': _('Installment of %s') % (install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': credit_account_id,
                        'journal_id':  install.bank_journal_id.id,
                        'debit': 0.0,
                        'credit':install.total,
                    })
                    
                total_debit_account_id = install.loan_id.partner_loan_account.id
                total_credit_account_id = install.loan_id.interest_receivable_account_id.id
                
                total_debit_line = (0, 0, {
                        'name': _('Interest of Installment No. %s of %s') % (install.install_no,install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': total_debit_account_id,
                        'journal_id': install.bank_journal_id.id,
                        'debit': install.interest_amt,
                        'credit': 0.0,
                    })
                total_credit_line = (0, 0, {
                        'name': _('Interest of Installment No. %s of %s') % (install.install_no,install.loan_id.name),
                        'date': install.date_from,
                        'partner_id': partner_id,
                        'account_id': total_credit_account_id,
                        'journal_id':  install.bank_journal_id.id,
                        'debit': 0.0,
                        'credit':install.interest_amt,
                    })
                move_principle.update({'line_ids' : [total_debit_line, total_credit_line]})
                total_move_id = move_pool.create(move_principle)
                if not install.date_from:
                    vals.update(move_id=total_move_id.id)
                else:
                    vals.update(move_id=total_move_id.id)
                    
            move.update({'line_ids': [debit_line, credit_line]})
            move_id = move_pool.create(move)
            date_from = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
            
            if not install.date_from:
                vals.update(state='paid', total_amt_move_id=move_id.id, date_from=date_from)
            else:
                vals.update(state='paid', total_amt_move_id=move_id.id)
            install.write(vals)
        return True
