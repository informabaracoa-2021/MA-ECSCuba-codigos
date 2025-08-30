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

