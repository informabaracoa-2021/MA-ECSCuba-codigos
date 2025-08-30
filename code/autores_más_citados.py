from docx import Document
import pandas as pd

# Cargar el archivo Word
doc_path = '/mnt/data/Autores más citados.docx'
doc = Document(doc_path)

# Extraer la tabla del documento
table = doc.tables[0]

# Extraer datos fila por fila
data = []
for row in table.rows[1:]:  # omitir encabezado
    cells = row.cells
    data.append([cell.text.strip() for cell in cells])

# Crear DataFrame
columns = ["Autor", "Citas acumuladas", "Publicaciones", "Índice H", "País"]
df_autores = pd.DataFrame(data, columns=columns)

# Convertir columnas numéricas
df_autores["Citas acumuladas"] = pd.to_numeric(df_autores["Citas acumuladas"])
df_autores["Publicaciones"] = pd.to_numeric(df_autores["Publicaciones"])
df_autores["Índice H"] = pd.to_numeric(df_autores["Índice H"])

df_autores

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Datos de ejemplo
data = {
    'Autor': [
        'Yunier Broche-Pérez', 'Katarzyna Pisanski', 'Anna Oleszkiewicz',
        'Emanuel C. Mora', 'Seda Can', 'Seda Dural', 'Zoi Manesi',
        'George Nizharadze', 'Georgina R. Lennard', 'Marina Butovskaya'
    ],
    'Citas Acumuladas': [500, 450, 400, 350, 300, 280, 260, 240, 220, 200],
    'Publicaciones': [50, 45, 40, 35, 30, 28, 26, 24, 22, 20],
    'Índice H': [15, 14, 13, 12, 11, 10, 9, 8, 7, 6],
    'País': [
        'Cuba', 'Francia', 'Polonia', 'Estados Unidos', 'Turquía',
        'Turquía', 'Países Bajos', 'Georgia', 'Australia', 'Rusia'
    ],
    'Bandera': [
        'cuba.png', 'francia.png', 'polonia.png', 'estados_unidos.png',
        'turquia.png', 'turquia.png', 'paises_bajos.png', 'georgia.png',
        'australia.png', 'rusia.png'
    ]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Configuración del gráfico
fig, ax = plt.subplots(figsize=(12, 8))

# Posiciones para las barras
bar_width = 0.25
r1 = range(len(df))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Crear las barras
ax.bar(r1, df['Citas Acumuladas'], color='b', width=bar_width, edgecolor='grey', label='Citas Acumuladas')
ax.bar(r2, df['Publicaciones'], color='g', width=bar_width, edgecolor='grey', label='Publicaciones')
ax.bar(r3, df['Índice H'], color='r', width=bar_width, edgecolor='grey', label='Índice H')

# Añadir banderas encima de los nombres de los autores
for i, (autor, bandera) in enumerate(zip(df['Autor'], df['Bandera'])):
    img = mpimg.imread(bandera)
    imagebox = OffsetImage(img, zoom=0.1)
    ab = AnnotationBbox(imagebox, (i + bar_width, 0), frameon=False, xybox=(0, -20), boxcoords="offset points", pad=0)
    ax.add_artist(ab)

# Configuración de ejes y etiquetas
ax.set_xlabel('Autores', fontweight='bold')
ax.set_ylabel('Valores', fontweight='bold')
ax.set_title('Métricas de Autores Más Citados con Banderas de sus Países')
ax.set_xticks([r + bar_width for r in range(len(df))])
ax.set_xticklabels(df['Autor'], rotation=45, ha='right')

# Añadir leyenda
ax.legend()

# Mostrar el gráfico
plt.tight_layout()
plt.show()

