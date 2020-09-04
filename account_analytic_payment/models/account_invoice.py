# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    account_analytic_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account"
    )
    analytic_tag_ids = fields.Many2many("account.analytic.tag", string="Analytic Tags")

    common_analytic_account = fields.Boolean(
        string="Common Analytic Account",
        help="Uncheck if you want to define distinct Analytic Accounts "
        "for each Invoice line",
        default=True,
    )

    @api.onchange("invoice_line_ids", "account_analytic_id", "analytic_tag_ids")
    def _propagate_analytic_account(self):
        for inv in self:
            if inv.common_analytic_account:
                for line in inv.invoice_line_ids:
                    line.update(
                        {
                            "account_analytic_id": inv.account_analytic_id.id,
                            "analytic_tag_ids": [(6, 0, inv.analytic_tag_ids.ids)],
                        }
                    )
            else:
                inv.account_analytic_id = False
                inv.analytic_tag_ids = [(5, 0,0)]

    # TODO: Check if need to propagate also for invoice tax analytic account
