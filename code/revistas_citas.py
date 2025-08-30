# Crear el DataFrame actualizado con la clasificación CCub corregida
data_actualizada = {
    "Fuente": [
        "Maestro y sociedad", "Mendive. Revista de Educación", "Conrado",
        "Dilemas contemporáneos", "Explorador Digital", "Revista Economía y Desarrollo",
        "Sinergia Académica", "Revista Estudios del Desarrollo Social", "LUZ", "COFINHABANA"
    ],
    "Publicaciones": [112, 105, 74, 64, 63, 63, 57, 52, 49, 48],
    "Citas": [2, 1, 13, 42, 38, 1, 5, 10, 14, 0],
    "Índice H": [1, 1, 2, 3, 3, 1, 1, 2, 2, 0],
    "CCub": [2, 2, 1, 3, 3, 4, 3, 1, 2, 2]
}

df_ccub = pd.DataFrame(data_actualizada)

# Asignar colores según CCub
colors = {1: 'red', 2: 'blue', 3: 'green', 4: 'orange'}
df_ccub["Color"] = df_ccub["CCub"].map(colors)

# Crear el scatter plot con las nuevas clasificaciones CCub
fig, ax = plt.subplots(figsize=(10, 7))

scatter = ax.scatter(
    df_ccub["Publicaciones"],
    df_ccub["Citas"],
    s=df_ccub["Índice H"] * 100 + 30,  # Tamaño proporcional al índice h
    c=df_ccub["Color"],
    alpha=0.75,
    edgecolors='k'
)

# Añadir etiquetas a los puntos
for i, row in df_ccub.iterrows():
    ax.text(row["Publicaciones"] + 0.5, row["Citas"] + 0.5, row["Fuente"], fontsize=9)

# Etiquetas y título
ax.set_xlabel("Cantidad de publicaciones")
ax.set_ylabel("Citas acumuladas")
ax.set_title("Dispersión: Publicaciones vs. Citas (Tamaño: Índice H, Color: CCub)")

# Crear leyenda de colores
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='CCub 1', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='CCub 2', markerfacecolor='blue', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='CCub 3', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='CCub 4', markerfacecolor='orange', markersize=10)
]
ax.legend(handles=legend_elements, title="Grupo CCub")

plt.grid(True)
plt.tight_layout()
plt.show()
