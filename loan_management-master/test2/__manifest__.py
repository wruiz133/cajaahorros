# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2017 David J. Romero C.
#    (<http://www.htccomputer.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'test2 ',
    'version': '10.0.0.1.0',
    'author': "David Jacobo Romero Calderon...",
    'maintainer': 'HTC Computer Lab',
    'website': 'http://www.htccomputer.com',
    'license': 'AGPL-3',
    'category': 's',
    'summary': ' s_test2 de categoria s, by HTC.',
    'depends': ['base','account'],
    'description': """
Modulo 
TEST2""",
    'demo': [],
    'test': [],
    'data': [
'views/apactivosfijos_view.xml',
'views/apcomprasorden_view.xml',
'views/apactivosfijosordenmov_view.xml',
'views/apactivosfijoshistor_view.xml',
'views/adjuntos_view.xml',
'views/apactivosfijosordenmovdetalle_view.xml',
#'security/test2_security.xml',
#'security/ir.model.access.csv',
],
    'installable': True,
    'auto_install': False,
}
