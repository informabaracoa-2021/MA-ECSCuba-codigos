fig_bubble_clean, ax3 = plt.subplots(figsize=(10, 6))

# Usar marcador 'o' para bolas
scatter_clean = ax3.scatter(
    df["Publicaciones"],
    df["Citas"],
    s=[h * 10 for h in df["h"]],
    c=df["i10"],
    cmap="viridis",
    alpha=0.75,
    edgecolors="black",
    linewidth=0.5,
    marker='o'  # marcador circular
)

# Añadir etiquetas con nombres de instituciones
for i, row in df.iterrows():
    ax3.text(row["Publicaciones"], row["Citas"], row["Institución"], fontsize=8, ha='center', va='center')

# Etiquetas y título
ax3.set_xlabel("Número de publicaciones")
ax3.set_ylabel("Citas acumuladas")
ax3.set_title("Producción vs Citas (Tamaño: índice h, Color: índice i10)")

# Barra de color para i10
cbar = plt.colorbar(scatter_clean, ax=ax3)
cbar.set_label("Índice i10")

plt.tight_layout()
plt.show()
