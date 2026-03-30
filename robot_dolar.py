import os
import requests
import gspread
from datetime import datetime

# 1. Ahora leemos el token desde los Secrets de GitHub
TOKEN_BANXICO = os.getenv("BANXICO_TOKEN") 
ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

# 2. Obtener el dato OPORTUNO (el más reciente)
url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
headers = {"Bmx-Token": TOKEN_BANXICO}

response = requests.get(url, headers=headers)
data = response.json()

# Extraer fecha y precio
serie = data['bmx']['series'][0]['datos'][0]
fecha_banxico = serie['fecha'] 
precio_banxico = serie['dato']

# 3. Conectar a Google Sheets
gc = gspread.service_account(filename='credenciales.json')
hoja = gc.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")

# --- LÓGICA DE SEGURIDAD PARA EL LUNES ---
# Obtenemos el último dato que ya tenemos en el Excel
filas = hoja.get_all_values()
ultima_fecha_excel = filas[-1][0] if len(filas) > 1 else ""

# Solo escribimos si Banxico tiene una fecha nueva (diferente a la del viernes)
if fecha_banxico != ultima_fecha_excel:
    hoja.append_row([fecha_banxico, precio_banxico])
    print(f"✅ ¡Éxito! Se guardó el dato de hoy: {fecha_banxico}")
else:
    print(f"⚠️ Banxico aún tiene el dato de {fecha_banxico}. No se guardó duplicado.")