from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from proyecto import df_final
import numpy as np

# ------------------------------------
# 1. Selección de variables

features = [
    'EDADHOM', 'EDADMUJ',
    'ESCHOM', 'ESCMUJ',
    'DEPREG', 'MESOCU'
]

X = df_final[features].copy()

#-------------------------------------------------------
# 2. Definir columnas numéricas y categóricas

cols_num = ['EDADHOM', 'EDADMUJ', 'MESOCU']
cols_cat = ['ESCHOM', 'ESCMUJ', 'DEPREG']

#---------------------------------------------------
# 3. Preprocesamiento

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), cols_num),

        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), cols_cat)
    ]
)

# ----------------------------------------------------------------
# 4. Modelo final con k = 3 (según método del codo)
kmeans = KMeans(n_clusters=3, random_state=12, n_init=20)

pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', kmeans)
])

# Entrenamiento
pipeline.fit(X)

# Asignar clusters
df_final['cluster'] = pipeline.predict(X)

#-------------------------------------------------------------------------------
# 5. Método del codo (descomentar si se quiere probar)

# inertia = []
# K = range(2, 10)

# for k in K:
#     model = Pipeline([
#         ('prep', preprocessor),
#         ('model', KMeans(n_clusters=k, random_state=42, n_init=20))
#     ])
#     model.fit(X)
#     inertia.append(model.named_steps['model'].inertia_)

# plt.plot(K, inertia, marker='o')
# plt.xlabel("Número de clusters")
# plt.ylabel("Inercia")
# plt.title("Método del Codo")
# plt.show()


# ----------------------------------------------------------------
# 6. Silhouette Score (muestra, no completo porque si no tarda mucho jajaj)

X_transformed = pipeline.named_steps['prep'].transform(X)
sample_idx = np.random.choice(X_transformed.shape[0], 20000, replace=False)
X_sample = X_transformed[sample_idx]
labels_sample = df_final['cluster'].iloc[sample_idx]
score = silhouette_score(X_sample, labels_sample)
print("\n Silhouette Score (muestra):", score)

#--------------------------------------------------------------------------------
# 7. Interpretación de clusters

print("\n=== EDADES PROMEDIO POR CLUSTER ===")
print(df_final.groupby('cluster')[['EDADHOM','EDADMUJ']].mean())

print("\n=== DISTRIBUCIÓN ESCOLARIDAD (HOMBRE) ===")
print(df_final.groupby('cluster')['ESCHOM'].value_counts(normalize=True))

print("\n=== DISTRIBUCIÓN POR DEPARTAMENTO ===")
print(df_final.groupby('cluster')['DEPREG'].value_counts(normalize=True))


#------------------------------------------------------------------------
# 8. Evolución temporal de clusters

tabla_clusters = (
    df_final
    .groupby(['AÑOOCU','cluster'])
    .size()
    .unstack()
)

tabla_prop = tabla_clusters.div(tabla_clusters.sum(axis=1), axis=0)

print("\n=== PROPORCIÓN DE CLUSTERS POR AÑO ===")
print(tabla_prop)

# Gráfica evolución temporal
tabla_prop.plot(kind='line', figsize=(10,6))
plt.title("Evolución de Clusters por Año")
plt.ylabel("Proporción")
plt.xlabel("Año")
plt.legend(title="Cluster")
plt.show()
