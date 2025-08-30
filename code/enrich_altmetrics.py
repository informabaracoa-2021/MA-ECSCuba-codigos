import re, pandas as pd
from pathlib import Path

base = Path(r"C:\Users\FAMILIA\Desktop\Altmetrics")

# Cargar tablas
openalex = pd.read_excel(base / "Set de datos producción científica Ciencias Sociales en Cuba (2020-2024).xlsx")
alt      = pd.read_csv(base / "altmetrics_table.csv")

def core(doi: str) -> str:
    """
    Devuelve el DOI en su forma canónica (todo en minúsculas,
    sin prefijos http, doi:, etc.). Si no hay DOI, devuelve "".
    """
    if pd.isna(doi):
        return ""
    doi = doi.strip().lower()
    # Encuentra la subcadena que empieza en '10.' y llega hasta el final
    m = re.search(r"10\.\S+", doi)
    return m.group(0) if m else ""

# Crear columna clave en ambos DataFrame
openalex["doi_core"] = openalex["doi"].apply(core)
alt["doi_core"]      = alt["doi"].apply(core)

# Fusionar sobre la clave normalizada
df = openalex.merge(alt.drop(columns=["doi"]),  # evitamos duplicar columnas
                    on="doi_core", how="left")

# Opcional: borrar la columna auxiliar
df = df.drop(columns=["doi_core"])

df.to_excel(base / "cuba_social_sciences_2020_2024_enriched.xlsx", index=False)
print("Fusión completada; archivo enriquecido guardado.")
