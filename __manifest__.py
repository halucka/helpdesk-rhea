# -*- coding: utf-8 -*-
{
    'name': "helpdesk_rhea",

    'summary': """
        Module for helpdesk with prepaid service
    """,

    'description': """
        This module provides connection between Helpdesk, Timesheets and Project management apps.
    """,

    'author': "BeOpen NV",
    'website': "http://www.beopen.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'project', 'helpdesk', 'hr_timesheet', 'report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/helpdesk_budget.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/helpdesk_rhea_reports.xml',
        'report/helpdesk_activity.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
}