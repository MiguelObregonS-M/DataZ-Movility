import os
import requests

DATA_DIR = "../data/raw"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def asegurar_directorio():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def descargar(url, destino):
    print(f"Descargando: {url}")
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    with open(destino, "w", encoding="utf-8") as f:
        f.write(r.text)
    print(f"Guardado en: {destino}")


# -----------------------------
# BIZI
# -----------------------------
def descargar_bizi():
    url = (
        "https://www.zaragoza.es/sede/servicio/"
        "urbanismo-infraestructuras/estacion-bicicleta.geojson?rf=json&rows=500"
    )
    destino = f"{DATA_DIR}/bizi.geojson"
    descargar(url, destino)


# -----------------------------
# TRÁFICO (endpoint clásico)
# -----------------------------
def descargar_trafico_tramos():
    url = "http://www.zaragoza.es/trafico/estado/tramos.json"
    destino = f"{DATA_DIR}/trafico_tramos.json"
    descargar(url, destino)


# -----------------------------
# CONTAMINACIÓN (Open Data Aragón)
# -----------------------------
def descargar_contaminacion_ultima():
    url = "https://opendata.aragon.es/servicios/medioambiente/calidad-aire/ultima"
    destino = f"{DATA_DIR}/contaminacion_ultima.json"
    descargar(url, destino)

def descargar_contaminacion_historico():
    url = "https://opendata.aragon.es/servicios/medioambiente/calidad-aire/historico"
    destino = f"{DATA_DIR}/contaminacion_historico.json"
    descargar(url, destino)


# -----------------------------
# DESCARGA COMPLETA
# -----------------------------
def descargar_todo():
    asegurar_directorio()
    descargar_bizi()
    descargar_trafico_tramos()
    descargar_contaminacion_ultima()
    descargar_contaminacion_historico()

