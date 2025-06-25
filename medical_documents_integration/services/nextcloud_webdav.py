# -*- coding: utf-8 -*-

import requests
import base64
import logging
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
import os

_logger = logging.getLogger(__name__)

class NextcloudWebDAVClient:
    """Cliente WebDAV para comunicación con Nextcloud"""
    
    def __init__(self, base_url, username, password):
        """
        Inicializar cliente WebDAV
        
        Args:
            base_url (str): URL base de Nextcloud (ej: http://localhost:8082)
            username (str): Usuario de Nextcloud
            password (str): Contraseña de Nextcloud
        """
        self.base_url = base_url.rstrip('/')
        self.webdav_url = f"{self.base_url}/remote.php/dav/files/{username}/"
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        
    def create_folder(self, folder_path):
        """
        Crear carpeta en Nextcloud si no existe
        
        Args:
            folder_path (str): Ruta de la carpeta a crear
            
        Returns:
            bool: True si se creó o ya existe, False en caso de error
        """
        try:
            url = urljoin(self.webdav_url, folder_path.strip('/') + '/')
            response = self.session.request('MKCOL', url)
            
            if response.status_code in [201, 405]:  # 201: creada, 405: ya existe
                _logger.info(f"Carpeta creada/existe: {folder_path}")
                return True
            else:
                _logger.error(f"Error creando carpeta {folder_path}: {response.status_code}")
                return False
                
        except Exception as e:
            _logger.error(f"Excepción creando carpeta {folder_path}: {str(e)}")
            return False
    
    def upload_file(self, file_content, remote_path, content_type='application/pdf'):
        """
        Subir archivo a Nextcloud
        
        Args:
            file_content (bytes): Contenido del archivo
            remote_path (str): Ruta remota donde guardar el archivo
            content_type (str): Tipo de contenido del archivo
            
        Returns:
            dict: Resultado de la operación con 'success' y 'url' o 'error'
        """
        try:
            # Crear directorios padre si no existen
            folder_path = '/'.join(remote_path.split('/')[:-1])
            if folder_path:
                self.create_folder(folder_path)
            
            # Subir archivo
            url = urljoin(self.webdav_url, remote_path.strip('/'))
            
            headers = {
                'Content-Type': content_type,
                'Content-Length': str(len(file_content))
            }
            
            response = self.session.put(url, data=file_content, headers=headers)
            
            if response.status_code in [200, 201, 204]:
                file_url = f"{self.base_url}/index.php/s/{self._get_share_token(remote_path)}"
                _logger.info(f"Archivo subido exitosamente: {remote_path}")
                
                return {
                    'success': True,
                    'url': file_url,
                    'remote_path': remote_path
                }
            else:
                error_msg = f"Error subiendo archivo: HTTP {response.status_code}"
                _logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            error_msg = f"Excepción subiendo archivo: {str(e)}"
            _logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def _get_share_token(self, file_path):
        """
        Obtener token de compartición para acceso público (simplificado)
        En implementación real, usaría la API de Nextcloud para crear shares
        """
        # Por ahora retorna un token basado en el path
        # En producción se debería usar la API de Nextcloud para crear shares reales
        return base64.b64encode(file_path.encode()).decode()[:16]
    
    def test_connection(self):
        """
        Probar conexión con Nextcloud
        
        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            response = self.session.request('PROPFIND', self.webdav_url)
            return response.status_code in [200, 207]
        except Exception as e:
            _logger.error(f"Error probando conexión: {str(e)}")
            return False

class DocumentUploader:
    """Clase principal para subir documentos médicos a Nextcloud"""
    
    def __init__(self, nextcloud_config):
        """
        Inicializar uploader con configuración de Nextcloud
        
        Args:
            nextcloud_config (dict): Configuración con url, username, password
        """
        self.client = NextcloudWebDAVClient(
            nextcloud_config['url'],
            nextcloud_config['username'], 
            nextcloud_config['password']
        )
    
    def upload_invoice_pdf(self, invoice, pdf_content):
        """
        Subir PDF de factura a Nextcloud
        
        Args:
            invoice: Objeto de factura de Odoo
            pdf_content (bytes): Contenido del PDF
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # Generar path organizado por cliente y fecha
            partner_name = self._sanitize_filename(invoice.partner_id.name)
            invoice_date = invoice.invoice_date.strftime('%Y-%m')
            filename = f"Factura_{invoice.name.replace('/', '_')}.pdf"
            
            remote_path = f"Documentos_Clinicos/Pacientes/{partner_name}/Facturas/{invoice_date}/{filename}"
            
            return self.client.upload_file(pdf_content, remote_path)
            
        except Exception as e:
            _logger.error(f"Error subiendo factura {invoice.name}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def upload_prescription_pdf(self, prescription, pdf_content):
        """
        Subir PDF de receta médica a Nextcloud
        
        Args:
            prescription: Objeto de receta médica
            pdf_content (bytes): Contenido del PDF
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            partner_name = self._sanitize_filename(prescription.partner_id.name)
            date = prescription.create_date.strftime('%Y-%m')
            filename = f"Receta_{prescription.name.replace('/', '_')}.pdf"
            
            remote_path = f"Documentos_Clinicos/Pacientes/{partner_name}/Recetas/{date}/{filename}"
            
            return self.client.upload_file(pdf_content, remote_path)
            
        except Exception as e:
            _logger.error(f"Error subiendo receta {prescription.name}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _sanitize_filename(self, filename):
        """
        Limpiar nombre de archivo para uso en filesystem
        
        Args:
            filename (str): Nombre original
            
        Returns:
            str: Nombre sanitizado
        """
        import re
        # Remover caracteres especiales y espacios
        sanitized = re.sub(r'[^\w\-_.]', '_', filename)
        # Remover múltiples underscores consecutivos
        sanitized = re.sub(r'_+', '_', sanitized)
        return sanitized.strip('_')
