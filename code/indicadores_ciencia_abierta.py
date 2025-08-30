import pandas as pd
from ace_tools import display_dataframe_to_user

# Load data (already computed in analysis)
file_path = '/mnt/data/Set de datos producción científica Ciencias Sociales en Cuba (2020-2024).xlsx'
df = pd.read_excel(file_path, sheet_name=0)
total = len(df)

oa_counts = df['open_access.oa_status'].value_counts().to_dict()
closed_count = oa_counts.get('closed', 0)
open_count = total - closed_count
open_pct = round(open_count/total*100, 1)

fulltext_count = df['has_fulltext'].sum()
fulltext_pct = round(fulltext_count/total*100, 1)

license_notnull = df['best_oa_location.license'].notna() & (df['best_oa_location.license']!='')
license_count = license_notnull.sum()
license_pct = round(license_count/total*100, 1)

doaj_count = (df['primary_location.source.is_in_doaj']==True).sum()
doaj_pct = round(doaj_count/total*100, 1)

preprint_count = (df['type'].str.lower()=='preprint').sum()
preprint_pct = round(preprint_count/total*100, 1)

summary_rows = [
    ['Acceso Abierto (cualquier ruta)', open_count, open_pct],
    ['Cerrados', closed_count, round(closed_count/total*100,1)],
    ['Diamond OA', oa_counts.get('diamond',0), round(oa_counts.get('diamond',0)/total*100,1)],
    ['Gold OA', oa_counts.get('gold',0), round(oa_counts.get('gold',0)/total*100,1)],
    ['Green OA', oa_counts.get('green',0), round(oa_counts.get('green',0)/total*100,1)],
    ['Hybrid OA', oa_counts.get('hybrid',0), round(oa_counts.get('hybrid',0)/total*100,1)],
    ['Bronze OA', oa_counts.get('bronze',0), round(oa_counts.get('bronze',0)/total*100,1)],
    ['Texto completo disponible (PDF)', fulltext_count, fulltext_pct],
    ['Licencia explícita (Creative Commons u otra)', license_count, license_pct],
    ['Revistas listadas en DOAJ', doaj_count, doaj_pct],
    ['Preprints', preprint_count, preprint_pct],
]

summary_df = pd.DataFrame(summary_rows, columns=['Indicador', 'Artículos', '% del total'])
display_dataframe_to_user("Indicadores de Acceso Abierto (2020‑2024)", summary_df)


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

file_path = '/mnt/data/Set de datos producción científica Ciencias Sociales en Cuba (2020-2024).xlsx'
df = pd.read_excel(file_path, sheet_name=0)
total = len(df)

oa_counts = df['open_access.oa_status'].value_counts().to_dict()
closed_pct = round(oa_counts.get('closed',0)/total*100,1)
open_pct = round(100-closed_pct,1)

percents = {
    'Acceso Abierto': open_pct,
    'Diamond OA': round(oa_counts.get('diamond',0)/total*100,1),
    'Green OA': round(oa_counts.get('green',0)/total*100,1),
    'Hybrid OA': round(oa_counts.get('hybrid',0)/total*100,1),
    'Gold OA': round(oa_counts.get('gold',0)/total*100,1),
    'Bronze OA': round(oa_counts.get('bronze',0)/total*100,1),
    'Texto completo (PDF)': round(df['has_fulltext'].sum()/total*100,1),
    'Licencia explícita': round(((df['best_oa_location.license'].notna()) & (df['best_oa_location.license']!='')).sum()/total*100,1),
    'DOAJ': round((df['primary_location.source.is_in_doaj']==True).sum()/total*100,1),
    'Preprints': round((df['type'].str.lower()=='preprint').sum()/total*100,1),
    'Cerrados': closed_pct
}

labels = list(percents.keys())
values = list(percents.values())

colors = {
    'Acceso Abierto': '#1b7837',
    'Diamond OA': '#a6dba0',
    'Green OA': '#4daf4a',
    'Hybrid OA': '#2c7fb8',
    'Gold OA': '#e3c542',
    'Bronze OA': '#b07c3e',
    'Texto completo (PDF)': '#3182bd',
    'Licencia explícita': '#6baed6',
    'DOAJ': '#08519c',
    'Preprints': '#756bb1',
    'Cerrados': '#969696'
}
color_list = [colors[l] for l in labels]

N = len(labels)
angles = np.linspace(0, 2*np.pi, N, endpoint=False)

fig = plt.figure(figsize=(8,8))
ax = plt.subplot(111, polar=True)
bars = ax.bar(angles, values, width=2*np.pi/N, align='edge', edgecolor='white', color=color_list)

for angle, value, label in zip(angles, values, labels):
    rot = np.degrees(angle + (np.pi/N))
    align = 'left'
    if 90 < rot < 270:
        rot += 180
        align = 'right'
    ax.text(angle + (np.pi/N)/2, value + 2, f'{label}\n{value}%', ha=align, va='center',
            rotation=rot, rotation_mode='anchor', fontsize=8, fontweight='bold')

ax.set_ylim(0, max(values)+10)
ax.set_yticklabels([])
ax.set_xticklabels([])

plt.title('Indicadores de Ciencia Abierta en Ciencias Sociales (Cuba, 2020‑2024)\n(Colores por Tipología de Indicador)', pad=30, fontweight='bold')

output_path = Path('/mnt/data/figura_ciencia_abierta_radial_colores_negrita.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
