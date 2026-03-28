import streamlit as st
import gspread
import pandas as pd
import os

# ==========================================
# 🎨 1. Configuración Visual de la Página
# ==========================================
st.set_page_config(
    page_title="Monitor Dólar Banxico", 
    page_icon="📈", 
    layout="wide"
)

st.title("📊 Monitor del Dólar Oficial (FIX)")
st.write("Esta aplicación web lee los datos históricos guardados en Google Sheets por nuestro robot diario.")

# ⚠️ REEMPLAZA ESTO CON EL ID REAL DE TU GOOGLE SHEET ⚠️
ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

# ==========================================
# 🔐 2. Conexión Inteligente (Nube vs PC Local)
# ==========================================
try:
    # ☁️ Camino A: Si estamos en la nube de Streamlit Cloud (leyendo los secretos que guardamos)
    if "gcp_service_account" in st.secrets:
        cliente = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    
    # 💻 Camino B: Si estás corriendo el archivo en Visual Studio Code local
    else:
        cliente = gspread.service_account(filename="credenciales.json")

    # Abrir la hoja por ID
    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    
    # ==========================================
    # 📈 3. Lectura de Datos Históricos
    # ==========================================
    datos = hoja.get_all_records() # Jala todas las filas pasadas de la tabla

    if datos:
        df = pd.DataFrame(datos)
        
        # Limpieza estándar de datos para la gráfica
        df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)
        df['Precio'] = pd.to_numeric(df['Precio'])

        # --- SECCIÓN DE MÉTRICAS RÁPIDAS ---
        ultimo_precio = df['Precio'].iloc[-1]
        precio_anterior = df['Precio'].iloc[-2] if len(df) > 1 else ultimo_precio
        variacion = ultimo_precio - precio_anterior

        col1, col2, col3 = st.columns(3)
        
        col1.metric(
            label="💵 Precio Más Reciente", 
            value=f"${ultimo_precio:.4f} MXN", 
            delta=f"{variacion:.4f} MXN"
        )
        
        col2.metric(
            label="📈 Máximo del Mes", 
            value=f"${df['Precio'].max():.4f} MXN"
        )
        
        col3.metric(
            label="📉 Mínimo del Mes", 
            value=f"${df['Precio'].min():.4f} MXN"
        )

        st.divider()

        # --- SECCIÓN DE GRÁFICA ---
        st.subheader("📉 Tendencia Visual de los Valores Pasados")
        # Grafica la línea temporal
        st.line_chart(df.set_index('Fecha')['Precio'])

        st.divider()

        # --- SECCIÓN DE TABLA DESPLEGABLE ---
        with st.expander("📂 Ver base de datos completa"):
            df_ordenado = df.sort_values(by='Fecha', ascending=False)
            st.dataframe(df_ordenado, use_container_width=True)

    else:
        st.warning("⚠️ La conexión fue exitosa, pero parece que la hoja de cálculo está vacía.")

except Exception as e:
    st.error(f"❌ Error de Conexión: {e}")
    st.info("💡 Tip: Verifica que pusiste el ID correcto de tu Google Sheet en el código y que guardaste correctamente el secreto en Streamlit Cloud.")