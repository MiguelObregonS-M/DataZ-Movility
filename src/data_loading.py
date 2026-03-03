import requests
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def asegurar_directorio():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def descargar(url, destino):
    print(f"Descargando: {url}")
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    destino.write_text(r.text, encoding="utf-8")
    print(f"Guardado en: {destino}")

def descargar_bizi():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    url = (
    "https://www.zaragoza.es/sede/servicio/"
    f"urbanismo-infraestructuras/estacion-bicicleta?rf=json&rows=2000&_={timestamp}"
)

    destino = DATA_DIR / "bizi.json"
    descargar(url, destino)

def descargar_todo():
    asegurar_directorio()
    descargar_bizi()

if __name__ == "__main__":
    descargar_todo()
