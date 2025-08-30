import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_excel('/mnt/data/cuba_social_sciences_2020_2024_enriched.xlsx', header=1)

df['Score'] = pd.to_numeric(df['Score'], errors='coerce').fillna(0)
df['oa_status'] = df['open_access.oa_status'].fillna('No OA')

coverage = (
    df.groupby('oa_status')
      .agg(Publicaciones=('id', 'count'),
           Con_atencion=('Score', lambda s: (s > 0).sum()))
      .reset_index()
)
coverage['Cobertura_%'] = coverage['Con_atencion'] / coverage['Publicaciones'] * 100

intensity = df[df['Score'] > 0].groupby('oa_status')['Score'].mean().reset_index(name='Media_Score')

merged = pd.merge(coverage, intensity, on='oa_status', how='left').fillna(0)

palette = {
    'gold': '#FFD700',
    'green': '#2E8B57',
    'bronze': '#CD7F32',
    'hybrid': '#6495ED',
    'diamond': '#8A2BE2',
    'closed': '#A9A9A9',
    'No OA': '#808080'
}
colors = [palette.get(s, '#333333') for s in merged['oa_status']]
sizes = merged['Con_atencion'] * 7  # scale factor

plt.figure(figsize=(7,5))
plt.scatter(merged['Cobertura_%'], merged['Media_Score'], s=sizes, c=colors, alpha=0.8, marker='o', edgecolors='black', linewidths=0.5)

for idx, row in merged.iterrows():
    plt.text(row['Cobertura_%']+0.15, row['Media_Score']+0.15, row['oa_status'], fontsize=8)

plt.xlabel('Cobertura altmétrica (% de artículos con AAS>0)')
plt.ylabel('Media de AAS (solo artículos con atención)')
plt.title('Cobertura vs Intensidad de atención por modalidad OA')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()

fig_path = '/mnt/data/oa_cobertura_intensidad_burbujas_colores_v2.png'
plt.savefig(fig_path, dpi=300)

fig_path
