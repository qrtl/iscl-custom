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


class StockMove(models.Model):
    _inherit = 'stock.move'
 
    dispatched = fields.Boolean(
        string='Dispatched', copy=False)

    @api.cr_uid_ids_context
    def do_unreserve(self, cr, uid, move_ids, context=None):
        res = super(StockMove, self).do_unreserve(cr, uid, move_ids, context)
        for move in self.browse(cr, uid, move_ids, context=context):
            if self.find_move_ancestors(cr, uid, move, context=context):
                self.write(cr, uid, [move.id], {'dispatched': False}, context=context)
            else:
                self.write(cr, uid, [move.id], {'dispatched': False}, context=context)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _track = {
        'state': {
            'stock_state_adjust.mt_pick_cancelled': lambda self, cr, uid, obj, ctx=None: obj.state == 'cancel',
            'stock_state_adjust.mt_pick_confirmed': lambda self, cr, uid, obj, ctx=None: obj.state == 'confirmed',
        },
    }
 
    dispatched = fields.Boolean(compute='_update_dispatched', store=True, string='Dispatched')
    ok_to_transfer = fields.Boolean(compute='_get_ok_to_transfer', store=True, string='OK to Transfer')

    @api.one
    def action_dispatch(self):
        Move = self.env['stock.move']
        moves = Move.search([('picking_id','=',self.id),('state','=','assigned')])
        if moves:
            moves.write({'dispatched': True})
#             self.write({'dispatched': True})
 
    @api.one
    @api.depends('state', 'move_lines.dispatched')
    def _update_dispatched(self):
#         if self.state not in ['assigned', 'partially_available']:
        if self.state in ['assigned', 'partially_available']:
            self.dispatched = False
            Move = self.env['stock.move']
            moves = Move.search([('picking_id','=',self.id)])
            if moves:
                for m in moves:
                    self.dispatched = m.dispatched
#                     m.write({'dispatched': False})
 
    @api.one
    @api.depends('dispatched', 'state')
    def _get_ok_to_transfer(self):
        self.ok_to_transfer = False
        if self.state in ['assigned', 'partially_available']:
            if self.picking_type_code != 'internal':
                self.ok_to_transfer = True
            elif self.dispatched == True:
                self.ok_to_transfer = True 

    @api.one
    def action_set_to_draft(self):
        Move = self.env['stock.move']
        moves = Move.search([('picking_id','=',self.id),('state','=','cancel')])
        if moves:
            moves.write({'state': 'draft'})
