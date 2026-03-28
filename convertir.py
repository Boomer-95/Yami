import json

# Abre el archivo que ya tienes en tu computadora
with open("credenciales.json", "r") as f:
    datos = json.load(f)

# Esto va a formatear la llave privada correctamente
llave_formateada = datos["private_key"].replace("\n", "\\n")

# Imprime el bloque TOML perfecto para Streamlit
print("\n=== COPIA DESDE LA SIGUIENTE LÍNEA ===\n")
print("[gcp_service_account]")
print(f'type = "{datos["type"]}"')
print(f'project_id = "{datos["project_id"]}"')
print(f'private_key_id = "{datos["private_key_id"]}"')
print(f'private_key = "{llave_formateada}"')
print(f'client_email = "{datos["client_email"]}"')
print(f'client_id = "{datos["client_id"]}"')
print(f'auth_uri = "{datos["auth_uri"]}"')
print(f'token_uri = "{datos["token_uri"]}"')
print(f'auth_provider_x509_cert_url = "{datos["auth_provider_x509_cert_url"]}"')
print(f'client_x509_cert_url = "{datos["client_x509_cert_url"]}"')
print('universe_domain = "googleapis.com"')
print("\n=== HASTA AQUÍ ===\n")