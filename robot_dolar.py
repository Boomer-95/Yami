import requests
import gspread
from datetime import datetime

# 1. Configuración de API y Google
TOKEN_BANXICO = "3cef102a89a5e07a3496c0476d61370a0dc5d655600d2aeb3d20e82be969f54e"
SERIE_DOLAR_FIX = "SF43718"
ARCHIVO_JSON = "credenciales.json" # Tu archivo de permisos renombrado
ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

# 2. Obtener el dato de HOY de Banxico
url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
headers = {"Bmx-Token": TOKEN_BANXICO}

response = requests.get(url, headers=headers)
data = response.json()

# Extraer fecha y precio
serie = data['bmx']['series'][0]['datos'][0]
fecha_hoy = serie['fecha']  # Ejemplo: "27/03/2026"
precio_hoy = serie['dato']   # Ejemplo: "18.0667"

# 3. Conectar a Google Sheets
# (Aquí usas tu método de service_account con el json)
gc = gspread.service_account(filename='credenciales.json')
hoja = gc.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")

# ==========================================
# 🔥 EL TRUCO PARA EL HISTORIAL: append_row
# ==========================================
# NO uses .update(), porque eso borra lo anterior.
# .append_row() busca el primer renglón vacío y escribe ahí.

hoja.append_row([fecha_hoy, precio_hoy])

print(f"✅ Guardado con éxito: {fecha_hoy} - ${precio_hoy}")