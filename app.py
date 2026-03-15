import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Water Quality Analytics", page_icon="💧", layout="wide")

# --- CARGA DE DATOS AJUSTADA A WATERA.CSV ---
@st.cache_data
def load_data():
    try:
        # Según tu diagnóstico, el separador es la coma y los nombres están en minúsculas
        df = pd.read_csv('Watera.csv')
        
        # Mapeo exacto basado en tu imagen de diagnóstico
        # Cambiamos los nombres para que el código sea fácil de leer
        mapeo = {
            'ph': 'pH',
            'hardness': 'Dureza',
            'tds': 'Sólidos',
            'chlorine': 'Cloro',
            'sulfate': 'Sulfatos',
            'conductivity': 'Conductividad',
            'organic_carbon': 'Carbono_Orgánico',
            'trihalomethanes': 'Trihalometanos',
            'turbidity': 'Turbidez',
            'potability': 'Potabilidad'
        }
        df = df.rename(columns=mapeo)
        
        # Limpieza de nulos para gráficos limpios
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

df = load_data()

if df is not None:
    # --- NAVEGACIÓN LATERAL ---
    st.sidebar.title("💧 Panel de Control")
    seccion = st.sidebar.radio("Ir a:", ["Landing Page", "Dashboard Analítico"])

    if seccion == "Landing Page":
        st.title("💧 Análisis Exploratorio: Calidad del Agua")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            ### Bienvenida
            Este sistema analiza la potabilidad del agua basándose en parámetros físico-químicos reales. 
            
            **Resumen del Dataset:**
            - **Muestras totales:** {len(df)}
            - **Columnas procesadas:** {len(df.columns)}
            - **Estado:** ✅ Datos limpios y listos.
            """)
            st.info("La **Potabilidad 1** indica agua apta para consumo, mientras que **0** indica no apta.")
        
        with col2:
            st.metric("Índice de Potabilidad", f"{round(df['Potabilidad'].mean()*100, 1)}%")

    else:
        st.title("📊 Dashboard de Control de Calidad")
        
        # Filtros rápidos
        filtro = st.sidebar.multiselect("Filtrar por Potabilidad", 
                                       options=df['Potabilidad'].unique(), 
                                       default=df['Potabilidad'].unique())
        
        df_filtrado = df[df['Potabilidad'].isin(filtro)]

        # --- FILA 1: MÉTRICAS ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Promedio pH", round(df_filtrado['pH'].mean(), 2))
        m2.metric("Sulfatos (prom)", round(df_filtrado['Sulfatos'].mean(), 1))
        m3.metric("Cloro (prom)", round(df_filtrado['Cloro'].mean(), 2))
        m4.metric("Sólidos (TDS)", round(df_filtrado['Sólidos'].mean(), 0))

        # --- FILA 2: GRÁFICOS ---
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Distribución de Sulfatos")
            fig_hist = px.histogram(df_filtrado, x="Sulfatos", color="Potabilidad", 
                                   marginal="box", color_discrete_map={0:'#EF553B', 1:'#636EFA'})
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with c2:
            st.subheader("Relación pH vs Sólidos")
            fig_scatter = px.scatter(df_filtrado, x="pH", y="Sólidos", color="Potabilidad",
                                    opacity=0.6, template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)

        # --- FILA 3: CORRELACIÓN ---
        st.divider()
        st.subheader("🔍 Matriz de Correlación")
        corr = df_filtrado.corr()
        fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_corr, use_container_width=True)

        st.write("#### Vista previa de datos filtrados")
        st.dataframe(df_filtrado.head(10), use_container_width=True)

 
