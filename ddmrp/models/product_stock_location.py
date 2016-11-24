# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp

UNIT = dp.get_precision('Product Unit of Measure')


class ProductStockLocation(models.Model):
    _inherit = 'product.stock.location'

    @api.multi
    @api.depends('quant_ids',
                 'quant_ids.location_id',
                 'quant_ids.product_id',
                 'quant_ids.qty')
    def _compute_product_available_qty(self):
        super(ProductStockLocation, self)._compute_product_available_qty()
        for rec in self:
            product_available = rec.product_id.with_context(
                location=rec.location_id.id
            )._product_available()[rec.product_id.id]
            rec.product_location_qty_available_not_res = product_available[
                'qty_available_not_res']

    product_location_qty_available_not_res = fields.Float(
        string='Quantity On Location (Unreserved)', digits=UNIT,
        compute='_compute_product_available_qty', store=True)