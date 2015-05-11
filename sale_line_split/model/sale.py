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


class sale_order(osv.osv):
    _inherit = "sale.order"

    def action_button_split_line(self, cr, uid, ids, context=None):
        context = context or {}
        for sale in self.browse(cr, uid, ids, context=context):
            if not sale.order_line:
                raise osv.except_osv(_('Error!'),_('You cannot split a sales order which has no line.'))
            for line in sale.order_line:
                if line.to_split:
                    prod_obj = self.pool.get('product.product')
                    prod_ids = prod_obj.search(cr, uid, [('product_tmpl_id','=',line.product_id.product_tmpl_id.id)])
                    for prod_id in prod_ids:
                        if not prod_id == line.product_id:
                            default = {'product_id': prod_id,
                                       'to_split': False,
                                       'product_uom_qty': 0.0,
                                       'product_uos_qty': 0.0,
                                       }
                            sale_line_id = self.pool.get('sale.order.line').\
                                copy(cr, uid, line.id, default=default, context=context)
                    self.pool.get('sale.order.line').write(cr, uid, [line.id],
                        {'to_split': False}, context=context)
        return True


class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    _columns = {
        'to_split': fields.boolean('To Split'),
    }

