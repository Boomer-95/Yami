import streamlit as st
import gspread

# 1. Configuración visual de la página
st.set_page_config(page_title="Calculadora Dólar FIX", page_icon="🧮")

st.title("🧮 Calculadora de Dólar Oficial")
st.write("Convierte tus dólares a pesos mexicanos usando datos oficiales de Banxico.")

# ⚠️ TU ID DE HOJA DE CÁLCULO
ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

try:
    # 2. Conexión Inteligente (Nube o Local)
    if "gcp_service_account" in st.secrets:
        cliente = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    else:
        # Para pruebas locales en tu VS Code
        cliente = gspread.service_account(filename="credenciales.json")

    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    
    # 3. Traer todos los valores guardados por el robot
    todos_los_datos = hoja.get_all_values()

    if len(todos_los_datos) > 1:
        # Saltamos la fila 1 (los encabezados)
        datos_sin_encabezado = todos_los_datos[1:]

        st.subheader("📅 Historial de Fechas")
        
        # Lista para el menú desplegable
        opciones_fechas = [f"{fila[0]} (Precio: ${fila[1]})" for fila in datos_sin_encabezado]
        
        # --- LÓGICA DE SELECCIÓN AUTOMÁTICA ---
        # Si hay más de un dato, seleccionamos el PENÚLTIMO (Ayer = len - 2)
        # Si solo hay uno, seleccionamos ese (0)
        if len(opciones_fechas) > 1:
            indice_defecto = len(opciones_fechas) - 2
        else:
            indice_defecto = 0

        seleccion = st.selectbox(
            "Selecciona un registro del historial:", 
            options=opciones_fechas,
            index=indice_defecto
        )

        # Extraemos el precio del registro elegido
        indice_seleccionado = opciones_fechas.index(seleccion)
        fila_elegida = datos_sin_encabezado[indice_seleccionado]
        
        fecha_actual = fila_elegida[0]
        # Limpiamos comas por puntos para que la matemática no falle
        precio_texto = str(fila_elegida[1]).replace(',', '.')
        precio_dolar = float(precio_texto)

        # --- SECCIÓN DE LA CALCULADORA ---
        st.divider()
        st.info(f"Calculando con el valor del: **{fecha_actual}**")
        st.metric(label="Tipo de Cambio Aplicado", value=f"${precio_dolar:.4f} MXN")

        st.subheader("Realizar Conversión")
        cantidad_usd = st.number_input("Cantidad en Dólares (USD):", min_value=0.0, value=1.0, step=1.0)

        resultado_mxn = cantidad_usd * precio_dolar

        st.success(f"### 💰 Resultado: ${resultado_mxn:,.2f} MXN")
        st.write(f"Operación: {cantidad_usd} USD x {precio_dolar} MXN")
        
    else:
        st.warning("⚠️ El Google Sheets no tiene datos suficientes. Asegúrate de que el robot ya corrió o llena unas filas a mano.")

except Exception as e:
    st.error(f"❌ Error al cargar la aplicación: {e}")