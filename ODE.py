import streamlit as st
import gspread
import pandas as pd
import json

# ==========================================
# 🎨 1. Configuración de la Página Web
# ==========================================
st.set_page_config(
    page_title="Monitor Dólar Banxico", 
    page_icon="📈", 
    layout="wide"
)

st.title("📊 Monitor del Dólar Oficial (FIX)")
st.write("Esta página web lee automáticamente los datos históricos guardados en Google Sheets por nuestro robot diario.")

# Reemplaza esto con el ID real de tu Google Sheet (está en la URL de tu navegador)
ID_HOJA_CALCULO = "TU_ID_DE_HOJA_AQUÍ"

# ==========================================
# 🔐 2. Conexión Inteligente (Nube o Local)
# ==========================================
try:
    # ☁️ Camino 1: Si estamos en la nube de Streamlit Cloud usando Secrets
    if "gcp_service_account" in st.secrets:
        cliente = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    
    # 💻 Camino 2: Si estás corriendo el archivo en tu PC local (Visual Studio Code)
    else:
        cliente = gspread.service_account(filename="credenciales.json")

    # Abrir la hoja
    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    
    # ==========================================
    # 📈 3. Lectura y Graficación de Valores Pasados
    # ==========================================
    # 📥 Traer TODOS los registros pasados de la hoja
    datos = hoja.get_all_records()

    if datos:
        # Convertimos los datos a un DataFrame de Pandas (ideal para gráficas)
        df = pd.DataFrame(datos)
        
        # Limpieza de datos (por si acaso)
        df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)
        df['Precio'] = pd.to_numeric(df['Precio'])

        # --- SECCIÓN DE MÉTRICAS RÁPIDAS ---
        ultimo_precio = df['Precio'].iloc[-1]
        precio_anterior = df['Precio'].iloc[-2] if len(df) > 1 else ultimo_precio
        variacion = ultimo_precio - precio_anterior

        col1, col2, col3 = st.columns(3)
        
        col1.metric(
            label="💵 Precio Actual (FIX)", 
            value=f"${ultimo_precio:.4f} MXN", 
            delta=f"{variacion:.4f} MXN"
        )
        
        col2.metric(
            label="📈 Máximo Histórico", 
            value=f"${df['Precio'].max():.4f} MXN"
        )
        
        col3.metric(
            label="📉 Mínimo Histórico", 
            value=f"${df['Precio'].min():.4f} MXN"
        )

        st.divider()

        # --- SECCIÓN DE GRÁFICA ---
        st.subheader("📉 Tendencia Visual de Valores Pasados")
        # Graficamos poniendo la Fecha en el eje X y el Precio en el eje Y
        st.line_chart(df.set_index('Fecha')['Precio'])

        st.divider()

        # --- SECCIÓN DE TABLA DESPLEGABLE ---
        with st.expander("📂 Ver la base de datos completa"):
            # Ordenamos del más nuevo al más viejo para que sea más fácil de leer
            df_ordenado = df.sort_values(by='Fecha', ascending=False)
            st.dataframe(df_ordenado, use_container_width=True)

    else:
        st.warning("⚠️ La hoja de cálculo está conectada pero parece estar vacía.")

except Exception as e:
    st.error(f"❌ Error de Conexión: No se pudo conectar a Google Sheets. Detalle: {e}")
    st.info("Revisa si copiaste correctamente tus credenciales en los secretos de Streamlit o si el ID de la hoja es correcto.")