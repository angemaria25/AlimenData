# AlimenData - Sistema Inteligente de Gestión y Distribución Alimentaria

## Descripción General

AlimenData es un sistema de logística diseñado para la gestión y distribución de recursos alimentarios en Cuba. El sistema permite el análisis de demanda poblacional, la optimización de mermas comerciales y la visualización del estado de inventarios en dependencias municipales.

Este proyecto constituye la Propuesta 2 del curso de Ingeniería de Datos 2025-2026, enfocándose en la logística de distribución de recursos, inventarios en condiciones de suministro variable y análisis de patrones estacionales de escasez.

---

## Estructura del Proyecto

```
alimendata/
│
├── .env                          # Variables de entorno (credenciales, configuración)
├── .gitignore                    # Archivos excluidos del control de versiones
├── docker-compose.yml            # Orquestación de contenedores Docker
├── README.md                     # Documentación del proyecto
│
├── document/                     # Documentación académica
│   └── informe_fase1.md          # Informe teórico y documentación de la Fase 1
│
├── backend/                      # Servicio de backend (API REST)
│   ├── .dockerignore                 # Archivos excluidos del contexto de build Docker
│   ├── Dockerfile                # Instrucciones para construir la imagen Docker
│   ├── entrypoint.sh             # Script de inicio: ejecuta migraciones y lanza la app
│   ├── requirements.txt          # Dependencias Python del proyecto
│   ├── alembic.ini               # Configuración de Alembic (migraciones)
│   │
│   ├── app/                      # Código fuente de la aplicación
│   │   ├── __init__.py           # Marca el directorio como paquete Python
│   │   ├── main.py               # Punto de entrada de la API FastAPI
│   │   ├── config.py             # Configuración centralizada con Pydantic
│   │   ├── database.py           # Conexión a PostgreSQL con SQLAlchemy
│   │   │
│   │   ├── models/               # Modelos de base de datos (ORM)
│   │   │   ├── __init__.py
│   │   │   └── models.py         # Definición de 10 tablas SQLAlchemy
│   │   │
│   │   ├── schemas/              # Esquemas de validación (Pydantic)
│   │   │   └── __init__.py
│   │   │
│   │   ├── seed/                 # Generación y carga de datos semilla
│   │   │   ├── __init__.py
│   │   │   ├── config.py         # Parámetros de productos y datos de Cuba
│   │   │   ├── generator.py      # Generador de 15 años de datos históricos
│   │   │   ├── loader.py         # Carga de datos a PostgreSQL via ORM
│   │   │   └── check_db.py       # Verificación de estado de BD vía ORM
│   │   │
│   │   ├── analytics/            # Métricas y visualizaciones
│   │   │   ├── __init__.py
│   │   │   ├── metrics.py        # Cálculo de rotación, patrones, alertas
│   │   │   └── visualization.py  # Generación de mapas de calor
│   │   │
│   │   └── routes/               # Endpoints de la API (Fase 3)
│   │       └── __init__.py
│   │
│   ├── database/                 # Archivos de base de datos generados
│   │   └── seeds/                # Archivos CSV y PNG generados (datos históricos)
│   │
│   └── migrations/               # Migraciones de base de datos (Alembic)
│       ├── env.py                # Configuración del entorno Alembic
│       ├── script.py.mako        # Plantilla para nuevas migraciones
│       └── versions/             # Historial de migraciones versionadas
│           └── 001_initial.py    # Migración inicial: creación de 10 tablas + índices
│
└── frontend/                     # Servicio de frontend (Fase 3)
```

---

## Descripción de Componentes

### Archivos de Configuración

| Archivo | Descripción |
|---------|-------------|
| `.env` | Contiene las variables de entorno: credenciales de PostgreSQL, clave secreta para JWT (incluido en `.gitignore`).
| `.gitignore` | Define qué archivos y carpetas Git debe ignorar. Incluye `.env`, `__pycache__`, CSVs generados y visualizaciones. |
| `docker-compose.yml` | Define los servicios del sistema: base de datos PostgreSQL y backend FastAPI. Configura redes, volúmenes y variables de entorno. |

### Documentación (document/)

| Archivo | Descripción |
|---------|-------------|
| `informe_fase1.md` | Informe teórico que documenta la fundamentación metodológica del proyecto: ciclos de vida CRISP-DM y TDSP, justificación del uso de datos sintéticos, selección de PostgreSQL, y diseño de la arquitectura de datos. |

### Backend (API REST)

| Archivo | Descripción |
|---------|-------------|
| `Dockerfile` | Instrucciones para construir la imagen Docker del backend. Instala dependencias Python, cliente PostgreSQL y expone el puerto 8000. |
| `entrypoint.sh` | Script de inicio: espera a PostgreSQL, ejecuta migraciones de Alembic, verifica si hay datos vía ORM, genera y carga datos históricos si es necesario, genera visualizaciones y lanza la API con Uvicorn. |
| `requirements.txt` | Lista todas las dependencias Python: FastAPI, SQLAlchemy, Alembic, pandas, numpy, matplotlib, seaborn, entre otras. |
| `alembic.ini` | Configuración de Alembic para gestionar migraciones de la base de datos. |

### Aplicación (app/)

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Punto de entrada de la API FastAPI. Crea la aplicación y define rutas básicas de salud del sistema. No crea tablas automáticamente; utiliza exclusivamente migraciones de Alembic. |
| `config.py` | Configuración centralizada usando Pydantic Settings. Lee las variables de entorno desde `.env`. |
| `database.py` | Configura la conexión a PostgreSQL usando SQLAlchemy. Define el motor de base de datos y la sesión local. |

### Modelos (models/)

| Archivo | Descripción |
|---------|-------------|
| `models.py` | Define 10 tablas SQLAlchemy: Provincia, Municipio, Producto, AlmacenCentral, PuntoVenta, Inventario, Asignacion, EntradaMercancia, Merma y PerdidaTransporte. Utiliza campo `fecha` (Date) para series temporales. |

### Seed Data (seed/)

| Archivo | Descripción |
|---------|-------------|
| `config.py` | Contiene los parámetros de configuración de 8 productos alimentarios (arroz, aceite, frijoles, azúcar, harina, pollo, cerdo, huevos) con sus tasas de consumo, mermas y factores estacionales. También incluye la estructura geográfica de Cuba con 16 provincias y sus municipios. |
| `generator.py` | Script que genera 15 años de datos históricos (2011-2026) para inventarios, entradas de mercancía, mermas, asignaciones y pérdidas por transporte. Utiliza campo `fecha` (Date) para series temporales. |
| `loader.py` | Script que carga los archivos CSV generados a PostgreSQL utilizando SQLAlchemy ORM. Las tablas deben existir previamente (creadas por Alembic). Ejecuta la inserción por lotes para optimizar el rendimiento. |

### Migraciones (migrations/)

| Archivo | Descripción |
|---------|-------------|
| `env.py` | Configuración del entorno Alembic. Conecta a PostgreSQL y carga los modelos SQLAlchemy para detectar cambios. |
| `script.py.mako` | Plantilla para generar nuevas migraciones. Define la estructura básica de cada archivo de migración. |
| `versions/001_initial.py` | Migración inicial que crea las 10 tablas del sistema con sus restricciones, claves foráneas e índices. Este archivo está versionado en Git. |

### Analytics (analytics/)

| Archivo | Descripción |
|---------|-------------|
| `metrics.py` | Implementa 4 métricas analíticas: velocidad de rotación de inventario, detección de patrones estacionales, cálculo de nivel de stock crítico y generación de alertas de desabastecimiento. Ejecutable via `python -m app.analytics.metrics`. |
| `visualization.py` | Genera visualizaciones: mapas de calor de inventarios por municipio, matriz de estado crítico y gráficos de tendencia temporal. Utiliza matplotlib y seaborn. Ejecutable via `python -m app.analytics.visualization`. |

---

## Modelo de Datos

El sistema utiliza 10 tablas relacionadas creadas mediante migraciones de Alembic:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│  Provincias │────▶│  Municipios │────▶│ Puntos de Venta │
└─────────────┘     └─────────────┘     └─────────────────┘
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐     ┌─────────────────┐
                    │ Almacenes   │────▶│  Asignaciones   │
                    │  Centrales  │     └─────────────────┘
                    └─────────────┘              │
                           │                    ▼
                           │            ┌─────────────────┐
                           │            │   Productos     │
                           │            └─────────────────┘
                           │                     │
                           ▼                     ▼
                    ┌─────────────┐     ┌─────────────────┐
                    │  Inventarios│◀────│  Entradas       │
                    └─────────────┘     │  Mercancía      │
                           │            └─────────────────┘
                           ▼
                    ┌─────────────┐     ┌─────────────────┐
                    │   Mermas    │     │  Pérdidas por   │
                    │             │     │  Transporte     │
                    └─────────────┘     └─────────────────┘
```

---

## Instrucciones de Instalación y Ejecución

### Requisitos Previos

- Docker Desktop instalado y en ejecución
- Conexión a internet (para descargar imágenes Docker)
- Mínimo 4GB de RAM disponible para Docker

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/USUARIO/alimendata.git
cd alimendata
```

### Paso 2: Configurar Variables de Entorno


### Paso 3: Levantar el Sistema Completo

Un solo comando construye las imágenes, levanta todos los servicios y ejecuta el pipeline completo automáticamente:

```bash
docker-compose up --build
```

El `entrypoint.sh` se encargará automáticamente de:

1. Esperar a que PostgreSQL esté listo
2. Ejecutar las migraciones de Alembic (`alembic upgrade head`)
3. Verificar si la base de datos tiene datos (vía ORM, sin raw SQL)
4. Si está vacía: generar datos históricos (15 años), cargarlos a PostgreSQL y generar visualizaciones
5. Lanzar la API FastAPI en `http://localhost:8000`

En ejecuciones posteriores, si ya hay datos, el pipeline los detecta y salta la ingesta, iniciando directamente la API.

---

## Proceso de Migraciones (Alembic)

El sistema utiliza exclusivamente migraciones de Alembic para gestionar el esquema de la base de datos. Esto cumple con la directriz 1.2 que prohíbe las inicializaciones manuales.

### Flujo de Trabajo

1. **Migración inicial:** El archivo `001_initial.py` crea las 10 tablas del sistema
2. **Ejecución automática:** El `entrypoint.sh` ejecuta `alembic upgrade head` al iniciar el contenedor
3. **Versionado:** Cada cambio en el esquema se registra como una nueva migración en `versions/`

### Generar Nuevas Migraciones

Si se modifican los modelos SQLAlchemy, se debe generar una nueva migración:

```bash
docker-compose run --rm backend alembic revision --autogenerate -m "descripción del cambio"
docker-compose run --rm backend alembic upgrade head
```

### Verificar Estado de Migraciones

```bash
docker-compose run --rm backend alembic current
docker-compose run --rm backend alembic history
```

---

## Métricas Analíticas Implementadas

### 1. Velocidad de Rotación de Inventario

Calcula la relación entre el inventario actual y el promedio histórico. Indica qué tan rápido se mueve un producto en un punto de venta específico.

### 2. Detección de Patrones Estacionales

Analiza el comportamiento histórico de un producto por mes para identificar períodos recurrentes de escasez o abundancia.

### 3. Nivel de Stock Crítico

Determina el estado del inventario basándose en días de stock restante:
- **Crítico:** Menos de 7 días de stock
- **Alerta:** Entre 7 y 15 días de stock
- **Normal:** Entre 15 y 30 días de stock
- **Suficiente:** Más de 30 días de stock

### 4. Alertas de Desabastecimiento

Genera una lista prioritaria de puntos de venta con productos en estado crítico o de alerta, ordenada por urgencia.

---

## Visualización

El sistema genera automáticamente:

- **Mapas de calor** que muestran la distribución de inventarios por municipio y mes
- **Gráficos de tendencia** que ilustran el comportamiento temporal de los productos

Los archivos de visualización se almacenan en `backend/database/seeds/`.

---

## Tecnologías Utilizadas

| Capa | Tecnología |
|------|------------|
| Backend | FastAPI 0.104.1 |
| ORM | SQLAlchemy 2.0.23 |
| Migraciones | Alembic 1.13.0 |
| Base de Datos | PostgreSQL 15 |
| Análisis de Datos | pandas 2.1.4, numpy 1.26.2 |
| Visualización | matplotlib 3.8.2, seaborn 0.13.0 |
| Contenerización | Docker, docker-compose |
| Validación | Pydantic 2.5.2 |

---

## License

Proyecto académico - Universidad de Ciencias de Datos, Cuba 2025-2026
