from sklearn.linear_model import LinearRegression
import numpy as np

# Calcular regresión lineal entre Productividad y Citas
X = df_fuentes_actualizado["Productividad"].values.reshape(-1, 1)
y = df_fuentes_actualizado["Citas"].values
modelo = LinearRegression().fit(X, y)
beta_0 = modelo.intercept_
beta_1 = modelo.coef_[0]

# Crear la ecuación como texto para mostrarla en la gráfica
ecuacion_texto = f"ŷ = {beta_0:.2f} + {beta_1:.2f}x"

# Rehacer el gráfico e incluir la fórmula visualmente
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_fuentes_actualizado,
    x="Productividad",
    y="Citas",
    hue="Cuartil-SJR",
    size="Índice H",
    sizes=(50, 300),
    palette={"Q1": "green", "Q2": "gold", "Q0": "black"},
    edgecolor="gray",
    alpha=0.8,
    marker="D",
    legend=False
)

# Línea de regresión
sns.regplot(
    data=df_fuentes_actualizado,
    x="Productividad",
    y="Citas",
    scatter=False,
    color="gray",
    line_kws={"linestyle": "dashed"}
)

# Etiquetas sin una fuente específica
for i, row in df_fuentes_actualizado.iterrows():
    if row["Fuente"] != "International Journal of Mental Health and Addiction":
        plt.text(row["Productividad"] + 0.3, row["Citas"], row["Fuente"], fontsize=8)

# Añadir leyenda personalizada
plt.legend(
    handles=full_legend,
    title="Cuartil SJR / Índice H",
    loc='upper left',
    bbox_to_anchor=(1.05, 1),
    borderaxespad=0.
)

# Mostrar la fórmula de la regresión
plt.text(0.5, max(y) * 0.95, ecuacion_texto, fontsize=12, color="gray")

# Estética
plt.title("Relación entre Productividad y Citas con Ecuación de la Regresión Lineal", fontsize=14)
plt.xlabel("Productividad (Número de Publicaciones)", fontsize=12)
plt.ylabel("Citas Acumuladas", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
