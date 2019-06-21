# -*- coding: utf-8 -*-
# Copyright 2019 Chafique Delli <chafique.delli@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP Production Request Procurement Analytic',
    'description': 'This module sets analytic account in mrp production of '
                   ' mrp request from procurement analytic account',
    'version': '10.0.1.0.0',
    'category': 'Analytic',
    'license': 'AGPL-3',
    'author': "Akretion, "
              "Odoo Community Association (OCA)",
    'website': 'http://www.github.com/oca/manufacture',
    'depends': [
        'mrp_production_request',
        'procurement_analytic',
    ],
    'installable': True,
}
