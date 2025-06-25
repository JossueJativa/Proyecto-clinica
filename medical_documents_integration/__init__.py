# -*- coding: utf-8 -*-

from . import models
from . import services
from . import hooks

def post_init_hook(env):
    """Hook ejecutado después de la instalación del módulo"""
    try:
        # Verificar que los campos se hayan creado correctamente
        env['account.move']._fields.get('nextcloud_uploaded')
        env['account.move']._fields.get('nextcloud_url')
        
        # Configurar configuración por defecto si no existe
        config = env['nextcloud.config'].search([('active', '=', True)], limit=1)
        if not config:
            env['nextcloud.config'].create({
                'name': 'Configuración por defecto',
                'url': 'http://nextcloud:80',
                'username': 'admin',
                'password': 'admin',
                'active': True
            })
            
    except Exception as e:
        import logging
        _logger = logging.getLogger(__name__)
        _logger.warning(f"Error en post_init_hook: {str(e)}")
