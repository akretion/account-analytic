# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

# deal with account_analytic_id in advance payments
class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment"

    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account"
    )
    analytic_tag_ids = fields.Many2many("account.analytic.tag", string="Analytic Tags")

    @api.model
    def default_get(self, fields):
        rec = super().default_get(fields)
        active_ids = self._context.get("active_ids")
        inv = self.env["account.invoice"].browse(active_ids)
        if len(inv) == 1:
            rec.update(
                {
                    "analytic_account_id": inv.account_analytic_id.id,
                    "analytic_tag_ids": [(6, 0, inv.analytic_tag_ids.ids)],
                }
            )
        else:
            # TODO
            pass
        return rec


class account_payment(models.Model):
    _inherit = "account.payment"

    def _get_shared_move_line_vals(
        self, debit, credit, amount_currency, move_id, invoice_id=False
    ):
        """ Override native function creating payment's account.move.line values"""
        res = super()._get_shared_move_line_vals(
            debit, credit, amount_currency, move_id, invoice_id=False
        )

        res.update(
            {
                "analytic_account_id": self.analytic_account_id.id,
                "analytic_tag_ids": [(6, 0, self.analytic_tag_ids.ids)],
            }
        )
        return res
