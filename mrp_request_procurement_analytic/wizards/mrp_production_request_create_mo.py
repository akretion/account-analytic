# -*- coding: utf-8 -*-

from odoo import api, models


class MrpProductionRequestCreateMo(models.TransientModel):
    _inherit = 'mrp.production.request.create.mo'

    @api.multi
    def _prepare_manufacturing_order(self):
        vals = super(
            MrpProductionRequestCreateMo, self)._prepare_manufacturing_order()
        vals['analytic_account_id'] = self.mrp_production_request_id.\
            procurement_id.account_analytic_id.id or False
        return vals
