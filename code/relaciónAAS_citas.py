import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Cargar datos
df = pd.read_excel('/mnt/data/cuba_social_sciences_2020_2024_enriched.xlsx', header=1)

# Preparar variables
df['Score'] = pd.to_numeric(df['Score'], errors='coerce').fillna(0)
df['cited_by_count'] = pd.to_numeric(df['cited_by_count'], errors='coerce').fillna(0)

# Filtrar para scatter y regresión (Score > 0)
scatter_df = df[df['Score'] > 0][['cited_by_count', 'Score']]

# Ajustar modelo de regresión lineal simple para visualizar línea
X = scatter_df['cited_by_count'].values.reshape(-1, 1)
y = scatter_df['Score'].values
reg = LinearRegression().fit(X, y)
y_pred = reg.predict(X)

# Gráfico 1: scatter con línea de regresión
plt.figure(figsize=(6, 4))
plt.scatter(scatter_df['cited_by_count'], scatter_df['Score'])
plt.plot(scatter_df['cited_by_count'], y_pred)
plt.xlabel('Número de citas')
plt.ylabel('Altmetric Attention Score')
plt.title('Relación entre Score y citas')
plt.tight_layout()
plt.show()

# Gráfico 2: Boxplot Top25 vs Others
threshold = df['cited_by_count'].quantile(0.75)
df['grupo_citas'] = np.where(df['cited_by_count'] >= threshold, 'Top 25%', 'Otros')

data_to_plot = [df[df['grupo_citas'] == grp]['Score'] for grp in ['Otros', 'Top 25%']]

plt.figure(figsize=(6, 4))
plt.boxplot(data_to_plot, labels=['Otros', 'Top 25%'])
plt.ylabel('Altmetric Attention Score')
plt.title('Distribución de Score por grupo de citaciones')
plt.tight_layout()
plt.show()
