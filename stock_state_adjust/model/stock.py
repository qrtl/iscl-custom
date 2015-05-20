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

from openerp.osv import fields, osv
from openerp.tools.translate import _


class stock_move(osv.osv):
    _inherit = "stock.move"
    
    _columns = {
        'dispatched': fields.boolean('Dispatched',
            help="""
            Indicates that the product has been dispatched for internal transfer and waiting to be received by the destination location.
            """
        )
    }


class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def action_dispatch(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('stock.move')
        move_ids = move_obj.search(cr, uid, [('picking_id','in',ids),('state','=','assigned'),('dispatched','=',False)], context=context)
        if move_ids:
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                move_obj.write(cr, uid, [move.id], {'dispatched': True}, context=context)
            self.write(cr, uid, ids, {'dispatched': True}, context=context)

    def _get_ok_to_transfer(self, cr, uid, ids, name, args, context=None):
        res = {}
        for p in self.browse(cr, uid, ids, context=context):
            res[p.id] = False
            if p.state in ['assigned', 'partially_available']:
                if p.picking_type_code != 'internal':
                    res[p.id] = True
                elif p.dispatched == True:
                    res[p.id] = True 
        return res

    _columns = {
        'dispatched': fields.boolean('Dispatched',
            help="""
            Indicates that the products have been dispatched for internal transfer and waiting to be received by the destination location.
            """),
        'ok_to_transfer': fields.function(_get_ok_to_transfer, type='boolean', string='OK to Transfer',
              store={
                  'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['state', 'dispatched'], 10),}),
    }
