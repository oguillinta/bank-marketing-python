import io
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Config general
# ---------------------------
st.set_page_config(
    page_title="EDA - Bank Marketing (Streamlit)",
    page_icon="📊",
    layout="wide"
)

sns.set()  # estilo base (simple)
TARGET_DEFAULT = "y"


# ---------------------------
# POO: Clase obligatoria
# ---------------------------
class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def basic_info(self) -> dict:
        """Retorna info general: shape, dtypes, nulos, memoria aproximada."""
        info_buffer = io.StringIO()
        self.df.info(buf=info_buffer)
        info_text = info_buffer.getvalue()

        return {
            "shape": self.df.shape,
            "dtypes": self.df.dtypes,
            "nulls": self.df.isna().sum().sort_values(ascending=False),
            "info_text": info_text
        }

    def classify_variables(self) -> dict:
        """Clasifica variables numéricas y categóricas (función personalizada)."""
        numeric_cols = self.df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = [c for c in self.df.columns if c not in numeric_cols]
        return {
            "numeric": numeric_cols,
            "categorical": categorical_cols
        }

    def descriptive_stats(self) -> pd.DataFrame:
        numeric_df = self.df.select_dtypes(include=["number"])
        if numeric_df.shape[1] == 0:
            return pd.DataFrame()  # empty => UI will show warning
        return numeric_df.describe().T

    def categorical_summary(self, col: str) -> pd.DataFrame:
        """Conteo y proporción de una categórica."""
        counts = self.df[col].astype("object").fillna("NA").value_counts(dropna=False)
        props = (counts / len(self.df)).round(4)
        out = pd.DataFrame({"count": counts, "proportion": props})
        return out

    def plot_hist(self, col: str, bins: int = 30, kde: bool = True):
        fig, ax = plt.subplots()
        sns.histplot(self.df[col], bins=bins, kde=kde, ax=ax)
        ax.set_title(f"Histograma: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frecuencia")
        return fig

    def plot_bar(self, col: str, top_n: int = 15):
        data = self.df[col].astype("object").fillna("NA").value_counts().head(top_n)
        fig, ax = plt.subplots()
        sns.barplot(x=data.values, y=data.index, ax=ax)
        ax.set_title(f"Top {top_n} categorías: {col}")
        ax.set_xlabel("Conteo")
        ax.set_ylabel(col)
        return fig

    def plot_box_by_category(self, num_col: str, cat_col: str):
        fig, ax = plt.subplots()
        tmp = self.df[[num_col, cat_col]].dropna()
        tmp[cat_col] = tmp[cat_col].astype("object")
        sns.boxplot(data=tmp, x=cat_col, y=num_col, ax=ax)
        ax.set_title(f"{num_col} vs {cat_col} (Boxplot)")
        ax.tick_params(axis='x', rotation=30)
        return fig

    def crosstab(self, col_a: str, col_b: str, normalize: bool = True) -> pd.DataFrame:
        ct = pd.crosstab(self.df[col_a], self.df[col_b], dropna=False)
        if normalize:
            ct = (ct.div(ct.sum(axis=1), axis=0)).round(4)
        return ct

    def acceptance_rate_by_group(self, group_col: str, target_col: str = TARGET_DEFAULT) -> pd.DataFrame:
        """Tasa de aceptación (y==yes) por grupo."""
        tmp = self.df[[group_col, target_col]].dropna()
        tmp[group_col] = tmp[group_col].astype("object").fillna("NA")
        rate = tmp.groupby(group_col)[target_col].apply(lambda s: (s.astype(str).str.lower() == "yes").mean())
        out = rate.sort_values(ascending=False).to_frame("acceptance_rate").round(4)
        out["count"] = tmp[group_col].value_counts()
        return out.sort_values("acceptance_rate", ascending=False)


# ---------------------------
# Helpers
# ---------------------------
def require_df():
    if "df" not in st.session_state or st.session_state["df"] is None:
        st.warning("Primero carga un archivo .csv en el módulo **Carga del dataset**.")
        st.stop()


def load_csv(uploaded_file) -> pd.DataFrame:
    uploaded_file.seek(0)

    df = pd.read_csv(uploaded_file)

    if df.shape[1] == 1 and ";" in df.columns[0]:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, sep=";")

    return df


# ---------------------------
# Sidebar: navegación
# ---------------------------
st.sidebar.title("📌 Menú")
page = st.sidebar.radio(
    "Ir a:",
    ["Home", "Carga del dataset", "EDA (Análisis Exploratorio)"],
    index=0
)

st.sidebar.divider()
st.sidebar.caption("Requisito: usar sidebar, tabs, columns, widgets (selectbox, multiselect, slider, checkbox).")


# ---------------------------
# MÓDULO 1: HOME
# ---------------------------
if page == "Home":
    st.title("📊 EDA Interactivo - Bank Marketing")
    st.write(
        "Aplicación en **Streamlit** orientada al **Análisis Exploratorio de Datos (EDA)** del dataset "
        "**BankMarketing.csv**. El objetivo es entender patrones y relaciones que influyen en la aceptación "
        "de campañas de marketing (**y = yes/no**)."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👤 Autor")
        st.markdown(
            "- **Nombre:** Oscar Guillinta  \n"
            "- **Curso:** Especialización Python for Analytics  \n"
            "- **Año:** 2026"
        )

    with col2:
        st.subheader("📁 Sobre el dataset")
        st.write(
            "Dataset de una institución financiera para analizar factores que influyen en la aceptación "
            "de campañas (variable objetivo: **y**). Incluye variables demográficas, de contacto, "
            "historial de campañas y variables macroeconómicas."
        )

    st.subheader("🧰 Tecnologías usadas")
    st.markdown(
        "- Python\n"
        "- Pandas / NumPy\n"
        "- Streamlit\n"
        "- Matplotlib / Seaborn\n"
        "- Estadística descriptiva"
    )

    st.info(
        "Nota: este proyecto NO construye modelos predictivos. Se enfoca en EDA e insights.",
        icon="ℹ️"
    )


# ---------------------------
# MÓDULO 2: CARGA DEL DATASET
# ---------------------------
elif page == "Carga del dataset":
    st.title("📥 Carga del dataset (obligatorio)")

    uploaded = st.file_uploader("Sube tu archivo BankMarketing.csv", type=["csv"])

    if uploaded is None:
        st.warning("Sube un archivo para continuar. Sin dataset cargado, no se ejecuta ningún análisis.")
        st.caption("Tip: si estás en local, puedes seleccionar el CSV desde tu computadora.")
    else:
        try:
            df = load_csv(uploaded)
            st.session_state["df"] = df
            st.success("✅ Archivo cargado correctamente.")

            st.subheader("Vista previa")
            st.dataframe(df.head(10), use_container_width=True)

            st.subheader("Dimensiones")
            st.write(f"**Filas:** {df.shape[0]} | **Columnas:** {df.shape[1]}")

            st.subheader("Columnas")
            st.write(list(df.columns))

        except Exception as e:
            st.session_state["df"] = None
            st.error(f"❌ Error leyendo el archivo: {e}")


# ---------------------------
# MÓDULO 3: EDA (10 ítems mínimo)
# ---------------------------
else:
    st.title("🔎 EDA (Análisis Exploratorio de Datos)")
    require_df()

    df = st.session_state["df"]
    analyzer = DataAnalyzer(df)

    # Widgets globales
    st.sidebar.subheader("⚙️ Controles globales")
    show_raw = st.sidebar.checkbox("Mostrar dataset completo (puede ser pesado)", value=False)
    sample_n = st.sidebar.slider("Filas para mostrar (muestra)", min_value=5, max_value=200, value=20, step=5)

    if show_raw:
        st.subheader("Dataset (vista completa)")
        st.dataframe(df, use_container_width=True)
    else:
        st.subheader(f"Muestra del dataset (n={sample_n})")
        st.dataframe(df.sample(min(sample_n, len(df)), random_state=42), use_container_width=True)

    st.divider()

    # Tabs para organizar el EDA
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Ítems 1-2",
        "Ítems 3-4",
        "Ítems 5-6",
        "Ítems 7-8",
        "Ítems 9-10"
    ])

    # ---------------------------
    # Ítem 1 y 2
    # ---------------------------
    with tab1:
        st.header("Ítem 1: Información general del dataset")
        info = analyzer.basic_info()

        c1, c2 = st.columns(2)
        with c1:
            st.write("**.info() (resumen textual):**")
            st.code(info["info_text"])
        with c2:
            st.write("**Tipos de datos:**")
            st.dataframe(info["dtypes"].astype(str), use_container_width=True)

        st.write("**Conteo de valores nulos (top):**")
        st.dataframe(info["nulls"].head(20), use_container_width=True)

        st.caption("Interpretación: revisa tipos de datos y columnas con nulos para decidir limpieza/transformaciones.")

        st.divider()

        st.header("Ítem 2: Clasificación de variables (numéricas vs categóricas)")
        var_types = analyzer.classify_variables()

        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Numéricas")
            st.write(f"Total: **{len(var_types['numeric'])}**")
            st.write(var_types["numeric"])
        with c4:
            st.subheader("Categóricas")
            st.write(f"Total: **{len(var_types['categorical'])}**")
            st.write(var_types["categorical"])

        st.caption("Interpretación: esta separación ayuda a elegir el tipo de análisis y visualización.")

    # ---------------------------
    # Ítem 3 y 4
    # ---------------------------
    with tab2:
        st.header("Ítem 3: Estadísticas descriptivas (numéricas)")
        desc = analyzer.descriptive_stats()
        if desc.empty:
            st.warning("No se detectaron columnas numéricas. Revisa el separador del CSV (probablemente es ';').")
        else:
            st.dataframe(desc, use_container_width=True)

        st.caption("Interpretación rápida: media/mediana indican tendencia central; std y rangos muestran dispersión.")

        st.divider()

        st.header("Ítem 4: Análisis de valores faltantes")
        nulls = df.isna().sum()
        nulls = nulls[nulls > 0].sort_values(ascending=False)

        if nulls.empty:
            st.success("✅ No se detectaron valores faltantes (NaN) en el dataset.")
        else:
            st.write("**Columnas con nulos (conteo):**")
            st.dataframe(nulls, use_container_width=True)

            st.write("**Visualización simple:**")
            fig, ax = plt.subplots()
            sns.barplot(x=nulls.values, y=nulls.index, ax=ax)
            ax.set_title("Conteo de valores faltantes por columna")
            ax.set_xlabel("Nulos")
            ax.set_ylabel("Columna")
            st.pyplot(fig)

        st.caption("Discusión: si hay nulos, evalúa imputación, eliminar filas/columnas o tratamiento según negocio.")

    # ---------------------------
    # Ítem 5 y 6
    # ---------------------------
    with tab3:
        st.header("Ítem 5: Distribución de variables numéricas (histogramas)")
        var_types = analyzer.classify_variables()
        numeric_cols = var_types["numeric"]

        if not numeric_cols:
            st.warning("No hay columnas numéricas detectadas.")
        else:
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                num_col = st.selectbox("Selecciona variable numérica", numeric_cols)
            with c2:
                bins = st.slider("Bins", min_value=5, max_value=100, value=30, step=5)
            with c3:
                kde = st.checkbox("Mostrar KDE", value=True)

            fig = analyzer.plot_hist(num_col, bins=bins, kde=kde)
            st.pyplot(fig)

            st.caption("Interpretación: observa sesgos, colas largas y valores extremos (posibles outliers).")

        st.divider()

        st.header("Ítem 6: Análisis de variables categóricas (conteos y proporciones)")
        cat_cols = analyzer.classify_variables()["categorical"]
        if not cat_cols:
            st.warning("No hay columnas categóricas detectadas.")
        else:
            c4, c5 = st.columns([2, 1])
            with c4:
                cat_col = st.selectbox("Selecciona variable categórica", cat_cols)
            with c5:
                top_n = st.slider("Top N categorías", min_value=5, max_value=30, value=15, step=1)

            summary = analyzer.categorical_summary(cat_col)
            st.dataframe(summary.head(top_n), use_container_width=True)

            fig = analyzer.plot_bar(cat_col, top_n=top_n)
            st.pyplot(fig)

            st.caption("Interpretación: categorías dominantes pueden influir en la segmentación y estrategia de contacto.")

    # ---------------------------
    # Ítem 7 y 8
    # ---------------------------
    with tab4:
        st.header("Ítem 7: Análisis bivariado (numérico vs categórico)")

        var_types = analyzer.classify_variables()
        numeric_cols = var_types["numeric"]
        cat_cols = var_types["categorical"]

        if not numeric_cols or not cat_cols:
            st.warning("Se requiere al menos 1 variable numérica y 1 variable categórica para este análisis.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                num_col = st.selectbox("Variable numérica", numeric_cols, key="item7_num")
            with c2:
                cat_col = st.selectbox("Variable categórica", cat_cols, key="item7_cat")

            fig = analyzer.plot_box_by_category(num_col=num_col, cat_col=cat_col)
            st.pyplot(fig)

            st.caption(
                "Interpretación: compara la distribución de la variable numérica por cada categoría "
                "(mediana, dispersión y posibles outliers)."
            )

        st.divider()

        st.header("Ítem 8: Tablas cruzadas (categórica vs categórica)")

        if len(cat_cols) < 2:
            st.warning("Se requieren al menos 2 variables categóricas.")
        else:
            c3, c4, c5 = st.columns([2, 2, 1])
            with c3:
                col_a = st.selectbox("Categórica A", cat_cols, key="item8_a")
            with c4:
                col_b = st.selectbox("Categórica B", [c for c in cat_cols if c != col_a], key="item8_b")
            with c5:
                normalize = st.checkbox("Normalizar por filas", value=True)

            ct = analyzer.crosstab(col_a, col_b, normalize=normalize)
            st.dataframe(ct, use_container_width=True)

            st.caption(
                "Interpretación: una tabla cruzada ayuda a ver patrones de combinación entre categorías. "
                "Normalizado por filas muestra proporciones dentro de cada categoría A."
            )

    # ---------------------------
    # Ítem 9 y 10
    # ---------------------------
    with tab5:
        st.header("Ítem 9: Correlación entre variables numéricas")

        numeric_cols = analyzer.classify_variables()["numeric"]
        if len(numeric_cols) < 2:
            st.warning("Se requieren al menos 2 variables numéricas para calcular correlaciones.")
        else:
            corr_method = st.selectbox("Método de correlación", ["pearson", "spearman", "kendall"])
            corr = df[numeric_cols].corr(method=corr_method)

            st.dataframe(corr, use_container_width=True)

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=False, ax=ax)
            ax.set_title(f"Matriz de correlación ({corr_method})")
            st.pyplot(fig)

            st.caption(
                "Interpretación: correlaciones altas (positivas o negativas) pueden sugerir relación lineal/monótona "
                "entre variables. No implica causalidad."
            )

        st.divider()

        st.header("Ítem 10: Tasa de aceptación (y=yes) por segmento (categórico)")

        target_col = st.selectbox(
            "Selecciona la variable objetivo (target)",
            options=df.columns.tolist(),
            index=df.columns.tolist().index(TARGET_DEFAULT) if TARGET_DEFAULT in df.columns else 0
        )

        cat_cols = analyzer.classify_variables()["categorical"]
        if not cat_cols:
            st.warning("No se detectaron variables categóricas para segmentar.")
        else:
            group_col = st.selectbox("Segmentar por (categórica)", cat_cols, key="item10_group")
            top_n = st.slider("Mostrar top N segmentos", min_value=5, max_value=30, value=15, step=1, key="item10_topn")

            # Calcula tasa de aceptación
            rates = analyzer.acceptance_rate_by_group(group_col=group_col, target_col=target_col)
            st.dataframe(rates.head(top_n), use_container_width=True)

            fig, ax = plt.subplots()
            plot_df = rates.head(top_n).iloc[::-1]  # para que el mayor quede arriba visualmente
            sns.barplot(x=plot_df["acceptance_rate"], y=plot_df.index, ax=ax)
            ax.set_title(f"Tasa de aceptación (target={target_col}) por {group_col} (Top {top_n})")
            ax.set_xlabel("Acceptance rate")
            ax.set_ylabel(group_col)
            st.pyplot(fig)

            st.caption(
                "Interpretación: ayuda a identificar segmentos donde la campaña tiene mayor probabilidad de éxito, "
                "útil para priorización de contactos."
            )
