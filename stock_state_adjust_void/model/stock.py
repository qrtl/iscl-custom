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
        'state': fields.selection([('draft', 'New'),
                                   ('cancel', 'Cancelled'),
                                   ('waiting', 'Waiting Another Move'),
                                   ('confirmed', 'Waiting Availability'),
                                   ('assigned', 'Available'),
                                   ('dispatched', 'Dispatched'),
                                   ('done', 'Done'),
                                   ], 'Status', readonly=True, select=True, copy=False,
                 help= "* New: When the stock move is created and not yet confirmed.\n"\
                       "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"\
                       "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to me manufactured...\n"\
                       "* Available: When products are reserved, it is set to \'Available\'.\n"\
                       "* Dispatched: products are dispatched for internal transfer and waiting to be received by the destination location.\n"\
                       "* Done: When the shipment is processed, the state is \'Done\'."),
    }


class stock_picking(osv.osv):
    _inherit = "stock.picking"


    def action_dispatch(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('stock.move')
        move_ids = move_obj.search(cr, uid, [('picking_id','in',ids)], context=context)
        if move_ids:
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                if move.state == 'assigned':
                    move_obj.write(cr, uid, [move.id], {'state': 'dispatched'}, context=context)


#     @api.cr_uid_ids_context
#     def do_unreserve(self, cr, uid, move_ids, context=None):
#         quant_obj = self.pool.get("stock.quant")
#         for move in self.browse(cr, uid, move_ids, context=context):
#             if move.state in ('done', 'cancel'):
#                 raise osv.except_osv(_('Operation Forbidden!'), _('Cannot unreserve a done move'))
#             quant_obj.quants_unreserve(cr, uid, move, context=context)
#             if self.find_move_ancestors(cr, uid, move, context=context):
#                 self.write(cr, uid, [move.id], {'state': 'waiting'}, context=context)
#             else:
#                 self.write(cr, uid, [move.id], {'state': 'confirmed'}, context=context)



    def _state_get(self, cr, uid, ids, field_name, arg, context=None):
        '''The state of a picking depends on the state of its related stock.move
            draft: the picking has no line or any one of the lines is draft
            done, draft, cancel: all lines are done / draft / cancel
            confirmed, waiting, assigned, partially_available depends on move_type (all at once or partial)
        '''
        res = {}
        for pick in self.browse(cr, uid, ids, context=context):
            if (not pick.move_lines) or any([x.state == 'draft' for x in pick.move_lines]):
                res[pick.id] = 'draft'
                continue
            if all([x.state == 'cancel' for x in pick.move_lines]):
                res[pick.id] = 'cancel'
                continue
            if all([x.state in ('cancel', 'done') for x in pick.move_lines]):
                res[pick.id] = 'done'
                continue

            order = {'confirmed': 0, 'waiting': 1, 'assigned': 2, 'dispatched': 3}
            order_inv = {0: 'confirmed', 1: 'waiting', 2: 'assigned', 3: 'dispatched'}
            lst = [order[x.state] for x in pick.move_lines if x.state not in ('cancel', 'done')]
            if pick.move_type == 'one':
                res[pick.id] = order_inv[min(lst)]
            else:
                #we are in the case of partial delivery, so if all move are assigned, picking
                #should be assign too, else if one of the move is assigned, or partially available, picking should be
                #in partially available state, otherwise, picking is in waiting or confirmed state
                res[pick.id] = order_inv[max(lst)]
                if not all(x == 2 for x in lst):
                    if any(x == 2 for x in lst):
                        res[pick.id] = 'partially_available'
                    else:
                        #if all moves aren't assigned, check if we have one product partially available
                        for move in pick.move_lines:
                            if move.partially_available:
                                res[pick.id] = 'partially_available'
                                break
        return res

    def _get_pickings(self, cr, uid, ids, context=None):
        res = set()
        for move in self.browse(cr, uid, ids, context=context):
            if move.picking_id:
                res.add(move.picking_id.id)
        return list(res)

    _columns = {
        'state': fields.function(_state_get, type="selection", copy=False,
            store={
                'stock.picking': (lambda self, cr, uid, ids, ctx: ids, ['move_type'], 20),
                'stock.move': (_get_pickings, ['state', 'picking_id', 'partially_available'], 20)},
            selection=[
                ('draft', 'Draft'),
                ('cancel', 'Cancelled'),
                ('waiting', 'Waiting Another Operation'),
                ('confirmed', 'Waiting Availability'),
                ('partially_available', 'Partially Available'),
                ('assigned', 'Ready to Transfer'),
                ('dispatched', 'Dispatched'),
                ('done', 'Transferred'),
                ], string='Status', readonly=True, select=True, track_visibility='onchange',
            help="""
                * Draft: not confirmed yet and will not be scheduled until confirmed\n
                * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n
                * Waiting Availability: still waiting for the availability of products\n
                * Partially Available: some products are available and reserved\n
                * Ready to Transfer: products reserved, simply waiting for confirmation.\n
                * Dispatched: has been dispatched for internal transfer and is waiting to be received by the destination location.\n
                * Transferred: has been processed, can't be modified or cancelled anymore\n
                * Cancelled: has been cancelled, can't be confirmed anymore"""
        ),
    }

