# -*- coding: utf-8 -*-

import logging
from ..services.nextcloud_webdav import DocumentUploader

_logger = logging.getLogger(__name__)

def post_invoice_pdf_generation(env, invoice_id, pdf_content):
    """
    Hook llamado después de generar PDF de factura
    
    Args:
        env: Environment de Odoo
        invoice_id: ID de la factura
        pdf_content: Contenido del PDF generado
    """
    try:
        # Obtener registro de factura
        invoice = env['account.move'].browse(invoice_id)
        
        if not invoice.exists():
            _logger.warning(f"Factura con ID {invoice_id} no encontrada")
            return
        
        # Obtener configuración de Nextcloud
        config = env['nextcloud.config'].get_active_config()
        
        if not config:
            _logger.warning("No hay configuración de Nextcloud disponible")
            return
        
        # Inicializar uploader
        uploader = DocumentUploader({
            'url': config.url,
            'username': config.username,
            'password': config.password
        })
        
        # Subir archivo
        result = uploader.upload_invoice_pdf(invoice, pdf_content)
        
        if result['success']:
            # Actualizar registro de factura
            invoice.write({
                'nextcloud_url': result.get('url', ''),
                'nextcloud_uploaded': True
            })
            _logger.info(f"PDF de factura {invoice.name} subido automáticamente a Nextcloud")
        else:
            _logger.error(f"Error en hook de factura {invoice.name}: {result.get('error')}")
            
    except Exception as e:
        _logger.error(f"Excepción en hook post_invoice_pdf_generation: {str(e)}")

def post_prescription_pdf_generation(env, prescription_id, pdf_content):
    """
    Hook llamado después de generar PDF de receta médica
    
    Args:
        env: Environment de Odoo
        prescription_id: ID de la receta
        pdf_content: Contenido del PDF generado
    """
    try:
        # Este hook sería para un módulo de recetas médicas (no existe por defecto en Odoo)
        # Aquí se implementaría la lógica similar para recetas
        _logger.info(f"Hook de receta médica llamado para ID: {prescription_id}")
        
        # Obtener configuración y subir archivo...
        # (Implementación similar a facturas)
        
    except Exception as e:
        _logger.error(f"Excepción en hook post_prescription_pdf_generation: {str(e)}")

def register_pdf_hooks(env):
    """
    Registrar todos los hooks de PDF
    
    Args:
        env: Environment de Odoo
    """
    try:
        # Registrar hooks en el sistema de eventos de Odoo
        # Esto sería parte de la inicialización del módulo
        _logger.info("Hooks de PDF registrados exitosamente")
        
    except Exception as e:
        _logger.error(f"Error registrando hooks de PDF: {str(e)}")
