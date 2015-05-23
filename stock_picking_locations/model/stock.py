# -*- coding: utf-8 -*-
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG
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

from openerp import models, fields, api, _


# class StockMove(models.Model):
#     _inherit = 'stock.move'
#  
#     dispatched = fields.Boolean(
#         string='Dispatched', copy=False)



class StockPicking(models.Model):
    _inherit = 'stock.picking'
 
    location_id = fields.Many2one('stock.location', related='move_lines.location_id', string='Source Location', readonly=False)
    location_dest_id = fields.Many2one('stock.location', related='move_lines.location_dest_id', string='Source Location', readonly=False, select=True)
#         'location_id': fields.related('move_lines', 'location_id', type='many2one', relation='stock.location', string='Location', readonly=True),
#         'location_dest_id': fields.related('move_lines', 'location_dest_id', type='many2one', relation='stock.location', string='Destination Location', readonly=True),

