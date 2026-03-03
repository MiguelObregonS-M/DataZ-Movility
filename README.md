# DataZ Movility – Análisis horario del sistema Bizi Zaragoza

## Descripción
DataZ Movility es un proyecto de análisis de movilidad urbana centrado en el sistema de bicicletas públicas Bizi Zaragoza. Durante 24 horas se capturaron datos horarios de disponibilidad de bicicletas y anclajes en todas las estaciones de la ciudad, construyendo un pipeline ETL automatizado y un dashboard profesional en Power BI.
El objetivo es entender patrones de uso, identificar estaciones críticas y evaluar la eficiencia del sistema.

## Objetivos del proyecto
•	Capturar datos horarios reales del sistema Bizi.
•	Construir un pipeline ETL robusto y automatizado.
•	Limpiar, transformar y consolidar los datos en un dataset analítico.
•	Diseñar un dashboard profesional con insights horarios.
•	Detectar patrones temporales, anomalías y estaciones críticas.

## Arquitectura del pipeline
El pipeline se ejecuta cada hora y sigue esta estructura:
1.	hourly_capture.py Llama a la API de Bizi y guarda un snapshot RAW en formato JSON.
2.	hourly_clean.py Limpia únicamente el snapshot más reciente y genera un archivo procesado.
3.	hourly_consolidate.py Añade el snapshot limpio al histórico consolidado.
4.	run_hourly.py Orquesta todo el proceso.
5.	regenerate_processed.py Permite regenerar todo el dataset desde los RAW en caso de errores.
Flujo: RAW → CLEAN → CONSOLIDADO → Power BI

## Estructura del repositorio
DataZ Movility/
│
├── data/
│   ├── raw/hourly_snapshots/        # Datos capturados cada hora (JSON)
│   ├── processed/hourly_clean/      # Datos limpios por snapshot (CSV)
│   └── hourly/bizi_hourly.csv       # Dataset consolidado final
│
├── src/
│   ├── hourly_capture.py
│   ├── hourly_clean.py
│   ├── hourly_consolidate.py
│   ├── run_hourly.py
│   └── regenerate_processed.py
│
└── dashboard/
    └── DataZ_Movility.pbix
	
## Dataset
•	Fuente: API pública de Bizi Zaragoza.
•	Frecuencia: 1 snapshot cada media hora.
•	Duración: 24 horas (ampliable con mayores recursos) .
•	Contenido:
o	ID de estación
o	Nombre
o	Bicis disponibles
o	Anclajes disponibles
o	Capacidad
o	Ratio de ocupación
o	Categoría de ocupación
o	Coordenadas
o	Estado
o	Timestamp

## Problemas encontrados y soluciones
1. RAW vacíos o corruptos
La API devolvió archivos vacíos en horas de baja actividad. Solución: el pipeline ignora RAW vacíos y continúa sin romperse.
2. Procesamiento duplicado
El pipeline original procesaba los RAW cada media hora, machacando datos. Solución: se modificó para procesar solo el snapshot más reciente.
3. Consolidado incorrecto
El consolidado se regeneraba entero cada media hora. Solución: ahora solo añade el último CLEAN.
4. Regeneración completa del dataset
Se creó un script para reconstruir todo desde RAW de forma segura.

## Dashboard (Power BI)
El dashboard contiene varias fases:
1.  Análisis globales
Mapas, gráficos y KPIs principales.
2. Análisis horarios
•	Variación 24h
•	% Variación 24h
•	Anomalías detectadas
•	Evolución horaria por estación
•	Mapa de estaciones

3. Conclusiones
## Conclusiones del análisis
•	El uso del sistema Bizi presenta picos claros en horas laborales.
•	Las estaciones del centro y zonas universitarias tienen mayor rotación.
•	Algunas estaciones presentan saturación temporal.
•	La redistribución podría optimizarse en franjas concretas.
•	El pipeline final es robusto, reproducible y escalable.
## Próximos pasos
•	Integrar datos meteorológicos.
•	Añadir análisis espacial avanzado (clusters, hotspots).
•	Implementar predicción simple de ocupación.
•	Automatizar logs y alertas del pipeline.

## Cómo ejecutar el proyecto
1.	Activar el entorno virtual.
2.	Ejecutar el pipeline manualmente:
Código
python src/run_hourly.py
3.	Regenerar datos desde RAW (opcional):
Código
python src/regenerate_processed.py
4.	Abrir el dashboard en Power BI y refrescar.

