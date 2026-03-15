import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Water Quality Analytics",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Simulación de carga de datos (Dataset: Water Potability)
@st.cache_data
def load_data():
    # En producción, asegúrate de que el CSV esté en la raíz o usa la API de Kaggle
    # URL de ejemplo si el archivo se llama water_potability.csv
    try:
        df = pd.read_csv('water_potability.csv')
        return df
    except:
        # Generación de datos sintéticos en caso de que no encuentre el archivo localmente para la demo
        import numpy as np
        data = pd.DataFrame(
            np.random.randn(100, 4),
            columns=['ph', 'Sulfate', 'Chloramines', 'Potability']
        )
        data['Potability'] = np.random.choice([0, 1], size=100)
        return data

df = load_data()

# Navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Inicio / Landing Page", "Dashboard Analítico"])

if page == "Inicio / Landing Page":
    st.title("💧 Análisis de Calidad y Potabilidad del Agua")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Sobre el Proyecto
        Este sistema permite monitorear y analizar los parámetros críticos que definen si el agua es apta para el consumo humano. 
        Utilizando técnicas de **Análisis Exploratorio de Datos (EDA)**, transformamos datos crudos en decisiones informadas.

        **Objetivos del Panel:**
        * Visualizar la distribución de métricas químicas (pH, Sulfatos, Cloro).
        * Identificar correlaciones entre variables.
        * Evaluar el porcentaje de potabilidad en las muestras recolectadas.
        """)
        
    with col2:
        st.image("https://images.unsplash.com/photo-1548932813-71000a65fb25?auto=format&fit=crop&w=400", caption="Recursos Hídricos")

    st.divider()
    st.subheader("Parámetros Analizados")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Muestras Totales", len(df))
    m2.metric("Promedio pH", round(df['ph'].mean(), 2))
    m3.metric("Potabilidad (%)", f"{round(df['Potability'].mean()*100, 2)}%")

elif page == "Dashboard Analítico":
    st.title("📊 Panel de Control de Datos")
    
    # Filtros rápidos
    st.sidebar.subheader("Filtros")
    potabilidad_filter = st.sidebar.multiselect("Estado de Potabilidad", 
                                              options=df['Potability'].unique(), 
                                              default=df['Potability'].unique())
    
    filtered_df = df[df['Potability'].isin(potabilidad_filter)]

    # Layout de Gráficos
    row1_1, row1_2 = st.columns(2)
    
    with row1_1:
        st.write("#### Distribución del pH")
        fig_hist = px.histogram(filtered_df, x="ph", color="Potability", 
                               marginal="box", nbins=30, color_discrete_sequence=['#ef553b', '#636efa'])
        st.plotly_chart(fig_hist, use_container_width=True)

    with row1_2:
        st.write("#### Relación Sulfatos vs Cloraminas")
        fig_scatter = px.scatter(filtered_df, x="Sulfate", y="Chloramines", 
                                color="Potability", opacity=0.6)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.write("#### Vista Previa del Dataset")
    st.dataframe(filtered_df.head(10), use_container_width=True)

# Nueva Sección: Matriz de Correlación
    st.divider()
    st.subheader("🔍 Análisis de Correlación de Variables")
    
    col_corr, col_text = st.columns([2, 1])
    
    with col_corr:
        # Calculamos la correlación solo de las columnas numéricas principales
        corr = filtered_df[['ph', 'Sulfate', 'Chloramines', 'Potability']].corr()
        
        # Creamos el Heatmap con Plotly
        fig_corr = px.imshow(corr, 
                             text_auto=True, 
                             aspect="auto", 
                             color_continuous_scale='RdBu_r',
                             labels=dict(color="Correlación"))
        st.plotly_chart(fig_corr, use_container_width=True)
        
    with col_text:
        st.markdown("""
        **¿Cómo leer este gráfico?**
        * **1.0**: Correlación perfecta (una variable sube igual que la otra).
        * **0.0**: No hay relación alguna entre las variables.
        * **Valores Negativos**: Cuando una variable sube, la otra tiende a bajar.
        
        *Nota: En la calidad del agua, las correlaciones suelen ser bajas, lo que indica que la potabilidad depende de un equilibrio complejo de todos los factores, no de uno solo.*
        """)
