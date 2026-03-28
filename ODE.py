import streamlit as st
import gspread

# 1. Configuración visual de la página
st.set_page_config(page_title="Calculadora Dólar FIX", page_icon="🧮")

st.title("🧮 Calculadora de Dólar Oficial")
st.write("Convierte tus dólares a pesos mexicanos usando datos oficiales de Banxico.")

# ⚠️ REEMPLAZA ESTO CON EL ID REAL DE TU GOOGLE SHEET
ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

try:
    # 2. Conexión Inteligente (Nube o Local)
    if "gcp_service_account" in st.secrets:
        cliente = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    else:
        cliente = gspread.service_account(filename="credenciales.json")

    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    
    # 3. Traer todos los valores pasados de la hoja
    todos_los_datos = hoja.get_all_values()

    if len(todos_los_datos) > 1:
        # Separamos los encabezados (Fila 1) de los datos reales
        datos_sin_encabezado = todos_los_datos[1:]

        # --- AQUÍ ESTÁ EL FILTRO DE FECHAS ---
        st.subheader("📅 Selecciona la fecha para el cálculo")
        
        # Creamos una lista de opciones con el formato "Fecha - Precio"
        opciones_fechas = [f"{fila[0]} (Precio: ${fila[1]})" for fila in datos_sin_encabezado]
        
        # El usuario elige una fecha del pasado en el menú (por defecto mostramos la última)
        seleccion = st.selectbox(
            "Selecciona un registro del historial:", 
            options=opciones_fechas,
            index=len(opciones_fechas) - 1 # Enfocado siempre en el día más reciente
        )

        # Encontramos qué fila seleccionó el usuario para extraer el precio exacto de ese día
        indice_seleccionado = opciones_fechas.index(seleccion)
        fila_elegida = datos_sin_encabezado[indice_seleccionado]
        
        fecha_actual = fila_elegida[0]
        
        # Corregimos la coma por punto para que Python no falle en la matemática
        precio_texto = str(fila_elegida[1]).replace(',', '.')
        precio_dolar = float(precio_texto)

        # --- SECCIÓN DE LA CALCULADORA ---
        st.divider()
        st.metric(label=f"Tipo de Cambio elegido ({fecha_actual})", value=f"${precio_dolar:.4f} MXN")

        st.subheader("Realizar Conversión")
        cantidad_usd = st.number_input("Cantidad en Dólares (USD):", min_value=0.0, value=1.0, step=1.0)

        resultado_mxn = cantidad_usd * precio_dolar

        st.success(f"### 💰 Resultado: ${resultado_mxn:,.2f} MXN")
        st.write(f"Operación: {cantidad_usd} USD x {precio_dolar} MXN")
        
    else:
        st.warning("⚠️ Parece que la base de datos está vacía o solo tiene encabezados.")

except Exception as e:
    st.error(f"❌ Error al cargar la aplicación: {e}")