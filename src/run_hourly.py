import subprocess
from pathlib import Path
from datetime import datetime
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

PYTHON = sys.executable

def run(script):
    script_path = SRC_DIR / script
    print(f"\n[{datetime.now()}] Ejecutando {script} con {PYTHON}...\n")

    result = subprocess.run(
        [PYTHON, str(script_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] {script} falló:\n{result.stderr}")
        raise SystemExit(1)

    print(result.stdout)

def main():
    print("\n=== INICIO CICLO HORARIO ===\n")

    run("data_loading.py")
    run("hourly_capture.py")
    run("hourly_clean.py")
    run("hourly_consolidate.py")

    print("\n=== CICLO COMPLETADO CORRECTAMENTE ===\n")

if __name__ == "__main__":
    main()
