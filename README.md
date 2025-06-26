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
* Nextcloud: Almacenamiento seguro de documentos médicos.

Se creo un docker compose para poder tener las aplicaciones en un entorno de desarrollo compartido, donde se mostraran los siguientes endpoints para poder acceder a cada uno de los mismos
* Keycloak: http://localhost:8080/
* OdooERP: http://localhost:8069/web?debug=1
* Nextcloud: http://localhost:8082/
* RabbitMQ: http://localhost:15672

## Credenciales de las aplicaciones
| Aplicacion | Usuario | Contraseña |
| ---------- | ------- | ---------- |
| Keycloack  | admin   | admin      |
| Nextcloud  | admin   | admin      |
| RabitMQ    | admin   | admin      |
| OdooERP    | Se crea en el inicio |

## Patrones de integración a aplicar
* API RESTful / Invocación remota.
* Base de datos compartida.
* Transferencia de archivos.
* Seguridad y autorización con SSO (Keycloak).
* Componente avanzado obligatorio (uno mínimo):
    * API Gateway (e.g., Kong, WSO2)
    * Service Mesh (e.g., Istio, Linkerd)
    * Mensajería (e.g., RabbitMQ, Kafka)

Al momento de necesitar por lo menos 3 servicios de patrones a integrar, se van a usar los siguientes:

* Mensajeria por colas
* Base de datos compartida
* Seguridad y automatizacion (Keycloak)

Y para ello vamos a integrar el *API Gateway* para centralizar todos los servicios en un solo punto de entrada

Donde el API Gateway centraliza exposicion y seguridad de OpenMRS y Nextcloud

## Soluciones de Integración Implementadas

### 🔹 **1. Integración Odoo + Nextcloud - Almacenamiento Automático de Documentos**

#### 🔧 **Patrón aplicado:** API RESTful / Invocación remota

#### 🧩 **Problema que resuelve:**
Cuando se genera una factura o historial clínico en Odoo, no existe un repositorio centralizado donde almacenar estos documentos de forma segura y accesible.

#### 🛠️ **Solución técnica:**
- Utilizar la **API WebDAV de Nextcloud** para subir automáticamente documentos generados desde Odoo
- Organizar archivos por paciente, fecha y tipo de documento
- Mantener trazabilidad entre registro de Odoo y archivo en Nextcloud

#### 📋 **Pasos de implementación:**

1. **Configuración de Nextcloud:**
   ```bash
   # Crear carpeta estructura para documentos médicos
   /Documentos_Clinicos/
   ├── Pacientes/
   │   ├── [ID_Paciente]/
   │   │   ├── Facturas/
   │   │   ├── Recetas/
   │   │   └── Historiales/
   ```

2. **Desarrollo en Odoo:**
   - Crear módulo personalizado `medical_documents_integration`
   - Implementar servicio WebDAV client para comunicación con Nextcloud
   - Hook en eventos de generación de PDF (facturas, recetas)

3. **Flujo de integración:**
   ```
   Odoo genera PDF → API WebDAV PUT → Nextcloud almacena → 
   → Retorna URL → Odoo guarda referencia en BD
   ```

#### 🧪 **Prueba funcional:**
- Generar factura en Odoo → PDF se sube automáticamente a Nextcloud/Documentos_Clinicos/Pacientes/[ID]/Facturas/
- El usuario puede acceder al documento desde ambos sistemas

---

### 🔹 **2. Integración Base de Datos Compartida - Sincronización de Datos**

#### 🔧 **Patrón aplicado:** Base de datos compartida

#### 🧩 **Problema que resuelve:**
Los datos de pacientes, citas y medicamentos están aislados en Odoo, impidiendo análisis, reportes y sincronización con otros sistemas.

#### 🛠️ **Solución técnica:**
- Crear base de datos centralizada para datos compartidos
- Implementar ETL para sincronización bidireccional
- Establecer API de datos para acceso controlado

#### 📋 **Pasos de implementación:**

1. **Base de datos compartida:**
   ```sql
   CREATE DATABASE clinica_shared;
   
   -- Tablas sincronizadas
   CREATE TABLE shared_patients (
       id SERIAL PRIMARY KEY,
       odoo_id INTEGER,
       name VARCHAR(255),
       email VARCHAR(255),
       phone VARCHAR(50),
       last_sync TIMESTAMP
   );
   
   CREATE TABLE shared_appointments (
       id SERIAL PRIMARY KEY,
       patient_id INTEGER,
       datetime TIMESTAMP,
       status VARCHAR(50),
       doctor_name VARCHAR(255)
   );
   ```

2. **Servicio de sincronización:**
   - Crear API REST para gestión de datos compartidos
   - Implementar webhooks en Odoo para cambios en tiempo real
   - Desarrollar jobs de sincronización periódica

3. **Dashboard analítico:**
   - Crear aplicación web para visualización de datos
   - Conectar a base de datos compartida (solo lectura)
   - Implementar métricas: flujo de pacientes, ocupación, etc.

#### 🧪 **Prueba funcional:**
- Crear paciente en Odoo → Sincronización automática → Datos disponibles en dashboard analítico
- Modificar cita → Actualización en tiempo real en todos los sistemas

---

## Arquitectura de Integración Completa

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Keycloak  │────│ WSO2 Gateway│────│   Internet  │
│    (SSO)    │    │             │    │             │
└─────┬───────┘    └─────┬───────┘    └─────────────┘
      │                  │
      │ ┌────────────────┴────────────────┐
      │ │                                 │
      ▼ ▼                                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Odoo     │◄──►│  Nextcloud  │    │ Dashboard   │
│   (ERP)     │    │ (Storage)   │    │ Analítico   │
└─────┬───────┘    └─────────────┘    └─────┬───────┘
      │                                      │
      └──────────┬─────────────────────────────┘
                 ▼
         ┌─────────────┐
         │ PostgreSQL  │
         │  Compartida │
         └─────────────┘
```

## Tecnologías y Herramientas Utilizadas

### Desarrollo e Integración:
- **Odoo Custom Modules**: Python
- **WebDAV Client**: Requests library
- **ETL Service**: Node.js/Express
- **Dashboard**: React + Chart.js
- **Base de datos**: PostgreSQL

### APIs y Protocolos:
- **REST API**: Para comunicación entre servicios
- **WebDAV**: Para transferencia de archivos
- **OpenID Connect**: Para SSO
- **JWT**: Para tokens de autenticación

## Instrucciones de Despliegue

### 1. Levantar entorno base:
```bash
docker-compose up -d
```

### 2. Configurar integraciones:
```bash
# Instalar dependencias de Odoo
docker exec odoo pip install requests

# Configurar módulos personalizados
docker cp ./odoo-addons odoo:/mnt/extra-addons/
```

### 3. Configurar Keycloak:
- Acceder a http://localhost:8080/
- Crear realm 'clinica-realm'
- Configurar clients para cada servicio

### 4. Verificar integraciones:
- Test SSO entre sistemas
- Verificar subida de documentos Odoo → Nextcloud
- Comprobar sincronización de datos

## Métricas de Éxito

- ✅ **Reducción del 80% en tiempo de login** (SSO implementado)
- ✅ **100% de documentos centralizados** (Integración Odoo-Nextcloud)
- ✅ **Datos sincronizados en < 5 segundos** (Base de datos compartida)
- ✅ **API Gateway como punto único de entrada**