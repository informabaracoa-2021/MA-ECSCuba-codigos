import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Crear el DataFrame
data = {
    "Autor": [
        "Yunier Broche‐Pérez", "Katarzyna Pisanski", "Anna Oleszkiewicz", "Emanuel C. Mora",
        "Seda Can", "Seda Dural", "Zoi Manesi", "Georgina R. Lennard",
        "George Nizharadze", "Marina Butovskaya"
    ],
    "Citas": [512, 508, 508, 508, 500, 500, 500, 500, 500, 500],
    "Publicaciones": [15, 8, 8, 8, 7, 7, 7, 7, 7, 7],
    "Índice H": [5, 7, 7, 7, 6, 6, 6, 6, 6, 6],
}

df = pd.DataFrame(data)
df.set_index("Autor", inplace=True)

# Normalizar los valores para mejorar la escala del heatmap
df_norm = (df - df.min()) / (df.max() - df.min())

# Crear heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df_norm, annot=df, fmt=".0f", cmap="YlGnBu", linewidths=0.5, cbar_kws={'label': 'Desempeño relativo'})
plt.title("Heatmap de desempeño cienciométrico por autor")
plt.ylabel("Autor")
plt.xlabel("Métrica")
plt.tight_layout()
plt.show()


import re

# Lista para almacenar resultados
institution_citations_cleaned = []

# Iterar sobre las filas
for _, row in df.iterrows():
    citations = row.get("cited_by_count", 0)
    institutions_raw = row.get("authorships.institutions")

    if pd.isna(institutions_raw):
        continue

    # Buscar todos los valores de 'display_name'
    matches = re.findall(r"'display_name':\s*'([^']+)'", institutions_raw)
    for institution in matches:
        institution_citations_cleaned.append((institution.strip(), citations))

# Crear DataFrame
inst_df_cleaned = pd.DataFrame(institution_citations_cleaned, columns=["institution", "citations"])

# Agrupar y sumar
top_institutions_cleaned = inst_df_cleaned.groupby("institution", as_index=False).agg({"citations": "sum"})

# Top 10
top_10_institutions_cleaned = top_institutions_cleaned.sort_values(by="citations", ascending=False).head(10)

# Mostrar al usuario
import ace_tools as tools; tools.display_dataframe_to_user(name="Top 10 Instituciones Más Citadas", dataframe=top_10_institutions_cleaned)


