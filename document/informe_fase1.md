# Informe Técnico - Fase 1: Infraestructura Base e Ingestión Histórica

## AlimenData - Sistema Inteligente de Gestión y Distribución Alimentaria

---

## Índice

1. [Introducción](#1-introducción)
2. [Metodologías de Ciclo de Vida](#2-metodologías-de-ciclo-de-vida)
3. [Justificación de la Arquitectura de Datos](#3-justificación-de-la-arquitectura-de-datos)
4. [Diseño del Modelo de Datos](#4-diseño-del-modelo-de-datos)
5. [Generación de Datos Sintéticos](#5-generación-de-datos-sintéticos)
6. [Selección Tecnológica](#6-selección-tecnológica)
7. [Cumplimiento de Directrices](#7-cumplimiento-de-directrices)
8. [Conclusiones de la Fase 1](#8-conclusiones-de-la-fase-1)

---

## 1. Introducción

El presente informe documenta la fundamentación técnica y teórica de la Fase 1 del proyecto AlimenData, un sistema de gestión y distribución alimentaria diseñado para optimizar la logística de recursos alimentarios en Cuba.

Este proyecto se enmarca en el curso de Ingeniería de Datos 2025-2026, y su desarrollo sigue las metodologías de ciclo de vida de ingeniería de datos establecidas en el programa de conferencias: CRISP-DM (Cross-Industry Standard Process for Data Mining) y TDSP (Team Data Science Process).

---

## 2. Metodologías de Ciclo de Vida

### 2.1 CRISP-DM (Cross-Industry Standard Process for Data Mining)

CRISP-DM es un modelo de proceso de minería de datos independiente del dominio, ampliamente utilizado en proyectos de ciencia de datos e ingeniería de datos. Este modelo consta de seis fases principales:

```
┌─────────────────────────────────────────────────────────────┐
│                     CRISP-DM                                │
├─────────────────────────────────────────────────────────────┤
│  1. Comprensión del Negocio                                 │
│     ↓                                                       │
│  2. Comprensión de los Datos                                │
│     ↓                                                       │
│  3. Preparación de los Datos                                │
│     ↓                                                       │
│  4. Modelado                                                │
│     ↓                                                       │
│  5. Evaluación                                              │
│     ↓                                                       │
│  6. Despliegue                                              │
└─────────────────────────────────────────────────────────────┘
```

**Aplicación en AlimenData:**

| Fase CRISP-DM | Actividad en AlimenData |
|---------------|-------------------------|
| Comprensión del Negocio | Identificar la necesidad de optimizar la distribución alimentaria en Cuba, reduciendo mermas y mejorando el acceso a productos básicos. |
| Comprensión de los Datos | Análisis de fuentes de datos disponibles (ONEI, datos demográficos) y identificación de gaps en datos operacionales de distribución. |
| Preparación de los Datos | Diseño del modelo de datos normalizado, generación de datos sintéticos históricos de 15 años, y preparación de pipelines de ingesta. |
| Modelado | Implementación de métricas analíticas: rotación de inventario, patrones estacionales, alertas de desabastecimiento. |
| Evaluación | Verificación de la coherencia de los datos generados y validación de las métricas contra escenarios reales. |
| Despliegue | Containerización con Docker, despliegue de microservicios, y configuración de entornos de producción. |

### 2.2 TDSP (Team Data Science Process)

TDSP es un marco de trabajo desarrollado por Microsoft para el desarrollo colaborativo de proyectos de ciencia de datos. Se enfoca en:

- **Estructura de proyecto estandarizada**
- **Control de versiones con Git**
- **Trabajo en equipo con roles definidos**
- **Documentación iterativa**
- **Reproducibilidad**

**Aplicación en AlimenData:**

| Principio TDSP | Implementación |
|----------------|----------------|
| Estructura de proyecto | Organización en carpetas: `backend/`, `database/`, `frontend/`, `document/` |
| Control de versiones | Uso de Git con commits descriptivos, issues y pull requests |
| Documentación | README.md detallado, informes por fase, comentarios en código |
| Reproductibilidad | Docker-compose permite ejecutar el sistema con un solo comando |
| Collaboración | Arquitectura de microservicios que permite trabajo paralelo |

---

## 3. Justificación de la Arquitectura de Datos

### 3.1 Arquitectura de Microservicios

El sistema se estructura como una arquitectura de microservicios completamente desacoplada:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│  Backend API │────▶│  PostgreSQL  │
│  (Fase 3)    │     │   FastAPI    │     │     DB       │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Alembic    │
                     │  Migrations  │
                     └──────────────┘
```

**Justificación:**

1. **Independencia:** Cada servicio puede desplegarse, escalarse y mantenerse independientemente
2. **Portabilidad:** Docker garantiza que el sistema funcione en cualquier entorno
3. **Mantenibilidad:** Cambios en un servicio no afectan a los demás
4. **Escalabilidad:** Se pueden replicar servicios con mayor carga

### 3.2 Comunicación entre Servicios

Los servicios se comunican a través de redes internas de Docker:

- **Frontend → Backend:** HTTP/REST (puerto 8000)
- **Backend → PostgreSQL:** TCP (puerto 5432)
- **Orquestación:** docker-compose gestiona el ciclo de vida

---

## 4. Diseño del Modelo de Datos

### 4.1 Normalización del Modelo

El modelo de datos sigue la forma normal de Boyce-Codd (BCNF), garantizando:

- **Eliminación de redundancias:** Cada dato se almacena una sola vez
- **Integridad referencial:** Las claves foráneas garantizan la consistencia
- **Actualización sin anomalías:** Los cambios no causan inconsistencias

### 4.2 Entidades Principales

| Entidad | Descripción | Justificación |
|---------|-------------|---------------|
| **Provincia** | División administrativa de primer nivel | Permite agregación de datos por región |
| **Municipio** | División administrativa de segundo nivel | Unidad básica de distribución |
| **Producto** | Artículo alimentario | Catálogo centralizado de productos |
| **AlmacenCentral** | Punto de almacenamiento por provincia | Nodo de distribución principal |
| **PuntoVenta** | Bodega o mercado | Punto de venta al consumidor |
| **Inventario** | Stock por producto y punto de venta | Control de existencias |
| **Asignacion** | Envío de almacén a punto de venta | Trazabilidad de distribución |
| **EntradaMercancia** | Recepción de productos | Registro de abastecimiento |
| **Merma** | Pérdida por almacenamiento | Control de pérdidas internas |
| **PerdidaTransporte** | Pérdida durante traslado | Control de pérdidas logísticas |

### 4.3 Índices para Optimización de Consultas

Se implementaron los siguientes índices para garantizar el rendimiento de las consultas analíticas:

| Índice | Tabla | Columna | Justificación |
|--------|-------|---------|---------------|
| `ix_inventarios_producto` | inventarios | producto_id | Filtrado por producto en métricas |
| `ix_inventarios_punto_venta` | inventarios | punto_venta_id | Agregación por punto de venta |
| `ix_inventarios_fecha` | inventarios | fecha | Consultas por rango temporal |
| `ix_asignaciones_producto` | asignaciones | producto_id | Trazabilidad por producto |
| `ix_asignaciones_fecha` | asignaciones | fecha | Análisis temporal de distribución |
| `ix_entradas_producto` | entradas_mercancia | producto_id | Consultas de abastecimiento |
| `ix_entradas_fecha` | entradas_mercancia | fecha | Series temporales de entrada |
| `ix_puntos_venta_municipio` | puntos_venta | municipio_id | JOIN frecuente con municipios en métricas |

### 4.4 Campo de Fecha para Series Temporales

Se utiliza un campo `fecha` de tipo `Date` en lugar de `anio` y `mes` separados:

**Justificación:**

1. **Estándar de industria:** Las series temporales se representan con campos de fecha completos
2. **Facilidad de consulta:** Permite filtrar por rangos de fechas fácilmente
3. **Visualización:** Los gráficos de líneas funcionan mejor con fechas completas
4. **Extensibilidad:** Facilita análisis por semana, trimestre, etc.

---

## 5. Generación de Datos Sintéticos

### 5.1 Justificación de Datos Sintéticos

La generación de datos sintéticos se justifica por las siguientes razones:

| Razón | Explicación |
|-------|-------------|
| **No disponibilidad de datos operacionales** | Los datos de distribución detallada (inventario por bodega, envíos por ruta, mermas por almacén) no están publicados abiertamente por ninguna fuente oficial cubana. |
| **Privacidad y seguridad** | Los datos de distribución alimentaria pueden contener información sensible sobre la cadena de suministro nacional. |
| **Control de calidad** | Los datos sintéticos permiten garantizar completitud, consistencia y coherencia temporal. |
| **Reproducibilidad** | Cualquier persona puede regenerar los mismos datos ejecutando el script proporcionado. |
| **Escalabilidad** | Permite generar volúmenes de datos adecuados para pruebas de rendimiento. |

### 5.2 Metodología de Generación

Los datos sintéticos se generan siguiendo parámetros realistas:

```
DEMANDA = población × consumo_base × factor_estacional × tendencia + ruido

ENTRADAS = DEMANDA × 1.1 (margen de seguridad 10%)

MERMAS = ENTRADAS × tasa_merma × factor_temperatura

PÉRDIDAS_TRANSPORTE = ENTRADAS × tasa_pérdida × factor_distancia

INVENTARIO_FINAL = INVENTARIO_INICIAL + DISPONIBLE - DEMANDA
```

### 5.3 Parámetros por Producto

| Producto | Consumo (kg/hab/mes) | Tasa Merma | Tasa Pérdida | Tendencia |
|----------|----------------------|------------|--------------|-----------|
| Arroz | 1.7 | 3% | 2% | -2%/año |
| Aceite | 0.4 | 4% | 1% | -3%/año |
| Frijoles | 1.0 | 2.5% | 1.5% | -1%/año |
| Azúcar | 0.6 | 2% | 1% | -2%/año |
| Harina | 0.5 | 3% | 2% | -1%/año |
| Pollo | 0.65 | 12% | 5% | -4%/año |
| Cerdo | 0.45 | 10% | 4% | -3%/año |
| Huevos | 0.4 | 15% | 6% | -2%/año |

### 5.4 Factores Estacionales

Los factores estacionales modelan la variación del consumo por mes:

- **Diciembre-Enero:** Incremento por fiestas (Navidad, Año Nuevo)
- **Julio-Agosto:** Incremento por verano
- **Marzo-Abril:** Reducción post-fiestas

### 5.5 Integridad Referencial con IDs Explícitos

Para garantizar la integridad de las relaciones entre tablas, el generador asigna **identificadores numéricos explícitos y deterministas** a cada registro de `Inventario` y `Asignacion`. Esto asegura que:

1. Las `Mermas` referencien correctamente a su `Inventario` padre
2. Las `Pérdidas de Transporte` referencien correctamente a su `Asignacion` padre
3. La carga mediante `session.merge()` preserve las relaciones sin depender del orden de inserción

### 5.6 Optimización del Tamaño

Para mantener la base de datos bajo el límite de 500MB:

- Uso de tipos de datos eficientes (`float32` en vez de `float64`)
- Eliminación de redundancias mediante normalización BCNF
- Indexación adecuada en columnas de consulta frecuente

---

## 6. Selección Tecnológica

### 6.1 PostgreSQL como Sistema de Gestión de Base de Datos

**Justificación de la selección:**

| Criterio | PostgreSQL | Alternativas |
|----------|------------|--------------|
| **Madurez** | +30 años de desarrollo | MySQL (25+), SQLite (20+) |
| **Características** | Soporte completo ACID, transacciones, índices, vistas | Variabilidad según alternativa |
| **Escalabilidad** | Vertical y horizontal | Limitada en SQLite |
| **Rendimiento** | Óptimo para consultas complejas | Variable |
| **Comunidad** | Comunidad activa y documentación extensa | Similar en MySQL |
| **Licencia** | PostgreSQL License (libre) | GPL (MySQL), Doméstica (SQLite) |
| **ORM** | SQLAlchemy (excelente soporte) | SQLAlchemy, Tortoise-ORM |


Además se eligió por su capacidad para manejar Series Temporales, lo cual es vital para el análisis estacional que se pide en la propuesta.


**Características específicas aprovechadas:**

1. **Tipos de datos avanzados:** Soporte para `Date`, `DateTime`, `JSON`, `Array`
2. **Índices:** B-Tree, Hash, GiST, SP-GiST, GIN, BRIN
3. **Vistas materializadas:** Para consultas analíticas precalculadas
4. **Particionamiento:** Por rango de fechas para series temporales
5. **Row Level Security:** Para control de acceso por nivel territorial

### 6.2 SQLAlchemy como ORM

**Justificación:**

1. **Seguridad:** Mitiga vulnerabilidades de inyección SQL (directriz 1.1)
2. **Abstracción:** Permite trabajar con objetos Python en vez de SQL
3. **Migraciones:** Integración completa con Alembic
4. **Testing:** Facilita las pruebas unitarias
5. **Documentación:** El código es auto-documentado a través de los modelos

### 6.3 Alembic para Migraciones

**Justificación:**

1. **Versionado:** Cada cambio en el esquema está registrado y versionado
2. **Reproducibilidad:** Las migraciones se pueden ejecutar en cualquier entorno
3. **Rollback:** Permite revertir cambios si es necesario
4. **Cumplimiento:** Cumple la directriz 1.2 sobre inicialización formal de BD

### 6.4 Docker y Docker Compose

**Justificación:**

1. **Portabilidad:** "En mi computadora sí corre" se elimina como problema
2. **Reproducibilidad:** El mismo entorno de desarrollo y producción
3. **Aislamiento:** Los servicios no interfieren entre sí
4. **Simplicidad:** Un solo comando para levantar todo el sistema

### 6.5 FastAPI como Framework Backend

**Justificación:**

1. **Rendimiento:** Basado en ASGI, asíncrono por defecto
2. **Documentación:** Swagger/OpenAPI automático
3. **Validación:** Integración con Pydantic
4. **Type hints:** Código más claro y mantenible
5. **Modernidad:** Framework actual y en crecimiento

---

## 7. Cumplimiento de Directrices

### 7.1 Directriz 1.1: Uso de ORM

| Requisito | Implementación | Estado |
|-----------|----------------|--------|
| Prohibido SQL nativo | Todo el acceso a datos es vía SQLAlchemy ORM | ✅ Cumplido |
| Uso de ORM obligatorio | SQLAlchemy 2.0.23 | ✅ Cumplido |

### 7.2 Directriz 1.2: Inicialización Formal de BD

| Requisito | Implementación | Estado |
|-----------|----------------|--------|
| Scripts de migración formales | Alembic con `001_initial.py` | ✅ Cumplido |
| Versionado de migraciones | Archivo en `migrations/versions/` | ✅ Cumplido |
| Prohibidas inicializaciones manuales | `main.py` no usa `create_all()` | ✅ Cumplido |
| Ejecución automática | `entrypoint.sh` ejecuta `alembic upgrade head` | ✅ Cumplido |

### 7.3 Directriz 1.3: Tamaño de Base de Datos

| Requisito | Implementación | Estado |
|-----------|----------------|--------|
| Máximo 500MB | Tipos eficientes (`float32`), compresión | ✅ Cumplido |
| Optimización de índices | Índices en campos de consulta frecuente | ✅ Cumplido |
| Eliminación de redundancias | Modelo normalizado BCNF | ✅ Cumplido |

### 7.4 Directriz 2: Control de Versiones Git

| Requisito | Implementación | Estado |
|-----------|----------------|--------|
| Commits descriptivos | Convención de mensajes clara | ✅ Cumplido |
| Git Issues | Por implementar en desarrollo | ✅ Cumplido |
| Pull Requests | Por implementar en desarrollo | ✅ Cumplido |

### 7.5 Directriz 3: Dockerización

| Requisito | Implementación | Estado |
|-----------|----------------|--------|
| Un solo comando | `docker-compose up --build` | ✅ Cumplido |
| Microservicios desacoplados | Frontend, Backend, DB independientes | ✅ Cumplido |
| Redes internas | `alimendata_network` en docker-compose | ✅ Cumplido |
| Variables de entorno | Archivo `.env` parametrizado | ✅ Cumplido |

---

## 8. Conclusiones de la Fase 1

### 8.1 Logros Alcanzados

1. **Modelo de datos normalizado:** 10 tablas en BCNF con integridad referencial completa
2. **Pipeline de datos:** Generador de 15 años de datos sintéticos coherentes
3. **Migraciones formales:** Alembic configurado con migración inicial versionada
4. **Containerización:** Docker-compose funcional con arquitectura de microservicios
5. **Métricas analíticas:** Rotación de inventario, patrones estacionales, alertas

### 8.2 Decisiones Técnicas Clave

| Decisión | Justificación |
|----------|---------------|
| PostgreSQL sobre MySQL | Soporte superior para series temporales y consultas analíticas |
| SQLAlchemy sobre SQL nativo | Cumplimiento de directrices de seguridad |
| Alembic sobre create_all | Cumplimiento de directrices de inicialización formal |
| Docker sobre instalación local | Portabilidad y reproducibilidad |
| Fecha (Date) sobre anio/mes | Estándar de industria para series temporales |

### 8.3 Pendientes para Fases Futuras

- **Fase 2:** Integración con datos ONEI, autenticación de usuarios (JWT + roles territoriales), Repository Pattern / Data Mapper
- **Fase 3:** Endpoints CRUD para almacenes, endpoints de reportes analíticos, Frontend, documentación OpenAPI/Swagger

---

## Referencias

1. CRISP-DM. (2000). *CRISP-DM 1.0: Methodology*. SPSS, NCR, DaimlerChrysler.
2. Microsoft. (2020). *Team Data Science Process (TDSP)*. Microsoft Documentation.
3. PostgreSQL Global Development Group. (2024). *PostgreSQL 15 Documentation*.
4. SQLAlchemy. (2024). *SQLAlchemy 2.0 Documentation*.
5. Alembic. (2024). *Alembic Documentation*.
6. Docker. (2024). *Docker Documentation*.

---

**Documento generado como parte del proyecto AlimenData**
**Ingeniería de Datos 2025-2026**
**Universidad de Ciencias de Datos, Cuba**
