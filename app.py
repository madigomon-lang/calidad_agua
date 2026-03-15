import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Water Analytics Pro",
    page_icon="💧",
    layout="wide"
)

# --- CARGA DE DATOS INTELIGENTE ---
@st.cache_data
def load_data():
    try:
        # Intentar leer con coma o punto y coma (común en Excel)
        try:
            df = pd.read_csv('Watera.csv', sep=',')
            if len(df.columns) <= 1: df = pd.read_csv('Watera.csv', sep=';')
        except:
            df = pd.read_csv('Watera.csv', sep=';')

        # Limpiar espacios en los nombres de columnas
        df.columns = df.columns.str.strip()

        # Diccionario de Mapeo: Traduce nombres de columnas automáticamente
        mapeo = {
            'ph': ['ph', 'PH', 'pH', 'Ph', 'Valor_ph'],
            'Solids': ['Solids', 'Sólidos', 'Solidos', 'TDS', 'Total_Solids'],
            'Sulfate': ['Sulfate', 'Sulfatos', 'Sulfato'],
            'Chloramines': ['Chloramines', 'Cloraminas', 'Cloramina'],
            'Potability': ['Potability', 'Potabilidad', 'Target', 'Apta', 'Potable']
        }

        for estandar, variantes in mapeo.items():
            for v in variantes:
                if v in df.columns:
                    df = df.rename(columns={v: estandar})
                    break
        
        # Eliminar filas vacías para evitar errores en gráficos
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"Error crítico al leer 'Watera.csv': {e}")
        return None

# --- EJECUCIÓN ---
df = load_data()

if df is not None:
    # Verificación de columnas mínimas
    columnas_necesarias = ['ph', 'Solids', 'Sulfate', 'Chloramines', 'Potability']
    faltantes = [c for c in columnas_necesarias if c not in df.columns]
    
    if faltantes:
        st.error(f"⚠️ Faltan columnas: {faltantes}")
        st.info(f"Columnas en tu archivo: {list(df.columns)}")
        st.stop()

    # --- NAVEGACIÓN ---
    st.sidebar.title("💧 Control de Panel")
    menu = st.sidebar.radio("Ir a:", ["Inicio", "Análisis Exploratorio"])

    if menu == "Inicio":
        st.title("💧 Calidad del Agua: Análisis Profesional")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Objetivo del Proyecto
            Este tablero permite evaluar la potabilidad del agua mediante el análisis de parámetros químicos.
            - **Potabilidad 1**: El agua cumple con los estándares.
            - **Potabilidad 0**: El agua no es segura para consumo.
            
            **Métricas del Archivo:**
            - Total de registros analizados: `{}`
            """.format(len(df)))
            
        with col2:
            st.metric("Tasa de Potabilidad", f"{round(df['Potability'].mean()*100, 2)}%")

    else:
        st.title("📊 Panel Analítico")
        
        # Filtros
        st.sidebar.subheader("Filtros de Datos")
        filtro_pot = st.sidebar.multiselect("Filtrar por Potabilidad:", 
                                           options=df['Potability'].unique(), 
                                           default=df['Potability'].unique())
        
        df_filtrado = df[df['Potability'].isin(filtro_pot)]

        # Métricas principales
        m1, m2, m3 = st.columns(3)
        m1.metric("pH Promedio", round(df_filtrado['ph'].mean(), 2))
        m2.metric("Sólidos (TDS)", f"{round(df_filtrado['Solids'].mean(), 0)}")
        m3.metric("Cloraminas", round(df_filtrado['Chloramines'].mean(), 2))

        # Visualizaciones
        row1_1, row1_2 = st.columns(2)
        
        with row1_1:
            st.write("#### Distribución de Sulfatos")
            fig1 = px.histogram(df_filtrado, x="Sulfate", color="Potability", 
                               marginal="box", color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig1, use_container_width=True)

        with row1_2:
            st.write("#### Relación pH vs Sólidos")
            fig2 = px.scatter(df_filtrado, x="ph", y="Solids", color="Potability", 
                              opacity=0.5, template="plotly_white")
            st.plotly_chart(fig2, use_container_width=True)

        # Matriz de Correlación
        st.divider()
        st.subheader("🔍 Matriz de Correlación")
        corr = df_filtrado[['ph', 'Solids', 'Sulfate', 'Chloramines', 'Potability']].corr()
        fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_corr, use_container_width=True)
