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
        invoices = self.env["account.invoice"].browse(active_ids)

        aa_ids = self.env["account.analytic.account"]
        atag_ids = self.env["account.analytic.tag"]
        for inv in invoices:
            aa_ids |= inv.invoice_line_ids.mapped("account_analytic_id")
            atag_ids |= inv.invoice_line_ids.mapped("analytic_tag_ids")
        if len(aa_ids) == 1:
            rec.update(
                {
                    "analytic_account_id": aa_ids.id,
                    "analytic_tag_ids": [(6, 0, atag_ids.ids)],
                }
            )
        elif len(aa_ids) > 1:
            # TODO Warning "Many analytic account for 1 payment : Continue or Cancel"
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
