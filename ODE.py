import streamlit as st
import gspread

st.set_page_config(page_title="Calculadora Dólar FIX", page_icon="🧮")
st.title("🧮 Calculadora de Dólar Oficial")

ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

try:
    if "gcp_service_account" in st.secrets:
        cliente = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    else:
        cliente = gspread.service_account(filename="credenciales.json")

    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    todos_los_datos = hoja.get_all_values()

    if len(todos_los_datos) > 1:
        datos_reales = [f for f in todos_los_datos[1:] if len(f) >= 2 and f[0].strip() != "" and f[1].strip() != ""]

        if datos_reales:
            st.subheader("📅 Historial de Fechas")
            opciones_fechas = [f"{fila[0]} (Precio: ${fila[1]})" for fila in datos_reales]
            
            # Seleccionar penúltimo (ayer) si existe, si no el último
            indice_defecto = len(opciones_fechas) - 2 if len(opciones_fechas) > 1 else 0

            seleccion = st.selectbox("Selecciona un registro:", options=opciones_fechas, index=indice_defecto)

            # Extraer y convertir a flotante con limpieza de comas
            fila_elegida = datos_reales[opciones_fechas.index(seleccion)]
            fecha_actual = fila_elegida[0]
            
            # --- AQUÍ ESTÁ EL ARREGLO DEL FLOTANTE ---
            precio_limpio = str(fila_elegida[1]).replace(',', '.').strip()
            precio_dolar = float(precio_limpio) 

            st.divider()
            st.metric(label=f"Tipo de Cambio ({fecha_actual})", value=f"${precio_dolar:.4f} MXN")

            cantidad_usd = st.number_input("Cantidad en Dólares (USD):", min_value=0.0, value=1.0)
            st.success(f"### 💰 Resultado: ${cantidad_usd * precio_dolar:,.2f} MXN")
        else:
            st.warning("La hoja existe pero no tiene datos válidos.")
    else:
        st.warning("La hoja está vacía.")

except Exception as e:
    st.error(f"❌ Error: {e}")