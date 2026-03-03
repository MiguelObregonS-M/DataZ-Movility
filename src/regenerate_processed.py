import json
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw" / "hourly_snapshots"
CLEAN_DIR = BASE_DIR / "data" / "processed" / "hourly_clean"
OUT_DIR = BASE_DIR / "data" / "hourly"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# 1. Función de limpieza (misma que hourly_clean.py)
# ---------------------------

def limpiar_snapshot(archivo):
    # Si el archivo está vacío → saltar
    if archivo.stat().st_size == 0:
        print(f"⚠️ RAW vacío: {archivo.name}, se ignora.")
        return pd.DataFrame()

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ RAW corrupto o no JSON: {archivo.name}, se ignora. Error: {e}")
        return pd.DataFrame()

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
        try:
            ts = datetime.strptime(ts_raw, "%Y-%m-%d_%H-%M")
        except:
            print(f"⚠️ Timestamp inválido en {archivo.name}, se ignora.")
            return pd.DataFrame()

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

# ---------------------------
# 2. Regenerar todos los CLEAN
# ---------------------------

def regenerar_clean():
    print("\n=== Regenerando archivos CLEAN desde RAW ===\n")

    archivos = sorted(RAW_DIR.glob("*.json"))
    if not archivos:
        print("No hay RAW para procesar.")
        return

    for archivo in archivos:
        df = limpiar_snapshot(archivo)

        # Si el DF está vacío → no generar archivo
        if df.empty:
            print(f"⚠️ No se genera CLEAN para {archivo.name} (vacío o inválido).")
            continue

        salida = CLEAN_DIR / f"{archivo.stem}.csv"
        df.to_csv(salida, index=False, encoding="utf-8")
        print(f"Limpio: {salida}")

# ---------------------------
# 3. Reconstruir el consolidado completo
# ---------------------------

def regenerar_consolidado():
    print("\n=== Reconstruyendo consolidado completo ===\n")

    archivos = sorted(CLEAN_DIR.glob("*.csv"))
    dfs = []

    for archivo in archivos:
        try:
            df = pd.read_csv(archivo)
            if df.empty:
                print(f"Saltando vacío: {archivo.name}")
                continue

            df["station_id"] = df["station_id"].astype(int)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            dfs.append(df)

        except Exception as e:
            print(f"Error en {archivo.name}: {e}")

    if not dfs:
        print("No hay datos válidos para consolidar.")
        return

    df_final = pd.concat(dfs, ignore_index=True)
    df_final = df_final.sort_values(["station_id", "timestamp"])

    salida = OUT_DIR / "bizi_hourly.csv"
    df_final.to_csv(salida, index=False, encoding="utf-8")

    print(f"\nConsolidado regenerado correctamente con {len(df_final)} filas.")
    print(f"Guardado en: {salida}")

# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":
    regenerar_clean()
    regenerar_consolidado()
    print("\n=== REGENERACIÓN COMPLETA ===\n")
