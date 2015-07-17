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


class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def action_button_split_line(self, cr, uid, ids, context=None):
        context = context or {}
        prod_obj = self.pool.get('product.product')
        line = self.browse(cr, uid, ids, context=context)
        prod_ids = prod_obj.search(cr, uid, [('product_tmpl_id','=',line.product_id.product_tmpl_id.id)])
        for prod_id in prod_ids:
            if not prod_id == line.product_id.id:
                context_partner = {'lang': line.order_id.partner_id.lang, 'partner_id': line.order_id.partner_id.id}
                name = self.pool.get('product.product').name_get(cr, uid, [prod_id], context=context_partner)[0][1]
                if line.product_id.product_tmpl_id.description_sale:
                    name += '\n'+line.product_id.product_tmpl_id.description_sale
                default = {'product_id': prod_id,
#                            'to_split': False,
                           'name': name,
                           'product_uom_qty': 0.0,
                           'product_uos_qty': 0.0,
                           }
                self.copy(cr, uid, line.id, default=default, context=context)
        return True
