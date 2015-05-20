# -*- coding: utf-8 -*-
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved
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

{
    'name': 'Stock State Adjust',
    'category': 'Stock',
    'version': '0.5',
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'www.openerp-asia.net',
    'depends': ['stock',
                ],
    'summary':"""""",
    'description': """ 
Overview:
---------
- Adds a state 'Dispatched' in between 'Ready to Transfer' and 'Transferred'.
    """,
    'data': [
             'view/stock_view.xml',
             ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
