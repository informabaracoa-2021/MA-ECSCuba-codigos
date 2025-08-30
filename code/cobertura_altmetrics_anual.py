import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the enriched dataset provided by the user
file_path = Path('/mnt/data/cuba_social_sciences_2020_2024_enriched.xlsx')
df = pd.read_excel(file_path)

# Fix the mis‑read header row
header = df.iloc[0]
df = df[1:].copy()
df.columns = header

# Keep only the columns we need
metrics = {
    "Score": "Altmetric Attention Score",
    " X users": "Usuarios en X",
    "Mendeley ": "Lectores en Mendeley",
    "News outlets": "Noticias",
    "Blogs": "Blogs",
    "Wikipedia pages": "Wikipedia",
    "Policy sources": "Documentos de política",
    "Patent": "Patentes",
    "Facebook page": "Páginas de Facebook",
    "Bluesky user": "Usuarios de Bluesky",
    "Redditors": "Reddit",
    "YouTube creator": "YouTube",
    "Peer review site": "Sitios de peer review",
    "Clinical guideline source": "Guías clínicas"
}

# Years of interest
years = list(range(2020, 2025))

# Prepare coverage data (percentage of publications with ≥1 mención)
coverage = {pretty: [] for pretty in metrics.values()}
for year in years:
    year_df = df[df["publication_year"] == year]
    total_year = len(year_df)
    for raw_col, pretty in metrics.items():
        if raw_col not in year_df.columns:
            coverage[pretty].append(0.0)
        else:
            counts = pd.to_numeric(year_df[raw_col], errors="coerce").fillna(0)
            covered = (counts > 0).sum()
            coverage[pretty].append(covered / total_year * 100 if total_year else 0)

# Plot
plt.figure(figsize=(12, 7))
for pretty, values in coverage.items():
    plt.plot(years, values, marker="o", label=pretty)

plt.xlabel("Año de publicación")
plt.ylabel("Cobertura altmétrica (%)")
plt.title("Cobertura altmétrica anual para publicaciones cubanas en Ciencias Sociales (2020‑2024)")
plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize="small")
plt.tight_layout()

output_path = Path('/mnt/data/cobertura_altmetrica_anual.png')
plt.savefig(output_path, dpi=300)
output_path
