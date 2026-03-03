import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
SNAP_DIR = RAW_DIR / "hourly_snapshots"

SNAP_DIR.mkdir(parents=True, exist_ok=True)

def capturar_snapshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    origen = RAW_DIR / "bizi.json"
    destino = SNAP_DIR / f"bizi_{timestamp}.json"

    if not origen.exists():
        raise FileNotFoundError(f"No existe el archivo base: {origen}")

    shutil.copy(origen, destino)
    print(f"Snapshot guardado en: {destino}")

if __name__ == "__main__":
    capturar_snapshot()
