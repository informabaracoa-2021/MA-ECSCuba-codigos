import pandas as pd

# Cargar el archivo Excel
file_path = '/mnt/data/Set de datos producción científica Ciencias Sociales en Cuba (2020-2024).xlsx'
xls = pd.ExcelFile(file_path)

# Mostrar los nombres de las hojas para saber cuál analizar
sheet_names = xls.sheet_names
sheet_names

# Cargar la hoja con los datos
df = xls.parse('works-2025-03-17T18-58-22')

# Mostrar las primeras filas para examinar la estructura de los datos
df.head()

# Verificar si la columna con los nombres de autores está presente
columns = df.columns
columns[columns.str.contains("author.display_name", case=False, na=False)]

# Extraer solo las columnas necesarias
df_authors = df[['authorships.author.display_name', 'counts_by_year.cited_by_count']].copy()

# Expandir la lista de autores y sus citas (los nombres están separados por '|')
df_authors['authorships.author.display_name'] = df_authors['authorships.author.display_name'].astype(str)
df_authors['counts_by_year.cited_by_count'] = df_authors['counts_by_year.cited_by_count'].astype(str)

# Explode los autores
df_authors = df_authors.assign(
    author=df_authors['authorships.author.display_name'].str.split('|'),
    citations=df_authors['counts_by_year.cited_by_count'].str.split('|')
).explode('author')

# Convertir citas a enteros y sumar por autor
df_authors['citations'] = df_authors['citations'].fillna('0').astype(int)
top_authors = df_authors.groupby('author')['citations'].sum().sort_values(ascending=False).head(10)

# Mostrar resultados
top_authors = top_authors.reset_index()
import ace_tools as tools; tools.display_dataframe_to_user(name="Top 10 Autores Más Citados (2020-2024)", dataframe=top_authors)

# Usar la columna 'cited_by_count' y expandir autores
df_citations = df[['authorships.author.display_name', 'cited_by_count']].copy()

# Separar autores y replicar las citas por cada uno
df_citations['author'] = df_citations['authorships.author.display_name'].astype(str).str.split('|')
df_citations = df_citations.explode('author')

# Agrupar por autor y sumar las citas
top_authors_final = df_citations.groupby('author')['cited_by_count'].sum().sort_values(ascending=False).head(10).reset_index()

# Mostrar resultados
import ace_tools as tools; tools.display_dataframe_to_user(name="Top 10 Autores Más Citados (2020-2024)", dataframe=top_authors_final)

# Verificación detallada paso a paso

# 1. Confirmar que la columna 'cited_by_count' es numérica
df['cited_by_count'] = pd.to_numeric(df['cited_by_count'], errors='coerce')

# 2. Confirmar que la columna de autores contiene cadenas separadas por '|'
df['authorships.author.display_name'] = df['authorships.author.display_name'].astype(str)

# 3. Crear nuevo DataFrame para autores y sus citas
df_verified = df[['authorships.author.display_name', 'cited_by_count']].copy()
df_verified['author'] = df_verified['authorships.author.display_name'].str.split('|')
df_verified = df_verified.explode('author')

# 4. Agrupar por autor y sumar el total de citas
verified_top_authors = df_verified.groupby('author')['cited_by_count'].sum().sort_values(ascending=False).head(10).reset_index()

# Mostrar resultados verificados
import ace_tools as tools; tools.display_dataframe_to_user(name="Verificación: Top 10 Autores Más Citados", dataframe=verified_top_authors)

# Filtrar el conjunto original por los 10 autores más citados
top_10_authors = verified_top_authors['author'].tolist()

# Reutilizar el DataFrame de autores explotado
author_publication_counts = df_verified[df_verified['author'].isin(top_10_authors)]

# Contar publicaciones por autor (cada publicación puede estar duplicada si hay varios coautores del top 10)
publication_counts = author_publication_counts.groupby('author').size().reset_index(name='publication_count')

# Mostrar resultados
import ace_tools as tools; tools.display_dataframe_to_user(name="Cantidad de Publicaciones - Top 10 Autores Más Citados", dataframe=publication_counts)

# Crear función para calcular índice h
def calculate_h_index(citations):
    citations = sorted(citations, reverse=True)
    h_index = sum(c >= i + 1 for i, c in enumerate(citations))
    return h_index

# Obtener publicaciones únicas con autores y citas
df_h_index = df[['id', 'cited_by_count', 'authorships.author.display_name']].copy()
df_h_index['author'] = df_h_index['authorships.author.display_name'].astype(str).str.split('|')
df_h_index = df_h_index.explode('author')

# Filtrar solo por los top 10 autores más citados
df_h_index = df_h_index[df_h_index['author'].isin(top_10_authors)]

# Calcular índice h por autor
h_index_results = (
    df_h_index.groupby('author')['cited_by_count']
    .apply(lambda x: calculate_h_index(list(x)))
    .reset_index(name='h_index')
)

# Mostrar resultados
import ace_tools as tools; tools.display_dataframe_to_user(name="Índice H - Top 10 Autores Más Citados", dataframe=h_index_results)

# Extraer las columnas de autor y país
df_author_country = df[['authorships.author.display_name', 'authorships.author.country_code']].copy()

# Explode los autores y países
df_author_country['author'] = df_author_country['authorships.author.display_name'].astype(str).str.split('|')
df_author_country['country'] = df_author_country['authorships.author.country_code'].astype(str).str.split('|')

df_author_country = df_author_country.explode(['author', 'country'])

# Filtrar solo autores del top 10 más citados
df_author_country = df_author_country[df_author_country['author'].isin(top_10_authors)]

# Contar el país más frecuente por autor
author_country_info = df_author_country.groupby(['author', 'country']).size().reset_index(name='count')
author_country_final = author_country_info.sort_values('count', ascending=False).drop_duplicates('author').drop(columns='count')

# Mostrar los resultados
import ace_tools as tools; tools.display_dataframe_to_user(name="País de los Autores Más Citados", dataframe=author_country_final)

