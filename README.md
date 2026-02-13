# MineriaProyecto1

Autores:
Melisa Mendizabal y Renato Rojas

## Descripción del proyecto
Este proyecto realiza un análisis exploratorio y de minería de datos sobre registros de matrimonios en Guatemala durante el período 2012–2022. Se trabajó con bases de datos en formato .sav (SPSS), realizando:
- Limpieza y normalización de datos
- Análisis estadístico descriptivo
- Visualización de variables numéricas y categóricas
- Cruces de variables
- Análisis de correlaciones
- Clustering (K-Means)

El objetivo principal es identificar patrones demográficos, tendencias temporales y segmentaciones relevantes en los matrimonios registrados en el país.

## Estructura del Proyecto
### proyecto.py
- Carga y unificación de los datos
- Limpieza y normalización
- Conversión de variables
- Eliminación de valores atípicos específicos
- Menú interactivo para ejecutar análisis

### serieB.py
Contiene funciones para:
- Gráficos numéricos
- Frecuencias
- Cruce de variables
- Mapas de calor
- Tendencias temporales

### serieC.py
- Análisis por tipo de unión
- Gráficos de dispersión
- Matriz de correlación
- Visualización de variables categóricas

📄 clustering.py
- Preprocesamiento con Pipeline
- OneHotEncoding
- Escalamiento
- K-Means (k=3)
- Método del codo (opcional)
- Silhouette Score
- Interpretación de clusters


## Tecnologías Utilizadas
- Python 3
- pandas
- NumPy
- SciPy
- Seaborn
- Matplotlib
- Siikit-learn




