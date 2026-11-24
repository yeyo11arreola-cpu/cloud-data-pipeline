
# Cloud Data Pipeline

## Descripción

Proyecto personal de infraestructura y automatización de datos
mediante Python, PostgreSQL, Linux y Docker.

El sistema implementa un pipeline ETL para procesar, validar,
transformar y almacenar registros comerciales simulados.

## Tecnologías utilizadas

- Python
- Pandas
- PostgreSQL
- SQL
- Psycopg
- Linux Ubuntu
- WSL 2
- Docker
- Docker Compose
- Git

## Arquitectura

CSV -> Python ETL -> PostgreSQL

Los servicios de Python y PostgreSQL se ejecutan en contenedores
independientes conectados mediante una red interna de Docker.

## Funcionalidades

- Extracción de información desde archivos CSV.
- Validación y limpieza de datos.
- Eliminación de registros duplicados.
- Validación de cantidades y precios.
- Cálculo automático de importes.
- Almacenamiento en PostgreSQL.
- Persistencia de datos mediante volúmenes.
- Registro de eventos mediante logging.
- Prevención de inserciones duplicadas.
- Configuración de credenciales mediante variables de entorno.

## Resultados

- Registros procesados: 12.
- Registros válidos: 9.
- Registros descartados: 3.
- Importe total: $103,400 MXN.

Los datos utilizados son ficticios.

## Instalación y ejecución

Requisitos: Docker y Docker Compose.

Crear un archivo .env en la raíz del proyecto con una
variable DB_PASSWORD y una contraseña propia.

Iniciar la base de datos:

    docker compose up -d db

Construir y ejecutar el pipeline:

    docker compose run --rm --build pipeline

Consultar la base de datos:

    docker compose exec db psql -U pipeline_user -d ventas_db

Detener los servicios:

    docker compose down

## Objetivo profesional

Aplicar conocimientos prácticos de infraestructura,
contenedores, automatización e ingeniería de datos
en un entorno de desarrollo local reproducible.

## Autor

Ingeniero Mecatrónico | Proyecto de formación en
Cloud e Ingeniería de Datos.
