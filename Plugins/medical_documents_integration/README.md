# Medical Documents Integration

Módulo de Odoo para integración automática con Nextcloud para almacenamiento de documentos médicos.

## Características

- **Subida automática de PDFs**: Las facturas se suben automáticamente a Nextcloud al ser confirmadas
- **Organización estructurada**: Los documentos se organizan por paciente, tipo y fecha
- **Configuración flexible**: Configuración de conexión a Nextcloud desde la interfaz de Odoo
- **Hooks extensibles**: Sistema de hooks para diferentes tipos de documentos

## Estructura de carpetas en Nextcloud

```
Documentos_Clinicos/
├── Pacientes/
│   ├── [Nombre_Paciente]/
│   │   ├── Facturas/
│   │   │   └── [YYYY-MM]/
│   │   ├── Recetas/
│   │   │   └── [YYYY-MM]/
│   │   └── Historiales/
│   │       └── [YYYY-MM]/
```

## Instalación

1. Copiar el módulo a la carpeta de addons de Odoo
2. Actualizar la lista de aplicaciones
3. Instalar "Medical Documents Integration"
4. Configurar la conexión a Nextcloud en Administración > Configuración Nextcloud

## Configuración

### Nextcloud
- URL: `http://nextcloud:80` (para Docker)
- Usuario: `admin`
- Contraseña: `admin`

### Dependencias Python
El módulo requiere la librería `requests` que se instala automáticamente.

## Uso

### Automático
- Al confirmar una factura, se sube automáticamente a Nextcloud
- Se muestra el estado de subida en la pestaña "Nextcloud" de la factura

### Manual
- Botón "Subir a Nextcloud" en facturas no subidas
- Botón "Ver en Nextcloud" para acceder al documento

## Desarrollo

### Estructura del módulo
```
medical_documents_integration/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── nextcloud_config.py
│   └── invoice_webdav.py
├── services/
│   ├── __init__.py
│   └── nextcloud_webdav.py
├── hooks/
│   ├── __init__.py
│   └── pdf_hooks.py
├── views/
│   └── nextcloud_config_views.xml
├── data/
│   └── nextcloud_config_data.xml
└── security/
    └── ir.model.access.csv
```

### Extensiones
Para agregar soporte a otros tipos de documentos:
1. Crear nuevo modelo heredando el objeto base
2. Implementar método `_upload_to_nextcloud`
3. Agregar hook en `pdf_hooks.py`

## Solución de problemas

### Error de conexión
- Verificar que Nextcloud esté corriendo
- Comprobar credenciales en la configuración
- Usar el botón "Probar Conexión"

### Permisos
- Verificar que el usuario tenga permisos de escritura en Nextcloud
- Comprobar que el directorio de destino sea accesible

## API WebDAV

El módulo utiliza WebDAV para comunicarse con Nextcloud:
- `MKCOL`: Crear directorios
- `PUT`: Subir archivos
- `PROPFIND`: Verificar conexión

## Logs

Los logs se pueden encontrar en el archivo de log de Odoo:
```
[INFO] medical_documents_integration.services.nextcloud_webdav: Archivo subido exitosamente
[ERROR] medical_documents_integration.models.invoice_webdav: Error subiendo factura
```
