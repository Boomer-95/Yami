import streamlit as st
import gspread

# 1. Configuración básica
st.title("🧮 Calculadora de Dólar Oficial")
st.write("Convierte tus dólares a pesos mexicanos usando el valor FIX más reciente de Banxico.")

# REEMPLAZA CON TU ID DE HOJA
ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

try:
    # 2. Conexión a los datos
    if "gcp_service_account" in st.secrets:
        cliente = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    else:
        cliente = gspread.service_account(filename="credenciales.json")

    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    
    # 3. Obtener el ÚLTIMO valor registrado por el robot
    # Suponiendo que la columna B tiene el precio y la última fila es la más nueva
    todos_los_datos = hoja.get_all_values()
    ultima_fila = todos_los_datos[-1] # Toma la última fila que escribió el robot
    fecha_actual = ultima_fila[0]
    precio_dolar = float(ultima_fila[1])

    # 4. Interfaz de la Calculadora
    st.info(f"📅 Valor actualizado al: **{fecha_actual}**")
    st.metric(label="Tipo de Cambio (FIX)", value=f"${precio_dolar:.4f} MXN")

    st.subheader("Realizar Conversión")
    cantidad_usd = st.number_input("Cantidad en Dólares (USD):", min_value=0.0, value=1.0, step=1.0)

    # El cálculo matemático
    resultado_mxn = cantidad_usd * precio_dolar

    st.success(f"### 💰 Resultado: ${resultado_mxn:,.2f} MXN")
    st.write(f"Operación: {cantidad_usd} USD x {precio_dolar} MXN")

except Exception as e:
    st.error(f"Error al cargar la calculadora: {e}")