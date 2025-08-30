import matplotlib.pyplot as plt
import seaborn as sns

# Crear gráfico de barras apiladas
plt.figure(figsize=(12, 7))
sns.set(style="whitegrid")
sns.barplot(data=pub_counts, x='publication_year', y='count', hue='type')

plt.title('Producción científica por tipo de publicación y año (Cuba, 2020–2024)', fontsize=14)
plt.xlabel('Año de publicación')
plt.ylabel('Número de publicaciones')
plt.legend(title='Tipo de publicación', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Guardar como imagen
output_graph_path = "/mnt/data/Publicaciones_por_tipo_y_año_Cuba_SS.png"
plt.savefig(output_graph_path, dpi=300)
plt.close()

output_graph_path

# Reintentar la generación de la figura después del error
fig = plt.figure(figsize=(12, 9))
gs = fig.add_gridspec(2, 1, height_ratios=[2.5, 1.2], hspace=0.4)

# Gráfico superior
ax0 = fig.add_subplot(gs[0])
stacked_df.plot(kind='bar', stacked=True, ax=ax0, color=[color_map[t] for t in stacked_df.columns])
ax0.set_title('Composición porcentual de tipos de publicación por año', fontsize=14)
ax0.set_xlabel('')
ax0.set_ylabel('Proporción (%)')
ax0.legend().remove()
ax0.set_xticklabels(ax0.get_xticklabels(), rotation=0)

# Tabla inferior
ax1 = fig.add_subplot(gs[1])
ax1.axis('off')

# Ajuste de celdas y fuentes
cell_height = 1.0 / (n_rows + 1.5)
col_width = 0.07
col_start = 0.18
tipo_col_width = 0.15
small_fontsize = 8

# Encabezados
for j, col in enumerate(table_data.columns):
    x_pos = col_start + j * col_width
    ax1.text(x_pos, 1, str(col), ha='center', va='center', fontsize=10, weight='bold')

# Filas
for i, tipo in enumerate(table_data.index):
    y_pos = 1 - (i + 1.2) * cell_height
    ax1.add_patch(plt.Rectangle((0, y_pos - cell_height/2), tipo_col_width, cell_height,
                                fill=True, color=color_map[tipo], alpha=0.3))
    ax1.text(0.01, y_pos, tipo, ha='left', va='center', fontsize=10, color=color_map[tipo], weight='bold')
    for j, col in enumerate(table_data.columns):
        value = table_data.loc[tipo, col]
        x_pos = col_start + j * col_width
        ax1.add_patch(plt.Rectangle((x_pos - col_width/2, y_pos - cell_height/2),
                                    col_width, cell_height, fill=True, color='white', ec='gray', lw=0.5))
        ax1.text(x_pos, y_pos, str(value), ha='center', va='center', fontsize=small_fontsize)

# Guardar imagen final
final_output_small_font = "/mnt/data/Figura_Publicaciones_Cuba_SS_con_tabla_y_total_espaciado_y_fuente_pequena.png"
plt.savefig(final_output_small_font, dpi=300, bbox_inches='tight')
plt.close()

final_output_small_font
