import matplotlib.pyplot as plt

# Crear el DataFrame con los datos institucionales
instituciones_data = {
    "Institución": [
        "Universidad de La Habana", "Universidad Central de Las Villas", "Universidad de Camagüey",
        "Universidad de Holguín", "Universidad de Pinar del Río", "Universidad de Oriente",
        "Universidad de Cienfuegos", "Universidad de Granma", "Universidad de Matanzas",
        "Universidad de Ciego de Ávila"
    ],
    "Publicaciones": [1748, 1048, 715, 659, 650, 460, 445, 306, 298, 285],
    "Citas": [2031, 566, 133, 329, 192, 237, 194, 271, 283, 346],
    "Índice H": [19, 13, 5, 8, 6, 7, 6, 10, 7, 12]
}

df_inst = pd.DataFrame(instituciones_data)

# Crear el gráfico de dispersión
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    df_inst["Publicaciones"],
    df_inst["Citas"],
    s=df_inst["Índice H"] * 20,  # Tamaño proporcional al índice H
    alpha=0.7
)

# Agregar etiquetas de texto a cada punto
for i in range(df_inst.shape[0]):
    plt.text(df_inst["Publicaciones"][i]+10, df_inst["Citas"][i], df_inst["Institución"][i], fontsize=9)

plt.xlabel("Número de publicaciones")
plt.ylabel("Citas acumuladas")
plt.title("Relación entre número de publicaciones, citas e índice H por institución")
plt.grid(True)
plt.tight_layout()
plt.show()


# Rehacer el gráfico incluyendo etiquetas con nombres de instituciones

plt.figure(figsize=(12, 7))
scatter = plt.scatter(
    df_inst["Publicaciones"],
    df_inst["Citas"],
    s=df_inst["Índice H"] * 20,
    c=df_inst["Índice H"],
    cmap=cmap,
    alpha=0.8,
    edgecolors="k",
    marker='o'
)

# Añadir nombres de las instituciones junto a cada punto
for i in range(df_inst.shape[0]):
    plt.text(
        df_inst["Publicaciones"][i] + 10,
        df_inst["Citas"][i],
        df_inst["Institución"][i],
        fontsize=9
    )

# Barra de color
cbar = plt.colorbar(scatter)
cbar.set_label("Índice H")

# Etiquetas
plt.xlabel("Número de publicaciones")
plt.ylabel("Citas acumuladas")
plt.title("Relación entre número de publicaciones, citas e índice H por institución")

plt.grid(True)
plt.tight_layout()
plt.show()
