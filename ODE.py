import streamlit as st
from datetime import timedelta
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Conversor DOF Oficial", page_icon="💰")

st.title("📊 Calculadora de Tipo de Cambio Oficial")
st.subheader("Consulta el valor publicado por el DOF del día anterior")
st.markdown("---")

# 🔗 1. CONEXIÓN DIRECTA AL GOOGLE SHEET
try:
    # Streamlit se conecta mágicamente al link del Sheet
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lee los datos de la hoja (ajusta el nombre si tu hoja se llama diferente)
    df = conn.read(worksheet="Hoja 1") 
except Exception as e:
    st.error(f"Error al conectar con Google Sheets: {e}")
    st.stop()


# 🎨 2. DISEÑO DE LA CALCULADORA
col1, col2 = st.columns(2)

with col1:
    monto_pesos = st.number_input("Cantidad en Pesos ($ MXN):", min_value=0.0, step=50.0)

with col2:
    fecha_usuario = st.date_input("Selecciona la fecha de hoy:")


if st.button("🧮 Calcular Conversión"):
    if monto_pesos <= 0:
        st.warning("Por favor, escribe una cantidad de pesos válida.")
    else:
        # Restamos un día para buscar la publicación de ayer
        fecha_anterior = fecha_usuario - timedelta(days=1)
        fecha_busqueda = fecha_anterior.strftime('%d/%m/%Y') # Formato DD/MM/AAAA
        
        st.info(f"📅 Buscando el dólar publicado el: **{fecha_busqueda}**")
        
        # 🔍 Buscamos la fecha en nuestra tabla de Pandas del Sheet
        # (Convertimos la columna 'Fecha' a texto para comparar fácil)
        registro = df[df['Fecha'].astype(str) == fecha_busqueda]
        
        if not registro.empty:
            # Sacamos el valor numérico del dólar
            tipo_cambio = float(registro['Valor_Dolar'].values[0])
            total_dolares = monto_pesos / tipo_cambio
            
            # Mostramos tarjetas visuales bonitas
            metrica1, metrica2 = st.columns(2)
            metrica1.metric(label="Tipo de Cambio Oficial", value=f"${tipo_cambio:.4f} MXN")
            metrica2.metric(label="Total en Dólares", value=f"${total_dolares:.2f} USD")
        else:
            st.error(f"No hay registro oficial para la fecha {fecha_busqueda} en la nube.")