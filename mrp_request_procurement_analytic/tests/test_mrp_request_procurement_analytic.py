# -*- coding: utf-8 -*-

from odoo.tests import common


class TestMrpRequestProcurementAnalytic(common.SavepointCase):
    """Use case : Prepare some data for current test case"""

    @classmethod
    def setUpClass(cls):
        super(TestMrpRequestProcurementAnalytic, cls).setUpClass()

        cls.product = cls.env.ref('product.product_product_8')
        cls.product.write({'mrp_production_request': True})
        cls.analytic_account = cls.env['account.analytic.account'].create({
            'name': 'Test Analytic Account',
        })
        cls.manufacture_rule = cls.env['procurement.rule'].search([
            ('action', '=', 'manufacture'),
            ('warehouse_id', '=', cls.env.ref('stock.warehouse0').id)])
        procur_vals = {
            'name': 'Procurement test',
            'product_id': cls.product.id,
            'product_uom': cls.product.uom_id.id,
            'warehouse_id': cls.env.ref('stock.warehouse0').id,
            'rule_id': cls.manufacture_rule.id,
            'product_qty': 1.0,
            'account_analytic_id': cls.analytic_account.id,
        }
        cls.procurement = cls.env['procurement.order'].create(procur_vals)

    def test_procurement_to_mrp_request(self):
        # Run procurement
        self.procurement.run()
        request_lines = self.procurement.mrp_production_request_id.\
            mrp_production_ids
        self.assertTrue(request_lines)
        # Make sure that request line have analytic account
        self.assertEqual(
            request_lines[0].analytic_account_id.id,
            self.analytic_account.id)
