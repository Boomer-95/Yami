import os
import json
import requests
import gspread
# ==========================================
# 🔧 Configuración
# ==========================================
TOKEN_BANXICO = "3cef102a89a5e07a3496c0476d61370a0dc5d655600d2aeb3d20e82be969f54e"
SERIE_DOLAR_FIX = "SF43718"
ARCHIVO_JSON = "credenciales.json" # Tu archivo de permisos renombrado
ID_HOJA_CALCULO = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

print("\n🤖 Iniciando Robot del Dólar Oficial...")

# ==========================================
# 🏦 1. Leer el dólar de Banxico
# ==========================================
try:
    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{SERIE_DOLAR_FIX}/datos/oportuno"
    headers = {"Bmx-Token": TOKEN_BANXICO}
    
    respuesta = requests.get(url, headers=headers)
    datos = respuesta.json()
    
    ultimo_dato = datos['bmx']['series'][0]['datos'][0]
    fecha_banxico = ultimo_dato['fecha'] # DD/MM/AAAA
    precio_dolar = float(ultimo_dato['dato'])
    
    print(f"✅ Dólar obtenido de Banxico: ${precio_dolar} MXN")

except Exception as e:
    print(f"❌ Error al leer de Banxico: {e}")
    exit()

try:
    # 🕵️‍♂️ ¿Estamos en GitHub o en tu computadora local?
    if "GOOGLE_CREDENTIALS" in os.environ:
        # Si estamos en GitHub, saca la llave del Secreto
        info_credenciales = json.loads(os.environ["GOOGLE_CREDENTIALS"])
        cliente = gspread.service_account_from_dict(info_credenciales)
    else:
        # Si estás en tu PC local, usa tu archivo credenciales.json tradicional
        cliente = gspread.service_account(filename="credenciales.json")

    hoja = cliente.open_by_key(ID_HOJA_CALCULO).worksheet("Hoja 1")
    
    fechas_existentes = hoja.col_values(1)

    if fecha_banxico in fechas_existentes:
        print(f"⚠️ El registro del {fecha_banxico} ya existe. Nada que agregar.\n")
    else:
        hoja.append_row([fecha_banxico, precio_dolar])
        print(f"🎉 ¡ÉXITO! Se agregó {fecha_banxico} con valor ${precio_dolar} al Google Sheet.\n")

except Exception as e:
    print(f"❌ Error al escribir en Google Sheets: {e}\n")