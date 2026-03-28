import streamlit as st
import gspread
import pandas as pd
import os
import json

# Configuración de la página
st.set_page_config(page_title="Monitor Dólar Banxico", page_icon="📈")

st.title("📊 Historial del Dólar (FIX)")
st.write("Datos obtenidos automáticamente desde Banxico y almacenados en Google Sheets.")

# --- CONEXIÓN A GOOGLE SHEETS ---
try:
    if "GOOGLE_CREDENTIALS" in os.environ:
        info_credenciales = json.loads(os.environ["GOOGLE_CREDENTIALS"])
        cliente = gspread.service_account_from_dict(info_credenciales)
    else:
        cliente = gspread.service_account(filename="credenciales.json")

    # Reemplaza con tu ID de hoja real
    ID_HOJA_CALCULO = "TU_ID_DE_HOJA_AQUÍ" 
    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    
    # 1. Traer todos los valores de la hoja
    datos = hoja.get_all_records() # Esto lee todas las filas y columnas pasadas
    
    if datos:
        # 2. Convertir a un DataFrame de Pandas para manejar los valores pasados
        df = pd.DataFrame(datos)
        
        # Asegurarnos de que las columnas tengan el formato correcto
        df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)
        df['Precio'] = pd.to_numeric(df['Precio'])

        # --- MOSTRAR MÉTRICA DEL DÍA ---
        ultimo_precio = df['Precio'].iloc[-1]
        precio_anterior = df['Precio'].iloc[-2] if len(df) > 1 else ultimo_precio
        variacion = ultimo_precio - precio_anterior

        col1, col2 = st.columns(2)
        col1.metric("Precio Actual", f"${ultimo_precio:.4f}", f"{variacion:.4f}")
        col2.write("Última actualización: " + str(df['Fecha'].iloc[-1].date()))

        # --- GRÁFICA DE HISTORIAL ---
        st.subheader("📈 Tendencia de los valores pasados")
        st.line_chart(df.set_index('Fecha')['Precio'])

        # --- TABLA DE DATOS ---
        with st.expander("Ver tabla completa de registros"):
            st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True)
    else:
        st.warning("La hoja de cálculo está vacía por ahora.")

except Exception as e:
    st.error(f"Error al conectar con los datos: {e}")