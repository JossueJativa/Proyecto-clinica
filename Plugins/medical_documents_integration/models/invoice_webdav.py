# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ..services.nextcloud_webdav import DocumentUploader
import logging
import base64

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    nextcloud_url = fields.Char('URL en Nextcloud', readonly=True)
    nextcloud_uploaded = fields.Boolean('Subido a Nextcloud', default=False)
    
    def action_post(self):
        """Override para subir PDF automáticamente al confirmar factura"""
        result = super(AccountMove, self).action_post()
        
        # Solo procesar facturas de cliente
        if self.move_type == 'out_invoice':
            self._upload_to_nextcloud()
            
        return result
    
    def _upload_to_nextcloud(self):
        """Subir PDF de factura a Nextcloud"""
        try:
            # Obtener configuración de Nextcloud
            config_model = self.env['nextcloud.config']
            config = config_model.get_active_config()
            
            if not config:
                _logger.warning("No hay configuración de Nextcloud disponible")
                return
            
            # Generar PDF de la factura
            pdf_content = self._generate_pdf()
            
            if pdf_content:
                # Inicializar uploader
                uploader = DocumentUploader({
                    'url': config.url,
                    'username': config.username,
                    'password': config.password
                })
                
                # Subir archivo
                result = uploader.upload_invoice_pdf(self, pdf_content)
                
                if result['success']:
                    self.write({
                        'nextcloud_url': result.get('url', ''),
                        'nextcloud_uploaded': True
                    })
                    _logger.info(f"Factura {self.name} subida exitosamente a Nextcloud")
                else:
                    _logger.error(f"Error subiendo factura {self.name}: {result.get('error', 'Error desconocido')}")
            
        except Exception as e:
            _logger.error(f"Excepción subiendo factura {self.name} a Nextcloud: {str(e)}")
    
    def _generate_pdf(self):
        """Generar PDF de la factura"""
        try:
            # Usar el reporte estándar de Odoo para facturas
            report = self.env.ref('account.account_invoices')
            pdf_content, _ = report._render_qweb_pdf(self.ids)
            return pdf_content
        except Exception as e:
            _logger.error(f"Error generando PDF para factura {self.name}: {str(e)}")
            return None
    
    def action_upload_to_nextcloud(self):
        """Acción manual para subir a Nextcloud"""
        self._upload_to_nextcloud()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Subida a Nextcloud',
                'message': f'Procesando subida de factura {self.name}',
                'type': 'info',
            }
        }
    
    def action_view_in_nextcloud(self):
        """Abrir documento en Nextcloud"""
        if self.nextcloud_url:
            return {
                'type': 'ir.actions.act_url',
                'url': self.nextcloud_url,
                'target': 'new',
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'Esta factura no ha sido subida a Nextcloud',
                    'type': 'warning',
                }
            }
