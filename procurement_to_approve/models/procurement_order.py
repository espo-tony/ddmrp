# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.multi
    @api.depends("purchase_id")
    def _compute_to_approve(self):
        for rec in self:
            if rec.state in ['draft', 'exception']:
                rec.to_approve = True
            if rec.state not in ['cancel', 'done'] \
                    and rec.purchase_id \
                    and rec.purchase_id.state == 'draft':
                rec.to_approve = True

    def _search_to_approve(self, operator, value):
        if operator == '=':
            return ['|', ('state', 'in', ['draft', 'exception']),
                    ('purchase_id.state', '=', 'draft')]
        else:
            raise NotImplementedError(
                'Search operator %s not implemented for value %s'
                % (operator, value)
            )

    to_approve = fields.Boolean(string="To approve",
                                compute="_compute_to_approve",
                                search='_search_to_approve',
                                default=False)
