# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Rooms For (Hong Kong) Limited (<http://www.openerp-asia.net>).
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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class product_template(osv.osv):
    _inherit = "product.template"
    _columns = {
#         'name_furigana': fields.char('Furigana', select=True),
#         'packaging': fields.many2one('product.packaging.unit', 'Packaging'),
        'brand': fields.many2one('product.brand', 'Brand'),
#         'shipping_method': fields.selection([('regular','Regular'),('cool','Cool'),('frozen','Frozen')], 'Shipping Method'),
#         'display_stock': fields.integer('Display Stock'),
#         'ship_height': fields.float('Shipping Height'),
#         'ship_width': fields.float('Shipping Width'),
#         'ship_length': fields.float('Shipping Length'),
#         'ingredients': fields.text('Materials/Ingredients', translate=True),
#         'salt_percent': fields.float('Salt %'),
        'prod_type_ids': fields.many2many('product.prod.type', id1='product_id', id2='prod_type_id', string='Product Type'),
#         'designer_ids': fields.many2many('product.designer', id1='product_id', id2='designer_id', string='Designer'),
#         'manufacture_country': fields.many2one('res.country', 'Manufacture Country', ondelete='restrict'),
#         'alcohol_percent': fields.float('Alcohol %'),
#         'buyer': fields.many2one('res.partner', 'Buyer', domain=[('is_company','=',False)]),
#         'buyer_commission': fields.float('Buyer Commission'),
    }

class product_brand(osv.osv):
    _name = 'product.brand'
    _description = 'Brand'
    _columns = {
        'name': fields.char('Name', required=True, translate=True),
    }
    _sql_constraints = [
        ('name_uniq', 'unique (name)','The name must be unique.')]

class product_prod_type(osv.osv):
    _name = 'product.prod.type'
    _description = 'Product Type'
    _columns = {
        'name': fields.char('Name', required=True, translate=True),
        'product_ids': fields.many2many('product.template', id1='prod_type_id', id2='product_id', string='Products'),
    }
    _sql_constraints = [
        ('name_uniq', 'unique (name)','The name must be unique.')]
