import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data" / "processed" / "hourly_clean"
OUT_DIR = BASE_DIR / "data" / "hourly"

OUT_DIR.mkdir(parents=True, exist_ok=True)

def consolidar():
    archivos = sorted(CLEAN_DIR.glob("*.csv"))
    if not archivos:
        print("No hay archivos limpios para consolidar.")
        return

    ultimo = archivos[-1]  # SOLO EL MÁS RECIENTE

    try:
        df_nuevo = pd.read_csv(ultimo)

        if df_nuevo.empty:
            print(f"Saltando archivo vacío: {ultimo.name}")
            return

        df_nuevo["station_id"] = df_nuevo["station_id"].astype(int)
        df_nuevo["timestamp"] = pd.to_datetime(df_nuevo["timestamp"])

    except Exception as e:
        print(f"Error procesando {ultimo.name}: {e}")
        return

    hist_path = OUT_DIR / "bizi_hourly.csv"

    if hist_path.exists():
        df_hist = pd.read_csv(hist_path)
        df_hist["timestamp"] = pd.to_datetime(df_hist["timestamp"])
        df_final = pd.concat([df_hist, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final = df_final.sort_values(["station_id", "timestamp"])
    df_final.to_csv(hist_path, index=False, encoding="utf-8")

    print(f"Histórico actualizado correctamente con {len(df_final)} filas.")


if __name__ == "__main__":
    consolidar()
