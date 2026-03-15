import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la interfaz
st.set_page_config(page_title="Water Quality Analytics", page_icon="💧", layout="wide")

# Estilos visuales
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # Cargamos el archivo con el nombre que indicaste
        df = pd.read_csv('Watera.csv')
        
        # Limpieza: Eliminamos valores nulos para evitar errores en cálculos estadísticos
        df = df.dropna()
        return df
    except FileNotFoundError:
        st.error("⚠️ El archivo 'Watera.csv' no se encuentra en el repositorio.")
        return None
@st.cache_data
def load_data():
    try:
        # Intentamos leer con coma, si falla probamos con punto y coma
        try:
            df = pd.read_csv('Watera.csv', sep=',')
            if len(df.columns) <= 1: # Si solo lee una columna, el separador está mal
                df = pd.read_csv('Watera.csv', sep=';')
        except:
            df = pd.read_csv('Watera.csv', sep=';')

        # LIMPIEZA DE NOMBRES: Eliminamos espacios en blanco alrededor de los nombres de columnas
        df.columns = df.columns.str.strip()
        
        # BUSCADOR INTELIGENTE DE COLUMNA:
        # Si no existe 'Potability', buscamos algo que se le parezca
        posibles_nombres = ['Potability', 'potability', 'Potabilidad', 'Target']
        for nombre in posibles_nombres:
            if nombre in df.columns:
                df = df.rename(columns={nombre: 'Potability'})
                break
        
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"Error al cargar el dataset: {e}")
        return None

df = load_data()

# Verificación de seguridad antes de calcular
if df is not None:
    if 'Potability' not in df.columns:
        st.error(f"❌ No encontré la columna de Potabilidad. Las columnas disponibles son: {list(df.columns)}")
        st.stop() # Detiene la app para que no salga el error rojo feo
df = load_data()

if df is not None:
    # Barra lateral de navegación
    st.sidebar.title("💧 Menú de Control")
    opcion = st.sidebar.selectbox("Seleccione una sección:", ["Landing Page", "Dashboard de Calidad"])

    if opcion == "Landing Page":
        st.title("Sistema de Análisis de Potabilidad")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("""
            ### Bienvenida
            Este dashboard profesional procesa datos fisicoquímicos para determinar la calidad del agua. 
            Utilizamos indicadores críticos como el pH, la dureza y la concentración de sólidos para evaluar la seguridad del consumo.
            
            **Estatus del Dataset:**
            - **Archivo:** Watera.csv
            - **Registros procesados:** {:,}
            """.format(len(df)))
            
            st.info("La potabilidad se define como: **1 (Apta)** y **0 (No Apta)**.")

        with col2:
            # Resumen rápido de métricas
            potabilidad_promedio = (df['Potability'].mean() * 100)
            st.metric("Índice de Potabilidad", f"{potabilidad_promedio:.1f}%")

    else:
        st.title("📊 Panel Analítico de Parámetros")
        
        # Filtros dinámicos en la barra lateral
        st.sidebar.subheader("Filtros de Datos")
        target = st.sidebar.radio("Ver muestras:", ["Todas", "Potables", "No Potables"])
        
        if target == "Potables":
            display_df = df[df['Potability'] == 1]
        elif target == "No Potables":
            display_df = df[df['Potability'] == 0]
        else:
            display_df = df

        # Fila 1: Indicadores clave
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("pH Promedio", round(display_df['ph'].mean(), 2))
        m2.metric("Sólidos (TDS)", round(display_df['Solids'].mean(), 1))
        m3.metric("Sulfatos", round(display_df['Sulfate'].mean(), 2))
        m4.metric("Cloraminas", round(display_df['Chloramines'].mean(), 2))

        # Fila 2: Gráficos principales
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### Distribución de pH por Potabilidad")
            fig1 = px.histogram(display_df, x="ph", color="Potability", 
                               marginal="violin", nbins=50,
                               color_discrete_map={0: "#EF553B", 1: "#636EFA"})
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            st.markdown("#### Correlación: Sulfatos vs Cloraminas")
            fig2 = px.scatter(display_df, x="Sulfate", y="Chloramines", 
                             color="Potability", size="ph", hover_data=['Hardness'],
                             color_continuous_scale="RdBu")
            st.plotly_chart(fig2, use_container_width=True)

        # Fila 3: Matriz de Correlación
        st.divider()
        st.subheader("🔍 Matriz de Correlación")
        corr = display_df.corr()
        fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='Blues')
        st.plotly_chart(fig_corr, use_container_width=True)
