import pandas as pd, re, collections, matplotlib.pyplot as plt

# Load dataset
file_path = '/mnt/data/cuba_social_sciences_2020_2024_enriched.xlsx'
df = pd.read_excel(file_path, header=1)

# Identify demographic breakdown for Mendeley professional status
mend_demo_col = 'Demographic breakdown.1'

prof_status_counter = collections.Counter()

for cell in df[mend_demo_col].dropna():
    sections = str(cell).split('Readers by')
    for sec in sections:
        if 'professional status' in sec:
            for entry in sec.split('\n'):
                m = re.match(r'([^\t]+)\t(\d+)', entry.strip())
                if m and m.group(1).lower() not in ['professional status', 'type', 'count', 'as %']:
                    label = m.group(1).strip()
                    count = int(m.group(2))
                    prof_status_counter[label] += count

prof_df = pd.DataFrame(prof_status_counter.items(), columns=['Estatus profesional', 'Lectores']).sort_values(by='Lectores', ascending=False)

# Create horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(prof_df['Estatus profesional'][::-1], prof_df['Lectores'][::-1], color='green')
ax.set_xlabel('Lectores únicos')
ax.set_title('Lectores de Mendeley por estatus profesional (2020‑2024)')
# Add labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + max(prof_df['Lectores']) * 0.01, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center')
plt.tight_layout()
plt.show()
