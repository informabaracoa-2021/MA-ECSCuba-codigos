import pandas as pd, re, collections, matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import ace_tools as tools

# Load dataset
file_path = '/mnt/data/cuba_social_sciences_2020_2024_enriched.xlsx'
df = pd.read_excel(file_path, header=1)

# Identify demographic breakdown columns
demo_cols = [c for c in df.columns if 'Demographic breakdown' in str(c)]
# Identify OA column – try common possibilities
oa_col_candidates = [c for c in df.columns if 'oa' in str(c).lower() or 'access' in str(c).lower()]
# Pick first plausible OA column
oa_col = None
for c in oa_col_candidates:
    if df[c].dtype == object or df[c].dtype == bool:
        oa_col = c
        break
if oa_col is None:
    raise ValueError("No OA column found")

# Mapping to macro categories
def map_macro(label):
    lbl = label.lower()
    if 'public' in lbl:
        return 'Público'
    if any(k in lbl for k in ['research', 'student', 'lectur', 'professor', 'academic', 'scholar', 'phd', 'msc', 'bsc']):
        return 'Académicos'
    if any(k in lbl for k in ['practitioner', 'health', 'medicine', 'nursing']):
        return 'Profesionales'
    if 'communicator' in lbl or 'journalist' in lbl or 'blogger' in lbl or 'editor' in lbl:
        return 'Comunicadores'
    if 'unknown' in lbl or 'unspecified' in lbl:
        return 'Unknown'
    return 'Otros'

# Aggregate global demographic counts
demo_counts = collections.Counter()

# Aggregate OA x audience
oa_audience = collections.defaultdict(lambda: collections.Counter())

for idx, row in df.iterrows():
    oa_status = str(row[oa_col]).strip() if pd.notnull(row[oa_col]) else 'Unknown'
    for col in demo_cols:
        cell = row[col]
        if pd.isnull(cell):
            continue
        for entry in str(cell).split('\n'):
            m = re.match(r'([^\t]+)\t(\d+)', entry.strip())
            if m:
                label = m.group(1).strip()
                count = int(m.group(2))
                macro = map_macro(label)
                demo_counts[macro] += count
                oa_audience[oa_status][macro] += count

# Prepare global donut data
labels = list(demo_counts.keys())
sizes = [demo_counts[k] for k in labels]

# Plot donut
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts = ax.pie(sizes, labels=labels, wedgeprops=dict(width=0.4, edgecolor='w'))
ax.set_title('Distribución global de audiencias en X para la investigación social cubana (2020‑2024)')
plt.tight_layout()
plt.show()

# Display global counts
global_df = pd.DataFrame({'Macro-categoría': labels, 'Cuentas únicas': sizes})
tools.display_dataframe_to_user(name="Conteo global de audiencias", dataframe=global_df)

# Build OA x Audience contingency table
oa_categories = list(oa_audience.keys())
macro_categories = list(demo_counts.keys())

cont_table = pd.DataFrame(index=macro_categories, columns=oa_categories).fillna(0)
for oa, counter in oa_audience.items():
    for macro, cnt in counter.items():
        cont_table.loc[macro, oa] = cnt

# Chi-square test
chi2, p, dof, expected = chi2_contingency(cont_table)

# Display contingency and chi-squared results
tools.display_dataframe_to_user(name="Tabla de contingencia OA × Audiencia", dataframe=cont_table)

chi_results = pd.DataFrame({'Estadístico chi²': [chi2], 'p‑valor': [p], 'Grados de libertad': [dof]})
tools.display_dataframe_to_user(name="Resultado prueba chi²", dataframe=chi_results)
