# -*- coding: utf-8 -*-

from odoo.tests import common


class TestMrpRequestProcurementAnalytic(common.SavepointCase):
    """Use case : Prepare some data for current test case"""

    @classmethod
    def setUpClass(cls):
        super(TestMrpRequestProcurementAnalytic, cls).setUpClass()
        cls.wiz_model = cls.env['mrp.production.request.create.mo']
        cls.product = cls.env.ref('mrp.product_product_19')
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
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'rule_id': cls.manufacture_rule.id,
            'product_qty': 1.0,
            'account_analytic_id': cls.analytic_account.id,
        }
        import ipdb
        ipdb.set_trace()
        cls.procurement = cls.env['procurement.order'].create(procur_vals)

    def test_procurement_to_mrp_request(self):
        # Run procurement
        self.procurement.run()
        request = self.procurement.mrp_production_request_id
        request.button_to_approve()
        request.button_draft()
        request.button_to_approve()
        request.button_approved()
        wiz = self.wiz_model.with_context(active_ids=request.ids).create({})
        wiz.compute_product_line_ids()
        wiz.mo_qty = 1
        wiz.create_mo()

        request_lines = request.mrp_production_ids
        self.assertTrue(request_lines)
        # Make sure that request line have analytic account
        self.assertEqual(
            request_lines[0].analytic_account_id.id,
            self.analytic_account.id)
