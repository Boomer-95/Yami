import os
import requests
import gspread
import json

# 1. Leer el secreto (Asegúrate que en el .yml diga BANXICO_TOKEN: ${{ secrets.TOKEN }})
token = os.getenv("BANXICO_TOKEN")
id_sheet = "1yk2bkHnJazeuZYBHfglfFQQho4Dd3oWz-qNwCm1ErUg"

try:
    # 2. Consultar Banxico
    url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
    headers = {"Bmx-Token": token}
    res = requests.get(url, headers=headers)
    res.raise_for_status() # Esto nos avisará si el token está mal
    
    data = res.json()
    dato = data['bmx']['series'][0]['datos'][0]
    fecha, valor = dato['fecha'], dato['dato']

    # 3. Conectar a Sheets (Usando el secreto de Google)
    creds_dict = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
    gc = gspread.service_account_from_dict(creds_dict)
    hoja = gc.open_by_key(id_sheet).worksheet("Hoja 1")

    # 4. Evitar duplicados
    valores = hoja.get_all_values()
    ultima_fecha = valores[-1][0] if len(valores) > 1 else ""

    if fecha != ultima_fecha:
        hoja.append_row([fecha, valor])
        print(f"✅ Guardado: {fecha} - ${valor}")
    else:
        print(f"⚠️ El dato de {fecha} ya existe.")

except Exception as e:
    print(f"❌ ERROR DETECTADO: {e}")
    exit(1) # Esto le avisa a GitHub que algo salió mal