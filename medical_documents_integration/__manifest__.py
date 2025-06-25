{
    'name': 'Medical Documents Integration',
    'version': '17.0.1.0.0',
    'category': 'Healthcare',
    'license': 'LGPL-3',
    'summary': 'Integration with Nextcloud for automatic document storage',
    'description': '''
        This module provides automatic integration between Odoo and Nextcloud
        for storing medical documents such as invoices, prescriptions, and reports.
        
        Features:
        - Automatic PDF upload to Nextcloud via WebDAV
        - Document organization by patient and type
        - Integration hooks for invoice and report generation
    ''',
    'author': 'UDLA Integration Project',
    'website': 'https://udla.edu.ec',
    'depends': ['base', 'account', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/nextcloud_config_data.xml',
        'views/nextcloud_config_views.xml',
        # Las vistas de facturas se cargan después
        # 'views/invoice_nextcloud_views.xml',
    ],
    'external_dependencies': {
        'python': ['requests'],
    },
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
    'application': False,
}
