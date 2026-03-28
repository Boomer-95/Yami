import streamlit as st
import pandas as pd
from datetime import timedelta

# Configuración de la página (Título en la pestaña del navegador)
st.set_page_config(page_title="Conversor DOF Oficial", page_icon="💰")

st.title("📊 Calculadora de Tipo de Cambio Oficial")
st.subheader("Consulta el valor publicado por el DOF del día anterior")
st.markdown("---")

# 🔗 1. CONEXIÓN DIRECTA A GOOGLE SHEETS USANDO PANDAS
sheet_id = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"
# Convertimos el enlace normal del Sheet a un enlace de descarga de datos CSV
url_csv = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Pandas descarga y lee la tabla directamente de la nube
    df = pd.read_csv(url_csv)
except Exception as e:
    st.error(f"Error al conectar con Google Sheets: {e}")
    st.stop()


# 🎨 2. DISEÑO DE LA INTERFAZ (Dos columnas)
col1, col2 = st.columns(2)

with col1:
    monto_pesos = st.number_input("Cantidad en Pesos ($ MXN):", min_value=0.0, step=50.0)

with col2:
    fecha_usuario = st.date_input("Selecciona la fecha de hoy:")


# 🧮 3. LÓGICA DEL CÁLCULO
if st.button("🧮 Calcular Conversión"):
    if monto_pesos <= 0:
        st.warning("Por favor, escribe una cantidad de pesos válida.")
    else:
        # Restamos un día (el DOF publica el dólar que se usa hoy, ayer)
        fecha_anterior = fecha_usuario - timedelta(days=1)
        fecha_busqueda = fecha_anterior.strftime('%d/%m/%Y') # Da formato DD/MM/AAAA
        
        st.info(f"📅 Buscando el dólar publicado el: **{fecha_busqueda}**")
        
        # 🔍 Buscamos la fecha en la columna 'Fecha' de nuestro Excel
        registro = df[df['Fecha'].astype(str) == fecha_busqueda]
        
        if not registro.empty:
            # Si lo encuentra, extrae el número y hace la división
            tipo_cambio = float(registro['Valor_Dolar'].values[0])
            total_dolares = monto_pesos / tipo_cambio
            
            # Mostramos el resultado en tarjetas bonitas
            metrica1, metrica2 = st.columns(2)
            metrica1.metric(label="Tipo de Cambio Oficial", value=f"${tipo_cambio:.4f} MXN")
            metrica2.metric(label="Total en Dólares", value=f"${total_dolares:.2f} USD")
        else:
            st.error(f"No hay registro oficial para la fecha {fecha_busqueda} en la nube.")