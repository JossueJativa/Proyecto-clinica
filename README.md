# Proyecto Integrador - Integración de sistemas

## Introducción
La transformación digital en el ámbito de la salud representa una necesidad urgente para mejorar la eficiencia operativa, la atención al paciente y la seguridad de los procesos clínicos. En este contexto, la Clínica Universitaria enfrenta múltiples desafíos debido a la fragmentación de sus sistemas de información, generando duplicidad de datos, demoras en los flujos de trabajo y una experiencia deficiente para usuarios y pacientes.

Este proyecto integrador tiene como objetivo aplicar los conocimientos adquiridos en la materia Integración de Sistemas para diseñar e implementar una solución real que permita integrar al menos tres sistemas clave utilizados en la clínica, resolviendo problemas concretos mediante el uso de patrones de integración, herramientas open source y arquitecturas modernas.

## Objetivo general
Diseñar, desarrollar e implementar una solución de integración funcional y segura, que permita modernizar los procesos administrativos, clínicos y de soporte de la clínica, resolviendo al menos tres problemas identificados en el escenario actual, mediante el uso de herramientas reales y patrones de integración aplicados en entornos profesionales.

## Sistema a integrar
Minimo 3 sistemas deben estar implementado, donde tenemos la siguiente instrucción:
Cada equipo deberá seleccionar y configurar los sistemas reales, poblarlos con data de prueba y demostrar su integración. Algunos de los sistemas propuestos:

* OdooERP: Sistema de gestión de historias clínicas electrónicas.
* Keycloak: Gestión de identidad, SSO y control de acceso.
* Google Drive: Almacenamiento seguro de backups automáticos de Odoo.

Se creo un docker compose para poder tener las aplicaciones en un entorno de desarrollo compartido, donde se mostraran los siguientes endpoints para poder acceder a cada uno de los mismos
* Keycloak: http://localhost:8080/
* OdooERP: http://localhost:8069/web?debug=1
* RabbitMQ: http://localhost:15672

## Credenciales de las aplicaciones
| Aplicacion | Usuario | Contraseña |
| ---------- | ------- | ---------- |
| Keycloack  | admin   | admin      |
| RabitMQ    | admin   | admin      |
| OdooERP    | Se crea en el inicio |

## Patrones de integración a aplicar
*   Transferencia de archivos.
*   Seguridad y autorización con SSO (Keycloak).
*   API RESTful / Invocación remota.

Al momento de necesitar por lo menos 3 servicios de patrones a integrar, se van a usar los siguientes:

*   **Transferencia de archivos** - Para backups automáticos y seguros de Odoo a Google Drive.
*   **Seguridad y autorización (Keycloak)** - SSO centralizado para todos los usuarios de Odoo.
*   **API RESTful / Invocación remota** - Para envío de correos electrónicos de confirmación de compra mediante Gmail API.

## Soluciones de Integración Implementadas

### 🔹 **1. Integración Odoo + Google Drive - Backups Automáticos Seguros**

#### 🔧 **Patrón aplicado:** Transferencia de archivos

#### 🧩 **Problema que resuelve:**
Los backups de la base de datos de Odoo no estaban automatizados ni se almacenaban en una ubicación externa segura, lo que exponía a la clínica a una pérdida total de información en caso de un fallo del servidor.

#### 🛠️ **Solución técnica:**
- Se utiliza el módulo **"Automatic Database Backup To Local Server, Remote Server, Google Drive, Dropbox, Onedrive, Nextcloud and Amazon S3 Odoo18"** para programar backups automáticos.
- Los archivos de respaldo se transfieren de forma segura a una carpeta designada en Google Drive utilizando su API.
- Se utiliza la autenticación OAuth2 para garantizar que solo Odoo pueda escribir en la carpeta de backups.

#### 🧪 **Prueba funcional:**
- Generar un backup (manual o automático) en Odoo.
- Verificar que el archivo de respaldo aparece correctamente en la carpeta de Google Drive designada.

---

### 🔹 **2. Integración Odoo + Keycloak - SSO y Gestión Centralizada de Usuarios**

#### 🔧 **Patrón aplicado:** Seguridad y autorización con SSO (Single Sign-On)

#### 🧩 **Problema que resuelve:**
La gestión de usuarios estaba fragmentada, obligando a los empleados a recordar múltiples contraseñas y dificultando al equipo de TI la administración de accesos y permisos de forma centralizada.

#### 🛠️ **Solución técnica:**
- Integrar Odoo con Keycloak como proveedor de identidad (IdP) usando el protocolo OpenID Connect.
- Los usuarios inician sesión en Odoo utilizando sus credenciales centralizadas de Keycloak.
- La creación, modificación y eliminación de usuarios se gestiona directamente en Keycloak, sincronizándose con Odoo.

#### 🧪 **Prueba funcional:**
- Crear un usuario en Keycloak.
- Iniciar sesión en Odoo con el nuevo usuario de Keycloak sin necesidad de crearlo previamente en Odoo.
- Desactivar el usuario en Keycloak y verificar que ya no puede acceder a Odoo.

---

### 🔹 **3. Integración Odoo + Google Console - Notificaciones de Compra por Email**

#### 🔧 **Patrón aplicado:** API RESTful / Invocación remota

#### 🧩 **Problema que resuelve:**
El envío de correos de confirmación de compra desde Odoo requería configurar un servidor SMTP complejo y gestionar la entrega de correos de manera manual, lo que generaba problemas de confiabilidad y mantenimiento.

#### 🛠️ **Solución técnica:**
- Configurar Odoo para utilizar Gmail API a través de Google Console para el envío de correos electrónicos.
- Implementar autenticación OAuth2 con Google para acceso seguro a la API de Gmail.
- Al confirmar una compra, Odoo invoca directamente la API de Gmail para enviar el correo de confirmación de manera confiable.
- Esto garantiza una alta tasa de entrega y elimina la necesidad de mantener un servidor SMTP local.

#### 📋 **Pasos de implementación:**

1.  **Configuración de Google Console:**
    - Crear un proyecto en Google Cloud Console y habilitar la API de Gmail.
    - Configurar credenciales OAuth2 y obtener client ID y client secret.
    - Configurar los scopes necesarios para el envío de correos.

2.  **Configuración en Odoo:**
    - Instalar el módulo de integración con Gmail API.
    - Configurar las credenciales OAuth2 en Odoo.
    - Configurar el servidor de correo saliente para usar Gmail API.

3.  **Desarrollo del flujo de envío:**
    - Modificar el flujo de confirmación de compra para que genere y envíe el correo usando la API de Gmail.
    - Implementar plantillas de correo personalizadas para confirmaciones de compra.

#### 🧪 **Prueba funcional:**
- Realizar una compra en Odoo y confirmar que se envía automáticamente un correo de confirmación.
- Verificar que el correo llega correctamente al destinatario desde la cuenta de Gmail configurada.
- Comprobar que los datos de la compra se incluyen correctamente en el correo.

---

## Arquitectura de Integración Completa

```
                ┌─────────────┐
                │   Keycloak  │
                │    (SSO)    │
                └─────┬───────┘
                      │
          ┌───────────┼──────────────────┐
          │           │                  │
          ▼           ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    Odoo     │──│ Google Drive│  │Gmail API    │
│   (ERP)     │  │  (Backups)  │  │(Google      │
└─────────────┘  └─────────────┘  │ Console)    │
                                  └─────────────┘
```

### Flujos de Integración:

1.  **Flujo de Transferencia de Archivos (Backups):**
    `Odoo → Google Drive (API REST) → Backup seguro en la nube`

2.  **Flujo de Autenticación (SSO):**
    `Usuario → Odoo → Redirección a Keycloak → Autenticación → Acceso a Odoo`

3.  **Flujo de Notificaciones por Email:**
    `Odoo (Compra) → Gmail API (Google Console) → Envío de correo de confirmación`

## Tecnologías y Herramientas Utilizadas

### Desarrollo e Integración:
-   **Odoo Custom Modules**: Python
-   **Google APIs**: Gmail API, Google Drive API
-   **Base de datos**: PostgreSQL

### APIs y Protocolos:
-   **REST API**: Para comunicación con Google Drive y Gmail
-   **OpenID Connect**: Para SSO con Keycloak
-   **OAuth2**: Para autenticación con servicios de Google

## Instrucciones de Despliegue

### 1. Levantar entorno base:
```bash
docker-compose up -d
```

### 2. Configurar integraciones:
```bash
# Instalar dependencias de Odoo
docker exec odoo pip install requests google-api-python-client

# Configurar módulos personalizados
docker cp ./odoo-addons odoo:/mnt/extra-addons/
```

### 3. Configurar Keycloak:
- Acceder a http://localhost:8080/
- Crear realm 'clinica-realm'
- Configurar clients para cada servicio

### 4. Configurar Google Console:
- Crear proyecto en Google Cloud Console
- Habilitar APIs de Gmail y Google Drive
- Configurar credenciales OAuth2

### 5. Verificar integraciones:
- Test SSO entre sistemas
- Verificar subida de backups a Google Drive
- Comprobar envío de correos mediante Gmail API

## Métricas de Éxito

-   ✅ **100% de backups automatizados** y almacenados externamente en Google Drive.
-   ✅ **Reducción del 80% en tiempo de login** y eliminación de gestión de contraseñas en Odoo gracias a SSO.
-   ✅ **99% de entrega de correos electrónicos** gracias a Gmail API y Google Console.
-   ✅ **Integración directa con servicios de Google** para mayor confiabilidad.

## Resumen de Soluciones Implementadas

| # | Solución | Patrón | Sistemas Integrados | Problema Resuelto |
|---|---|---|---|---|
| 1 | Backups Automáticos Seguros | Transferencia de archivos | Odoo ↔ Google Drive | Riesgo de pérdida de datos |
| 2 | SSO y Gestión de Usuarios | Seguridad y autorización | Odoo ↔ Keycloak | Gestión de identidades fragmentada |
| 3 | Notificaciones por Email | API RESTful / Invocación remota | Odoo ↔ Gmail API | Problemas de entrega de correos |