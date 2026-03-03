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
DataZ-Movility/
│
├── src/                  # Scripts del pipeline ETL
├── data/                 # Datos brutos, procesados y finales
├── notebooks/            # Exploración y análisis
├── dashboard/            # Dashboard PBIX, PDF y capturas
├── README.md             # Documentación principal
├── requirements.txt      # Dependencias del proyecto
└── run_hourly.bat        # Ejecución automatizada del pipeline

	
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

##Pipeline ETL
El pipeline está dividido en cuatro etapas principales:

1. Captura
hourly_capture.py  
Obtiene datos horarios desde la API de Bizi Zaragoza y los guarda en formato JSON.

2. Limpieza
hourly_clean.py  
Normaliza campos, corrige tipos, elimina duplicados y valida registros.

3. Consolidación
hourly_consolidate.py  
Une todos los snapshots limpios en un único dataset histórico.

4. Regeneración
regenerate_processed.py  
Reconstruye todos los archivos procesados desde cero.

Automatización
run_hourly.bat  
Permite ejecutar el pipeline automáticamente desde el programador de tareas de Windows.

## Dashboard (Power BI)
Incluye:

Disponibilidad total del sistema
Variación 24h y % variación
Detección de anomalías
Ranking de estaciones
Mapa interactivo
Insights horarios
Tendencias y patrones

El dashboard está disponible en:
dashboard/DataZ_Movility.pbix
dashboard/DataZ_Movility.pdf

##Análisis y notebooks
Los notebooks documentan todo el proceso:

Exploración inicial
Limpieza y validación
Análisis descriptivo
Visualizaciones
Análisis horario

Se encuentran en la carpeta notebooks/.

##Datos incluidos
Datos finales:
data/hourly/bizi_hourly.csv
data/processed/bizi_clean.csv
data/processed/bizi_visual_ready.csv
data/processed/bizi_preliminar.geojson

Datos originales:
data/raw/bizi.json
data/raw/bizi.geojson
Datos intermedios excluidos

Se excluyen del repositorio por tamaño y por no aportar valor:
data/processed/hourly_clean/
data/raw/hourly_snapshots/

##Tecnologías utilizadas
Python (pandas, requests, json, os)
Power BI
Jupyter Notebook
Git + GitHub
Programador de tareas de Windows

## Problemas encontrados y soluciones
1. RAW vacíos o corruptos
La API devolvió archivos vacíos en horas de baja actividad. Solución: el pipeline ignora RAW vacíos y continúa sin romperse.
2. Procesamiento duplicado
El pipeline original procesaba los RAW cada media hora, machacando datos. Solución: se modificó para procesar solo el snapshot más reciente.
3. Consolidado incorrecto
El consolidado se regeneraba entero cada media hora. Solución: ahora solo añade el último CLEAN.
4. Regeneración completa del dataset
Se creó un script para reconstruir todo desde RAW de forma segura.

## Conclusiones del análisis
•	El uso del sistema Bizi presenta picos claros en horas laborales.
•	Las estaciones del centro y zonas universitarias tienen mayor rotación.
•	Algunas estaciones presentan saturación temporal.
•	La redistribución podría optimizarse en franjas concretas.
•	El pipeline final es robusto, reproducible y escalable.

## Próximos pasos
•	Integrar datos meteorológicos.
•	Añadir análisis espacial avanzado (clusters, hotspots).
•	Automatizar logs y alertas del pipeline.
•	Modelos predictivos de demanda
•	Análisis de estacionalidad
•	API propia para servir datos procesados

## Cómo ejecutar el proyecto
1.	Activar el entorno virtual.
2.	Ejecutar el pipeline manualmente:
Código
python src/run_hourly.py
3.	Regenerar datos desde RAW (opcional):
Código
python src/regenerate_processed.py
4.	Abrir el dashboard en Power BI y refrescar.

## Licencia
MIT License

## Autor
Miguel Obregón
Zaragoza, España