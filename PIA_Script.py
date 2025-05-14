import json
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIA_Módulo import obtener_datos_api, TOKEN

# Coordenadas para realizar consultas en diferentes ubicaciones
coordenadas = [
    (21.85717833, -102.28487238),  # Aguascalientes, Aguascalientes
    (19.432608, -99.133209),       # Ciudad de México
    (25.686614, -100.316113)       # Monterrey, Nuevo León
]

# Lista para almacenar los datos de todas las consultas
transportes = []

# Realizar consultas para cada conjunto de coordenadas
token = TOKEN
for lat, lon in coordenadas:
    datos = obtener_datos_api(lat, lon, token)
    for establecimiento in datos:
        try:
            lat = float(establecimiento['Latitud'])
            lon = float(establecimiento['Longitud'])
            transportes.append({
                'nombre': establecimiento.get('Nombre', 'No disponible'),
                'actividad': establecimiento.get('Clase_actividad', 'No disponible'),
                'latitud': lat,
                'longitud': lon,
                'razon_social': establecimiento.get('Razon_social', 'No disponible'),
                'direccion': establecimiento.get('Calle', 'Sin dirección')
            })
        except (ValueError, KeyError, TypeError):
            continue  # Ignora registros con datos incorrectos

# Guardar archivo JSON
with open('transportes.json', 'w', encoding='utf-8') as f:
    json.dump(transportes, f, ensure_ascii=False, indent=4)

# Limpieza de datos: filtrar nombres no vacíos
transportes_limpios = [t for t in transportes if t['nombre'].strip()]

# Análisis estadístico
latitudes = [t['latitud'] for t in transportes_limpios]
longitudes = [t['longitud'] for t in transportes_limpios]

# Función para calcular la varianza de manera segura
def calcular_varianza(datos):
    if len(datos) > 1:
        return statistics.variance(datos)
    else:
        return None  # No hay suficientes datos para calcular la varianza

# Función para calcular la moda de manera segura
def calcular_moda(datos):
    try:
        return statistics.mode(datos)
    except statistics.StatisticsError:
        return None  # No hay moda definida si hay varios valores

# Imprimir estadísticas para latitudes
print("Media de latitudes:", statistics.mean(latitudes))
print("Mediana de latitudes:", statistics.median(latitudes))
moda_latitudes = calcular_moda(latitudes)
if moda_latitudes:
    print("Moda de latitudes:", moda_latitudes)
else:
    print("No hay moda en las latitudes")
varianza_latitudes = calcular_varianza(latitudes)
if varianza_latitudes is not None:
    print("Varianza de latitudes:", varianza_latitudes)
else:
    print("No hay suficientes datos para calcular la varianza de latitudes")
print("Desviación estándar de latitudes:", statistics.stdev(latitudes) if len(latitudes) > 1 else 'Insuficientes datos')

# Imprimir estadísticas para longitudes
print("Media de longitudes:", statistics.mean(longitudes))
print("Mediana de longitudes:", statistics.median(longitudes))
moda_longitudes = calcular_moda(longitudes)
if moda_longitudes:
    print("Moda de longitudes:", moda_longitudes)
else:
    print("No hay moda en las longitudes")
varianza_longitudes = calcular_varianza(longitudes)
if varianza_longitudes is not None:
    print("Varianza de longitudes:", varianza_longitudes)
else:
    print("No hay suficientes datos para calcular la varianza de longitudes")
print("Desviación estándar de longitudes:", statistics.stdev(longitudes) if len(longitudes) > 1 else 'Insuficientes datos')

# Visualización
plt.figure(figsize=(10, 6))
plt.hist(latitudes, bins=10, color='skyblue', edgecolor='black')
plt.title('Distribución Geográfica de Empresas de Transporte (Latitud)')
plt.xlabel('Latitud')
plt.ylabel('Número de Empresas')
plt.grid(True)
plt.show()
plt.savefig("grafico_latitudes.png")

# Gráfico de líneas para latitudes y longitudes
plt.figure(figsize=(10, 6))
plt.plot(latitudes, label='Latitudes', color='skyblue')
plt.plot(longitudes, label='Longitudes', color='orange')
plt.title('Evolución de Latitudes y Longitudes de Empresas de Transporte')
plt.xlabel('Índice de Empresa')
plt.ylabel('Coordenadas')
plt.legend()
plt.grid(True)
plt.show()

# Exportar los datos a pandas
df = pd.DataFrame(transportes_limpios)

# Exportar a un archivo de Excel
try:
    df.to_excel('empresas_transporte.xlsx', index=False, engine='openpyxl')
    print("Los datos han sido exportados a 'empresas_transporte.xlsx'")
except Exception as e:
    print(f"Error al exportar a Excel: {e}")
