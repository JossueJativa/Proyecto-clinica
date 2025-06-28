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
*   Mensajería (e.g., RabbitMQ, Kafka).

Al momento de necesitar por lo menos 3 servicios de patrones a integrar, se van a usar los siguientes:

*   **Transferencia de archivos** - Para backups automáticos y seguros de Odoo a Google Drive.
*   **Seguridad y autorización (Keycloak)** - SSO centralizado para todos los usuarios de Odoo.
*   **Mensajería por colas (RabbitMQ)** - Para envío asíncrono de correos electrónicos de confirmación de compra.

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

### 🔹 **3. Integración Odoo + RabbitMQ - Notificaciones de Compra por Email**

#### 🔧 **Patrón aplicado:** Mensajería por colas (RabbitMQ)

#### 🧩 **Problema que resuelve:**
El envío de correos de confirmación de compra desde Odoo era un proceso síncrono. Si el servicio de email estaba lento o fallaba, la interfaz de usuario de Odoo se bloqueaba hasta que el proceso terminaba o daba error, afectando la experiencia del usuario.

#### 🛠️ **Solución técnica:**
- Al confirmar una compra, Odoo no envía el email directamente. En su lugar, publica un mensaje en una cola de RabbitMQ.
- Un servicio consumidor (worker) independiente escucha en esa cola, toma los mensajes y se encarga de procesar y enviar el correo electrónico.
- Esto desacopla el proceso de envío de la interfaz de Odoo, permitiendo una respuesta inmediata al usuario y añadiendo tolerancia a fallos (si el envío falla, el mensaje puede ser reintentado).

#### 📋 **Pasos de implementación:**

1.  **Configuración de RabbitMQ:**
    - Crear un `exchange` llamado `email_exchange` y una `queue` llamada `purchase_confirmation_queue`.

2.  **Desarrollo en Odoo (Producer):**
    - Modificar el flujo de confirmación de compra para que, en lugar de llamar al servicio de email, publique un mensaje JSON con los datos de la compra en la cola de RabbitMQ.

3.  **Servicio Consumer (Worker):**
    - Crear un servicio independiente (e.g., en Python) que se conecta a RabbitMQ.
    - Este servicio consume los mensajes de la cola, construye el correo y lo envía a través de un servidor SMTP.

#### 🧪 **Prueba funcional:**
- Realizar una compra en Odoo. La interfaz responde de inmediato.
- Verificar que un mensaje aparece en la cola de RabbitMQ.
- Verificar que el servicio consumidor procesa el mensaje y el correo de confirmación llega al destinatario.

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
│    Odoo     │──│ Google Drive│  │  RabbitMQ   │
│   (ERP)     │  │  (Backups)  │  │ (Message    │
└─────┬───────┘  └─────────────┘  │  Broker)    │
      │                           └─────┬───────┘
      │                                 │
      └─────────────────────────────────► Email
                                        │ Service
                                        │ (Worker)
                                        └──────────
```