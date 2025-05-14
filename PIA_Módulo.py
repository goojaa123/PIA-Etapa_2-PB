import requests
import time

# Token de acceso a la API
TOKEN = 'ed827f5b-3bcc-4786-9289-311d219ea21e'

# Función para obtener datos de la API con manejo de errores y reintentos
def obtener_datos_api(latitud, longitud, token, radio=250, intentos_maximos=5, espera_segundos=2):
    url = f'https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/camiones/{latitud},{longitud}/{radio}/{token}'
    for intento in range(intentos_maximos):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if not data or not isinstance(data, list):
                    print(f"Error al obtener datos desde la API para la ubicación ({latitud}, {longitud})")
                    return []
                return data
            else:
                print(f"Error: API no responde correctamente (Status code {response.status_code})")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            if intento < intentos_maximos - 1:
                print(f"Reintentando... (Intento {intento + 1} de {intentos_maximos})")
                time.sleep(espera_segundos)
            else:
                print("Se alcanzó el número máximo de reintentos.")
                return []
