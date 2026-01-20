# 📊 Bank Marketing – Análisis Exploratorio de Datos (EDA)

## 📌 Descripción del proyecto

Este proyecto consiste en el desarrollo de una aplicación interactiva en Streamlit para realizar un Análisis Exploratorio de Datos (EDA) sobre el dataset Bank Marketing.

El objetivo principal es comprender el comportamiento de los clientes y analizar los factores que influyen en la aceptación de campañas de marketing bancario, cuya variable objetivo es:

**y = yes / no**

La aplicación permite:

- Cargar datasets en formato CSV
- Analizar variables numéricas y categóricas
- Visualizar distribuciones y relaciones entre variables
- Evaluar segmentaciones por tasa de aceptación
- Obtener insights estadísticos mediante gráficos interactivos

El proyecto no construye modelos predictivos, ya que el enfoque está centrado exclusivamente en el EDA.

## 🧰 Tecnologías utilizadas

- Python 3.11
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn

## 📁 Estructura del proyecto

```
DMC/
│
├── app.py
├── BankMarketing.csv
├── README.md
└── requirements.txt
```

## 🖥️ Funcionalidades de la aplicación

La aplicación está organizada en tres módulos principales:

### 🏠 Home

- Descripción del proyecto
- Objetivo del análisis
- Información general del dataset
- Tecnologías utilizadas

### 📥 Carga del Dataset

- Carga dinámica del archivo .csv
- Detección automática de separadores (; o ,)
- Vista previa del dataset
- Información básica de columnas y dimensiones

### 🔎 EDA – Análisis Exploratorio

Incluye los siguientes 10 ítems obligatorios:

1. Información general del dataset (info)
2. Clasificación de variables (numéricas vs categóricas)
3. Estadísticas descriptivas
4. Análisis de valores faltantes
5. Histogramas de variables numéricas
6. Distribución de variables categóricas
7. Análisis bivariado (numérico vs categórico)
8. Tablas cruzadas entre variables categóricas
9. Matriz de correlación
10. Tasa de aceptación por segmento

## 📸 Capturas de la aplicación

### 🔹 Home

![Home](/screenshots/home.png)

### 🔹 Carga del dataset

![Upload](/screenshots/upload.png)

### 🔹 Análisis Exploratorio (EDA)

![EDA](/screenshots/eda.png)

> 💡 **Sugerencia:** Toma las capturas con la app ejecutándose y guárdalas en una carpeta `/screenshots`.

## ▶️ Instrucciones de ejecución

### 1️⃣ Crear entorno virtual (opcional)

```bash
python -m venv venv
```

**Activar:**

- **Windows**

```bash
  venv\Scripts\activate
```

- **Linux / Mac**

```bash
  source venv/bin/activate
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install streamlit pandas numpy matplotlib seaborn
```

### 3️⃣ Ejecutar la aplicación

```bash
streamlit run app.py
```

### 4️⃣ Abrir en el navegador

```
http://localhost:8501
```

## 📊 Dataset utilizado

**Bank Marketing Dataset**

Variables incluidas:

- Datos demográficos
- Tipo de contacto
- Historial de campañas
- Indicadores macroeconómicos
- Resultado de campaña (y)

## 🔗 Links relevantes

- 📘 **Dataset original (UCI Machine Learning Repository):** https://archive.ics.uci.edu/ml/datasets/bank+marketing
- 📗 **Documentación Streamlit:** https://docs.streamlit.io
- 📘 **Pandas Documentation:** https://pandas.pydata.org/docs/
- 📘 **Seaborn Gallery:** https://seaborn.pydata.org/examples/index.html

## 👤 Autor

**Oscar Guillinta**  
Especialización en Analítica de Datos  
Año: 2026

## ✅ Observaciones finales

La aplicación cumple con todos los requisitos solicitados:

- ✅ Sidebar
- ✅ Tabs
- ✅ Columns
- ✅ Widgets interactivos
- ✅ Programación Orientada a Objetos
- ✅ Análisis Exploratorio completo

El código fue diseñado con enfoque educativo y claridad estructural.

---

⭐ **Fin del README**
