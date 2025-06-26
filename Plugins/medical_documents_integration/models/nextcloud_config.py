# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..services.nextcloud_webdav import NextcloudWebDAVClient
import logging

_logger = logging.getLogger(__name__)

class NextcloudConfig(models.Model):
    _name = 'nextcloud.config'
    _description = 'Configuración de Nextcloud'
    _rec_name = 'name'
    
    name = fields.Char('Nombre', required=True, default='Configuración Nextcloud')
    url = fields.Char('URL de Nextcloud', required=True, default='http://nextcloud:80')
    username = fields.Char('Usuario', required=True, default='admin')
    password = fields.Char('Contraseña', required=True, default='admin')
    active = fields.Boolean('Activo', default=True)
    last_test = fields.Datetime('Última prueba de conexión')
    connection_status = fields.Selection([
        ('success', 'Conexión exitosa'),
        ('failed', 'Conexión fallida'),
        ('not_tested', 'No probado')
    ], string='Estado de conexión', default='not_tested')
    
    @api.model
    def get_active_config(self):
        """Obtener la configuración activa de Nextcloud"""
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            # Crear configuración por defecto si no existe
            config = self.create({
                'name': 'Configuración por defecto',
                'url': 'http://nextcloud:80',
                'username': 'admin', 
                'password': 'admin'
            })
        return config
    
    def test_connection(self):
        """Probar conexión con Nextcloud"""
        try:
            client = NextcloudWebDAVClient(self.url, self.username, self.password)
            if client.test_connection():
                self.write({
                    'connection_status': 'success',
                    'last_test': fields.Datetime.now()
                })
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Conexión exitosa',
                        'message': 'La conexión con Nextcloud fue exitosa',
                        'type': 'success',
                    }
                }
            else:
                self.write({
                    'connection_status': 'failed',
                    'last_test': fields.Datetime.now()
                })
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error de conexión',
                        'message': 'No se pudo conectar con Nextcloud. Verifique las credenciales.',
                        'type': 'danger',
                    }
                }
        except Exception as e:
            _logger.error(f"Error probando conexión Nextcloud: {str(e)}")
            self.write({
                'connection_status': 'failed',
                'last_test': fields.Datetime.now()
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error de conexión',
                    'message': f'Error: {str(e)}',
                    'type': 'danger',
                }
            }
