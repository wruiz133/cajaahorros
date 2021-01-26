# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrPayslipEmployees(models.TransientModel):
    _name = 'aporte.list.test'
    _description = 'Generate aports for all selected partners'

    partner_ids = fields.Many2many('res.partner', column1='test_id', column2='partner_id', string='Partners')

    #employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees')

    @api.multi
    def compute_sheet(self):
        #payslips = self.env['loan.aportaciones']
        [data] = self.read() #seleccion de registros de este modelo aporte.list.test
        active_id = self.env.context.get('active_id')  #registro desde donde llamo al wizard modelo cartera.aportes.test
        #obtiene datos del registro llamador en funcion de su active_id
        if active_id:
            [run_data] = self.env['cartera.aportes.test'].browse(active_id).read(['date_start', 'date_end', 'credit_amount'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        credit_mount = run_data.get('credit_amount')
        #mes = (datetime.strptime(from_date, '%Y-%m-%d').month)
        #((datetime.strptime('cliente_id.fecha.id', '%Y-%m-%d').month) '=' mes)
        #date_from = fields.Datetime.to_string(from_date)
        #date_to = fields.Datetime.to_string(to_date)
        #print("mes:  ", mes)
        #verifica seleccionados fecha
        if not data['partner_ids']:
            raise UserError(_("You must select partner(s) to generate pay(s)."))
        #recorre los seleccionados sobre la base partners

        for employee in self.env['res.partner'].browse(data['partner_ids']): #selecciona solo marcados
            #('(datetime.strptime(cliente_id.fecha.id, '%Y-%m-%d').month)','=',mes)
            #itera para loan.aportaciones dentro del rango de fecha de cartera.aportes.test
            slip_data = self.env['loan.aportaciones'].search([('cliente_id.id','=', employee.id),('fecha','>=',from_date),('fecha','<=',to_date)])   #.onchange_partner_id(employee.id)
            #crea y actualiza registro dependiendo de si esta o no dentro de la carga del periodo
            slip_data_no = self.env['loan.noaporta']
            print "verificador  ",slip_data.id
            if slip_data.id in (False,None):
                print "entre ...aqui"
                no_apor ={
                    'noaporta_id':active_id,
                    'cliente_id': employee.id,
                    'monto_aportacion': credit_mount,
                    'fechai': from_date,
                    'fechaf': to_date,
                    'state': 'nopay',
                }
                slip_data_no.create(no_apor)
            else:
                apor = {
                    #'cliente_id': employee.id,
                    #'monto_aportacion': 35, # slip_data['value'].get('monto_aportacion'),
                    'state': 'Pay', #employee.state,
                    #'name': cont, #employee.id,
                    #'tipo_aportacion': 'aportacion', #slip_data['value'].get('tipo_aportacion'),
                    #'journal_id': 388,#slip_data['value'].get('journal_id'),
                    #'payslip_run_id': active_id,
                    #'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                    #'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                    #'fecha': from_date,
                    #'credit_note': run_data.get('credit_note'),
                    #'company_id': employee.company_id.id,
                }
                slip_data.write(apor)
        #payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}
