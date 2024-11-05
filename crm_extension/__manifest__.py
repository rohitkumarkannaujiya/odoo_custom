# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'CRM Lead',
    'version': '17.0.0.1',
    'summary': 'CRM Lead Services',
    'author': 'Apagen Solution Pvt. Ltd',
    'website': 'https://www.apagen.com',
    'description': """
====================
    """,
    'depends': ['base',
                'product',
                'mail',
               'crm',
               'sale',
               'sales_team',
               'sale_crm',
               'sale_subscription'
            ],
 
    'data': [ 
             'security/product_pricelist_security.xml',
             'security/ir.model.access.csv',
             'report/ir_actions_report_templates.xml',
             'views/crm_lead_inherit_view.xml',
             'views/sale_order_inherit_view.xml',
             'views/term_condition_view.xml',
             'views/sale_subscription_action_inherit.xml',
             'views/business_potential_line_view.xml',
           ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
