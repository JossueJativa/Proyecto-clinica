{
    'name': 'Medical Documents Integration',
    'version': '17.0.1.0.0',
    'category': 'Healthcare',
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
        'views/nextcloud_config_views.xml',
        'data/nextcloud_config_data.xml',
    ],
    'external_dependencies': {
        'python': ['requests'],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
