import ast
import re
from collections import defaultdict

# Inicializar diccionario para acumular citas por institución
institution_citations = defaultdict(float)

# Iterar sobre cada fila del DataFrame
for _, row in df.iterrows():
    raw_institutions = row.get("authorships.institutions", "")
    cited_by_count = row.get("cited_by_count", 0)
    
    # Extraer nombres de instituciones con regex
    matches = re.findall(r"'display_name':\s?'([^']+)'", str(raw_institutions))
    if matches:
        share = cited_by_count / len(matches)  # dividir las citas entre instituciones participantes
        for inst in matches:
            institution_citations[inst.strip()] += share

# Convertir a DataFrame
institutions_df = pd.DataFrame(institution_citations.items(), columns=["institution", "total_citations"])

# Ordenar por número de citas y tomar top 10
top10_institutions = institutions_df.sort_values(by="total_citations", ascending=False).head(10)

import seaborn as sns
import matplotlib.pyplot as plt

# Visualización
plt.figure(figsize=(10, 6))
sns.barplot(data=top10_institutions, y="institution", x="total_citations", palette="viridis")
plt.title("Top 10 Instituciones más Citadas (Cuba, Ciencias Sociales, 2020–2024)")
plt.xlabel("Total de Citas")
plt.ylabel("Institución")
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.show()


