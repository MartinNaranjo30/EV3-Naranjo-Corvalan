# Sistema End-to-End de Estadísticas de la NBA

Este proyecto implementa una arquitectura desacoplada y contenerizada para el procesamiento, almacenamiento y visualización de métricas de rendimiento de jugadores de la NBA. El ecosistema está diseñado bajo un enfoque de microservicios utilizando "Docker Compose", lo que garantiza la portabilidad, escalabilidad y aislamiento de cada componente del pipeline de datos.

## Arquitectura del Sistema

El sistema está compuesto por cuatro capas independientes que se comunican de forma asíncrona a través de redes virtuales de Docker:

1. Pipeline ETL (`etl`): Servicio autónomo encargado de la extracción de datos crudos (`nba_10000_dirty.csv`), transformaciones de limpieza, tipado y normalización mediante Pandas, y posterior carga en el motor de almacenamiento.
2. Almacenamiento (`data`): Base de datos relacional ligera utilizando "SQLite" (`nba.db`), encargada de persistir de forma estructurada los datos limpios en la tabla `nba_clean`.
3. Capa de Negocio / API REST (`api`): Desarrollada con "FastAPI" y ejecutada mediante Uvicorn. Expone endpoints optimizados (`/players` y `/stats`) para consultar las métricas procesadas, aislando la base de datos del cliente final.
4. Capa de Presentación / Dashboard (`dashboards`): Interfaz web interactiva construida con "Streamlit" que consume los servicios de la API mediante peticiones HTTP y renderiza visualizaciones dinámicas de los indicadores de la liga.


## Requisitos Previos

Para ejecutar este proyecto, solo es necesario contar con el siguiente entorno instalado:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Incluye Docker Compose)
* Git (Para la clonación del repositorio)

---

## Instrucciones de Despliegue

Gracias a la contenerización, todo el ecosistema se compila, ejecuta el flujo ETL y levanta los servicios con un único comando maestro.

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/MartinNaranjo30/EV3-Naranjo-Corvalan.git
   cd "Ev3 NBA"

2. Levantar la infraestructura:
    Ejecutar el comando de orquestación en la terminal. El flag --build asegura que se procesen las últimas actualizaciones del código fuente:
    docker-compose up --build

3. Acceso a la aplicación:
    Una vez que la terminal indique que los servicios están en línea, abra el navegador web e ingresa a las siguientes direcciones:

   -Dashboard de Streamlit: http://localhost:8501 (o usando la IP local http://127.0.0.1:8501)
   -Documentación Interactiva de la API (Swagger): http://localhost:8000/docs