# Laboratorio de Seguridad en NoSQL (MongoDB y Elasticsearch) con FastAPI

Repositorio de la práctica de auditoría, explotación controlada y endurecimiento (hardening) de una arquitectura de microservicios con FastAPI, MongoDB 7 y Elasticsearch 7.17.10.

## Estructura del Repositorio

```text
actividad_nosql/
├── docker-compose.yml       # Orquestación de contenedores (versión endurecida)
├── init_mongo.js            # Script de inicialización de MongoDB con RBAC (rol readWrite)
├── init_elastic.sh          # Script de creación y carga del índice 'articulos'
├── README.md                # Guía de despliegue y verificación
└── fastapi-app/
    ├── Dockerfile           # Imagen python:3.11-slim con Uvicorn
    ├── requirements.txt     # Dependencias (fastapi, uvicorn, pymongo, requests, pydantic)
    └── main.py              # API con validación estricta en Pydantic y filtrado de búsqueda
```

## Pasos de Ejecución

### 1. Despliegue del entorno
Clonar el repositorio, acceder al directorio y levantar los contenedores construyendo la imagen de FastAPI:

```bash
cd ~/actividad_nosql
docker-compose up -d --build
docker ps
```

### 2. Inicialización de datos
Los usuarios y pedidos en MongoDB se cargan automáticamente al iniciar el contenedor mediante `init_mongo.js`. Para poblar el índice de Elasticsearch, ejecutar:

```bash
bash init_elastic.sh
```

### 3. Pruebas funcionales (Smoke Test)
Verificar el inicio de sesión legítimo y la consulta de artículos:

```bash
curl -X POST http://localhost:8000/login_mongo -H "Content-Type: application/json" -d '{"username":"alice","password":"password123"}'
curl "http://localhost:8000/articulos?q=*"
```

### 4. Verificación de contramedidas ante ataques
Comprobar que la inyección de operadores lógicos NoSQL (`$ne`) es rechazada con código HTTP 422 y que el puerto 9200 de Elasticsearch no permite conexiones directas desde el exterior:

```bash
# Debe devolver error 422 (Input should be a valid string)
curl -X POST http://localhost:8000/login_mongo -H "Content-Type: application/json" -d '{"username":"alice","password":{"$ne":"x"}}'

# Debe devolver Connection refused (Puerto 9200 cerrado al host)
curl http://localhost:9200/_cat/indices?v
```
