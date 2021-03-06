# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011 ChriCar Beteiligungs- und Beratungs- GmbH (<http://www.camptocamp.com>).
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
import openerp.addons.one2many_sorted as one2many_sorted

#----------------------------------------------------------
#  Company
#----------------------------------------------------------

class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        
        'print_ean' : fields.boolean( string="Print EAN on documents"),
    }
    _defaults = {
        'print_ean': lambda *a: True,
    }

res_company()



class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def _print_uom(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
          print_uom = False
          if picking.move_lines:
            for line in picking.move_lines:
                if not line.product_uos or line.product_uos and line.product_uom != line.product_uos:
                   print_uom = True
          res[picking.id] =  print_uom
        return res

    def _print_uos(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
          print_uos = False
          if picking.move_lines:
            for line in picking.move_lines:
                if line.product_uos:
                   print_uos = True
          res[picking.id] =  print_uos
        return res


    def _print_packing(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
          print_packing = False
          if picking.move_lines:
            for line in picking.move_lines:
                if line.product_packaging:
                   print_packing = True
          res[picking.id] =  print_packing
        return res

    def _print_ean(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
          print_ean = False
          if picking.company_id.print_ean and picking.move_lines:
            for line in picking.move_lines:
                if line.product_id.ean13 or line.product_packaging.ean:
                   print_ean = True
          res[picking.id] =  print_ean
        return res

    def _print_lot(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
          print_lot = False
          if picking.move_lines:
            for line in picking.move_lines:
                if line.prodlot_id: 
                   print_lot = True
          res[picking.id] =  print_lot
        return res
        
    def _print_code(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
          print_code = False
          if picking.move_lines and 'print_code' in picking.company_id._columns and picking.company_id.print_code:
            for line in picking.move_lines:
                if line.product_id.default_code:
                   print_code = True
          res[picking.id] =  print_code
        return res

    def _get_cols(self, cr, uid, ids, name, args, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
          cols = 2
          if order.print_uom:
             cols += 2
          if order.print_uos:
             cols += 2
          if order.print_packing:
             cols += 2
          if order.print_ean:
             cols += 1
          if order.print_lot:
             cols += 1
          if order.print_code:
             cols += 1

          res[order.id] = cols

        return res

    def _get_packs(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids, context=context):
          packs = 0
          if picking.move_lines:
            for line in picking.move_lines:
                if 'price_unit_id' in self._columns and  line.product_packaging and line.product_packaging.qty:
                    packs += line.product_qty/line.product_packaging.qty 
          res[picking.id] = packs  
        return res
        
    _columns = {
              'print_uom': fields.function(_print_uom, method=True, type='boolean', string='Print UoM if different from UoS',),
              'print_uos': fields.function(_print_uos, method=True, type='boolean', string='Print UoS if exists',),
              'print_packing': fields.function(_print_packing, method=True, type='boolean', string='Print Packing Info if available',),
              'print_ean': fields.function(_print_ean, method=True, type='boolean', string='Print EAN if available',),
              'print_lot': fields.function(_print_lot, method=True, type='boolean', string='Print lot if available',),
              'print_code': fields.function(_print_code, method=True, type='boolean', string='Print code if available',),
              'cols': fields.function(_get_cols, method=True, type='integer', string='No of columns before totals',),
              'number_of_packages_computed': fields.function(_get_packs, method=True, type='float', string='Number of Packages'),
              'move_lines_sorted' : one2many_sorted.one2many_sorted
              ( 'stock.move'
              , 'picking_id'
              , 'Internal Moves Sorted'
              , states={'draft': [('readonly', False)]}
              , order  = 'product_id.name'
              )
              
    }
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        default.update({'move_lines_sorted': []})
        return super(stock_picking, self).copy(cr, uid, id, default, context=context)

stock_picking()

class stock_picking_out(osv.osv):
    _inherit = "stock.picking"

stock_picking_out()
