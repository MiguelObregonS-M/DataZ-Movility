import json
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
SNAP_DIR = BASE_DIR / "data" / "raw" / "hourly_snapshots"
CLEAN_DIR = BASE_DIR / "data" / "processed" / "hourly_clean"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def limpiar_snapshot(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        data = json.load(f)

    estaciones = data["result"] if isinstance(data, dict) and "result" in data else data

    filas = []
    for est in estaciones:

        if not isinstance(est, dict):
            continue

        if "bicisDisponibles" not in est or "anclajesDisponibles" not in est:
            continue

        geom = est.get("geometry")

        if isinstance(geom, dict) and "coordinates" in geom:
            lon, lat = geom["coordinates"]

        elif isinstance(geom, str) and geom.startswith("POINT"):
            coords = geom.replace("POINT", "").replace("(", "").replace(")", "").strip()
            lon, lat = map(float, coords.split())

        else:
            lon, lat = None, None

        bikes = est["bicisDisponibles"]
        slots = est["anclajesDisponibles"]
        capacity = bikes + slots

        ratio = bikes / capacity if capacity > 0 else None

        if ratio is None:
            categoria = "desconocido"
        elif ratio < 0.33:
            categoria = "baja"
        elif ratio < 0.66:
            categoria = "media"
        else:
            categoria = "alta"

        ts_raw = archivo.stem.replace("bizi_", "")
        ts = datetime.strptime(ts_raw, "%Y-%m-%d_%H-%M")
        ts_iso = ts.strftime("%Y-%m-%d %H:%M:%S")

        filas.append({
            "station_id": est["id"],
            "station_name": est["title"],
            "bikes": bikes,
            "slots": slots,
            "capacity": capacity,
            "ratio_ocupacion": ratio,
            "ocupacion_categoria": categoria,
            "status": est.get("estado"),
            "lon": lon,
            "lat": lat,
            "lastUpdated": est.get("lastUpdated"),
            "timestamp": ts_iso
        })

    df = pd.DataFrame(filas)

    if not df.empty:
        df["bikes"] = df["bikes"].astype(int)
        df["slots"] = df["slots"].astype(int)
        df["capacity"] = df["capacity"].astype(int)
        df["lon"] = df["lon"].astype(float)
        df["lat"] = df["lat"].astype(float)

    return df


def procesar_ultimo():
    archivos = sorted(SNAP_DIR.glob("*.json"))
    if not archivos:
        print("No hay snapshots RAW.")
        return

    archivo = archivos[-1]  # SOLO EL MÁS RECIENTE
    df = limpiar_snapshot(archivo)

    salida = CLEAN_DIR / f"{archivo.stem}.csv"
    df.to_csv(salida, index=False, encoding="utf-8")

    print(f"Limpio: {salida}")


if __name__ == "__main__":
    procesar_ultimo()
