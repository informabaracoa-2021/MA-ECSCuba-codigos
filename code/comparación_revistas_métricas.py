import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr

# Datos de la tabla proporcionada
data = {
    "Fuente": [
        "Maestro y sociedad", "Mendive. Revista de Educación", "Conrado",
        "Dilemas contemporáneos Educación Política y Valores", "Explorador Digital",
        "Revista Economía y Desarrollo", "Sinergia Académica",
        "Revista Estudios del Desarrollo Social: Cuba y América Latina", "LUZ",
        "COFINHABANA"
    ],
    "Publicaciones": [112, 105, 74, 64, 63, 63, 57, 52, 49, 48],
    "Citas acumuladas": [2, 1, 13, 42, 38, 1, 5, 10, 14, 0],
    "CCub": [2, 2, 1, 3, 3, 4, 3, 1, 2, 2],
    "Índice H": [1, 1, 2, 3, 3, 1, 1, 2, 2, 0]
}

df = pd.DataFrame(data)

# Crear gráficos de dispersión con regresión
fig1, ax1 = plt.subplots()
sns.regplot(data=df, x="CCub", y="Índice H", ax=ax1)
ax1.set_title("Regresión: CCub vs. Índice H")
ax1.set_xlabel("CCub (1=Mejor Clasificación)")
ax1.set_ylabel("Índice H")

fig2, ax2 = plt.subplots()
sns.regplot(data=df, x="CCub", y="Citas acumuladas", ax=ax2)
ax2.set_title("Regresión: CCub vs. Citas Acumuladas")
ax2.set_xlabel("CCub (1=Mejor Clasificación)")
ax2.set_ylabel("Citas Acumuladas")

# Calcular correlaciones
corr_h_spearman = spearmanr(df["CCub"], df["Índice H"])
corr_citas_spearman = spearmanr(df["CCub"], df["Citas acumuladas"])

fig1.tight_layout()
fig2.tight_layout()

(fig1, fig2), corr_h_spearman, corr_citas_spearman

from sklearn.preprocessing import StandardScaler

# Crear una copia del DataFrame original
df_comp = df.copy()

# Invertimos CCub para que 1 (mejor clasificación) se convierta en 4, etc.
df_comp["CCub_invertido"] = df_comp["CCub"].max() + 1 - df_comp["CCub"]

# Seleccionar columnas para normalización
features = ["Publicaciones", "Citas acumuladas", "Índice H", "CCub_invertido"]

# Normalizar las variables
scaler = StandardScaler()
df_comp_normalized = pd.DataFrame(scaler.fit_transform(df_comp[features]), columns=features)

# Calcular índice compuesto como promedio de las variables normalizadas
df_comp["Índice Compuesto"] = df_comp_normalized.mean(axis=1)

# Ordenar por el índice compuesto
df_comp_sorted = df_comp.sort_values("Índice Compuesto", ascending=False)

# Graficar
plt.figure(figsize=(12, 6))
sns.barplot(data=df_comp_sorted, x="Índice Compuesto", y="Fuente", palette="viridis")
plt.title("Ranking de Revistas según Índice Compuesto Multicriterio")
plt.xlabel("Índice Compuesto (Normalizado)")
plt.ylabel("Fuente")
plt.tight_layout()

import ace_tools as tools; tools.display_dataframe_to_user(name="Ranking de Revistas con Índice Compuesto", dataframe=df_comp_sorted[["Fuente", "Índice Compuesto"]])

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

# Usar las mismas variables normalizadas del paso anterior
X = df_comp_normalized.copy()

# Determinar número óptimo de clusters con el método del codo
inertia = []
K = range(1, 10)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

# Graficar el método del codo
plt.figure(figsize=(8, 4))
plt.plot(K, inertia, marker='o')
plt.title("Método del Codo para Determinar K Óptimo")
plt.xlabel("Número de Clusters (k)")
plt.ylabel("Inercia (Suma de distancias cuadradas)")
plt.tight_layout()
plt.show()

# Preparar datos para el heatmap
heatmap_data = df_comp.set_index("Fuente")[["Publicaciones", "Citas acumuladas", "Índice H", "CCub_invertido"]]

# Normalizar los valores entre 0 y 1 para mejor visualización
heatmap_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())

# Crear el heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_normalized, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Valor Normalizado'})
plt.title("Mapa de Calor: Comparación de Revistas según Métricas Bibliométricas")
plt.xlabel("Métricas")
plt.ylabel("Revistas")
plt.tight_layout()
plt.show()
