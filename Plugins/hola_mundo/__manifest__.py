# hello_world/__manifest__.py
{
    'name': 'Hello World',
    'version': '1.0',
    'summary': 'Primer módulo de ejemplo',
    'category': 'Tools',
    'author': 'Jossue Játiva',
    'depends': ['base'],
    'data': [
        'views/hello_view.xml',
    ],
    'installable': True,
    'application': True,
}
