# -*- coding: utf-8 -*-
{
    'name': 'Payment Provider: EuPlătesc.ro (placeholder)',
    'version': '19.0.1.0.3',
    'category': 'Accounting/Payment Providers',
    'sequence': 360,
    'summary': 'EuPlătesc.ro payment provider entry for backend / API-recorded transactions.',
    'description': 'Adds a EuPlătesc.ro provider without live payment processing or API credentials.',
    'depends': ['payment', 'account_payment', 'sale'],
    'data': [
        'data/payment_provider_data.xml',
        'data/payment_provider_kanban_image.xml',
        'views/payment_provider_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'author': 'OdooROTest',
    'license': 'LGPL-3',
}
