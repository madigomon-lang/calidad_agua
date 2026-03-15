import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico de Datos", page_icon="🔍")

st.title("🔍 Diagnóstico de Estructura de Datos")

try:
    # Leemos el archivo detectando automáticamente el separador (coma, punto y coma, etc.)
    df = pd.read_csv('Watera.csv', sep=None, engine='python')
    
    st.success("✅ ¡Archivo 'Watera.csv' detectado y leído!")
    
    st.subheader("1. Nombres exactos de tus columnas")
    st.write("Copia y pégame esta lista:")
    st.code(list(df.columns))
    
    st.subheader("2. Vista previa de los datos")
    st.dataframe(df.head())

    st.subheader("3. Tipos de datos detectados")
    st.write(df.dtypes)

except Exception as e:
    st.error(f"❌ Error al leer el archivo: {e}")
    st.info("Asegúrate de que el archivo se llame exactamente 'Watera.csv' y esté en la raíz de tu GitHub.")
