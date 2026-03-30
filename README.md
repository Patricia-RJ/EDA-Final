# EDA e-commerce OLIST

Realización de el Análisis Exploratorio de los Datos relacionados con campañas de marketing directo de una institución bancaria portuguesa.
El objetivo es:

- Limpiar y transformar los datos
- Analizar patrones y relaciones
- Visualizar información relevante
- Extraer conclusiones fundamentadas
- Construir un modelo sencillo de Machine Learning
- Presentar los resultados mediante un dashboard en Power BI

El proyecto sigue una estructura profesional basada en buenas prácticas de organización, control de versiones y separación por fases.

---

## 1. Tecnologías Utilizadas

- Python 3.11
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook
- Power BI (Dashboard)
- Anaconda (gestión de entornos)
- Git & GitHub
- Streamlit
- XGBoost

---

## 2. Metodología de Trabajo

El proyecto se desarrolla siguiendo una metodología estructurada basada en ramas de Git para simular un entorno profesional.

### Estrategia de ramas

```
main
 └── dev
      ├── feature/data-cleaning
      ├── feature/eda-ml
      └──  feature/dashboard-eda-clean

```

### Función de cada rama

- **main**  
  Contiene la versión final estable lista para entrega o despliegue.

- **dev**  
  Rama de integración donde se unifican todas las funcionalidades antes de pasar a producción.

- **feature/data-cleaning**  
  Desarrollo de la limpieza, tratamiento de valores nulos, duplicados y transformación de variables.

- **feature/eda-analysis**  
  Implementación del análisis estadístico y exploratorio.

- **feature/dashboard-eda-clean**  
  Desarrollo de los dashboards de Power BI y Streamlit y además se han añadido algunos documentos de la fase de eda-analyis

Esta estructura permite mantener el proyecto organizado, escalable y fácil de mantener.

---
## 3. Estructura del Proyecto

```
EDA-FINAL/
│
├── dashboard/
│ ├── streamlit/
│ │ └── dashboard.py
│ └── Olist_dashboard.pbix
│
├── data/
│ ├── processed/
│ │ └── olist_final_dataset.csv
│ └── raw/
│ ├── olist_customers_dataset.csv
│ ├── olist_order_items_dataset.csv
│ ├── olist_order_payments_dataset.csv
│ ├── olist_order_reviews_dataset.csv
│ ├── olist_orders_dataset.csv
│ ├── olist_product_category_name_translation.csv
│ ├── olist_products_dataset.csv
│ └── olist_sellers_dataset.csv
│
├── docs/
│ ├── br_states.geojson
│ ├── brazil_geo.json
│ └── Informe Olist.pdf
│
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ └── 02_eda_analysis_ml.ipynb
│
├── visuals/
│ ├── olist.jpg
│ └── xx_olist_model.png
│
├── README.md
└── requirements.txt
```

---

## 4. Fase de limpieza y transformación de datos

El proceso de limpieza y transformación se ha llevado a cabo en el notebook:

 `01_data_cleaning.ipynb`

En esta fase se ha construido un dataset final a partir de múltiples fuentes de datos del ecosistema Olist. Las principales tareas realizadas han sido:

- **Unificación de datasets** mediante joins entre tablas clave (pedidos, clientes, productos, pagos, etc.)
- **Tratamiento de valores nulos**, analizando su impacto y aplicando imputaciones o eliminaciones cuando era necesario
- **Eliminación de duplicados** para garantizar la integridad de los datos
- **Conversión de tipos de datos**, especialmente en variables temporales (fechas)
- **Creación de nuevas variables (feature engineering)**, como:
  - `delivery_time_days`
  - `delivery_delay`
  - `delay_flag`
  - `year_month`
- **Estandarización de nombres y formatos** para facilitar el análisis posterior

El resultado de esta fase es un dataset limpio, consistente y preparado para el análisis y modelado.

---

##  5. Análisis Exploratorio de Datos (EDA)

El análisis exploratorio se ha desarrollado en el notebook:

`02_eda_analysis_ml.ipynb`

En esta fase se han analizado los datos con el objetivo de entender patrones de comportamiento, tendencias y relaciones entre variables.

Principales análisis realizados:

- **Análisis de ventas**:
  - evolución temporal de pedidos
  - ingresos totales y ticket medio

- **Análisis logístico**:
  - tiempos de entrega
  - impacto de los retrasos (`delivery_delay`) en el negocio

- **Análisis de clientes**:
  - número de clientes únicos
  - clientes recurrentes
  - comportamiento de compra

- **Análisis de satisfacción**:
  - distribución de `review_score`
  - relación entre retrasos y valoraciones

- **Análisis por categorías y geográfico**:
  - rendimiento por categoría de producto
  - distribución por estados/regiones

Este análisis ha permitido identificar los principales factores que afectan a la satisfacción del cliente y al rendimiento del negocio.

---

## 6. Modelo de Machine Learning

Dentro del mismo notebook:

 `02_eda_analysis_ml.ipynb`

se ha desarrollado un modelo básico de Machine Learning con el objetivo de:

 **Predecir la valoración (`review_score`) de un pedido**

### Enfoque del modelo

- Se ha definido una variable objetivo (`target`) basada en la satisfacción del cliente
- Se han seleccionado variables relevantes como:
  - retraso en la entrega (`delivery_delay`)
  - tiempos de envío
  - características del pedido

### Proceso seguido:

- Preparación de los datos para modelado
- División en conjunto de entrenamiento y test
- Entrenamiento de un modelo de clasificación
- Evaluación del modelo mediante métricas básicas

### Conclusiones del modelo

El modelo muestra que:

- El **retraso en la entrega** es uno de los factores más determinantes en la satisfacción
- Variables operativas (logística) tienen mayor peso que variables demográficas
- Existe un claro patrón entre experiencia de entrega y valoración del cliente

Este modelo sirve como primera aproximación para entender cómo predecir la satisfacción del cliente y puede ser mejorado con técnicas más avanzadas.

---
## 7. Visualizaciones y Dashboards

La fase de visualización tiene como objetivo transformar los datos analizados en información clara, visual e interpretable para la toma de decisiones.

Se han utilizado dos herramientas principales:

- **Power BI** → dashboard principal
- **Streamlit** → dashboard interactivo en Python

---

### Dashboard en Power BI

Archivo:  
`dashboard/Olist_dashboard.pbix`

Se ha desarrollado un dashboard estructurado en varias secciones clave:

#### Ventas
- Evolución temporal de ingresos
- Número de pedidos
- Ticket medio
- Tendencias de crecimiento

#### Logística
- Tiempo medio de entrega
- Análisis de retrasos (`delivery_delay`)
- Porcentaje de pedidos retrasados
- Impacto de la logística en el servicio

#### Clientes
- Número de clientes únicos
- Clientes recurrentes
- Porcentaje de recurrencia
- Comportamiento de compra

#### Satisfacción
- Distribución de valoraciones (`review_score`)
- Relación entre retrasos y satisfacción
- Identificación de factores críticos en la experiencia del cliente

El dashboard permite filtrar por variables como tiempo, ubicación o tipo de producto, facilitando un análisis dinámico.

---

### Dashboard en Streamlit

Archivo:  
`dashboard/streamlit/dashboard.py`

Enlace web del dashboard: 
https://eda-final-l2srvjde5chtrlz2syx4nl.streamlit.app/ 

Se ha desarrollado una aplicación interactiva en Streamlit que permite:

- Visualizar métricas clave en tiempo real
- Explorar datos de forma interactiva
- Analizar clientes, ventas y satisfacción
- Navegar entre distintas secciones del negocio

Este dashboard complementa el de Power BI y aporta una visión más flexible y programática del análisis.

---

###  Visualizaciones utilizadas

Durante el análisis se han utilizado diferentes tipos de gráficos para representar la información:

- Gráficos de líneas → evolución temporal
- Gráficos de barras → comparaciones entre categorías
- Mapas → distribución geográfica
- Gráficos de dispersión → relación entre variables
- Indicadores KPI → métricas clave del negocio

---

###  Objetivo de los dashboards

Los dashboards han sido diseñados para:

- Facilitar la interpretación de los datos
- Detectar patrones y problemas del negocio
- Apoyar la toma de decisiones estratégicas
- Traducir el análisis técnico en insights accionables

---
## 8. Configuración del Entorno

### Crear entorno virtual

```bash
conda create -n hackio python=3.11
conda activate hackio
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install pandas matplotlib seaborn scikit-learn jupyter
```

---

## 9. Ejecución del Proyecto

1. Clonar repositorio:

```bash
git clone <url_del_repositorio>
cd eda-proyecto
```

2. Activar entorno:

```bash
conda activate hackio
```

3. Ejecutar notebooks en orden:

- 01_data_cleaning  
- 02_eda_analysis  
- 03_ml_model

---

## 10. Informe Final

El proyecto incluye un informe técnico en Word que contiene:

- Contexto y objetivo del análisis
- Proceso de limpieza y decisiones tomadas
- Resultados del análisis exploratorio
- Interpretación de visualizaciones
- Resultados del modelo de Machine Learning
- Conclusiones y recomendaciones

Ubicación:

```
docs/Informe Olist.pdf
```

---
## 11. Recursos Extras
Recusos para crear mapas:
```
docs/br_states.geojson
docs/brazil_geo.json
```
Recursos visuales
```
visuals/XX_olist_model.png
visuals/olist.jpg
```

---
## Autora

Patricia Romo Jiménez
