# Proyecto Integrador - Integración de sistemas

## Introducción
La transformación digital en el ámbito de la salud representa una necesidad urgente para mejorar la eficiencia operativa, la atención al paciente y la seguridad de los procesos clínicos. En este contexto, la Clínica Universitaria enfrenta múltiples desafíos debido a la fragmentación de sus sistemas de información, generando duplicidad de datos, demoras en los flujos de trabajo y una experiencia deficiente para usuarios y pacientes.

Este proyecto integrador tiene como objetivo aplicar los conocimientos adquiridos en la materia Integración de Sistemas para diseñar e implementar una solución real que permita integrar al menos tres sistemas clave utilizados en la clínica, resolviendo problemas concretos mediante el uso de patrones de integración, herramientas open source y arquitecturas modernas.

## Objetivo general
Diseñar, desarrollar e implementar una solución de integración funcional y segura, que permita modernizar los procesos administrativos, clínicos y de soporte de la clínica, resolviendo al menos tres problemas identificados en el escenario actual, mediante el uso de herramientas reales y patrones de integración aplicados en entornos profesionales.

## Sistema a integrar
Minimo 3 sistemas deben estar implementado, donde tenemos la siguiente instrucción:
Cada equipo deberá seleccionar y configurar los sistemas reales, poblarlos con data de prueba y demostrar su integración. Algunos de los sistemas propuestos:

* OpenMRS: Sistema de gestión de historias clínicas electrónicas.
* Keycloak: Gestión de identidad, SSO y control de acceso.
* Nextcloud: Almacenamiento seguro de documentos médicos.

Se creo un docker compose para poder tener las aplicaciones en un entorno de desarrollo compartido, donde se mostraran los siguientes endpoints para poder acceder a cada uno de los mismos
* Keycloak: http://localhost:8080/
* OpenMRS: http://localhost:8081/openmrs/
* Nextcloud: http://localhost:8082/
* APIGateway: 
    - https://localhost:9443/devportal/
    - https://localhost:9443/publisher

## Credenciales de las aplicaciones
| Aplicacion | Usuario | Contraseña |
| ---------- | ------- | ---------- |
| Keycloack  | admin   | admin      |
| WSO2       | admin   | admin      |
| Nextcloud  | admin   | admin      |
| OpenMRS    | admin   | Admin123   |

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

* API Restfull / Invocacion remota
* Base de datos compartida ()
* Seguridad y automatizacion (Keycloak)

Y para ello vamos a integrar el *API Gateway* para centralizar todos los servicios en un solo punto de entrada

Donde el API Gateway centraliza exposicion y seguridad de OpenMRS y Nextcloud