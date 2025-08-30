import pandas as pd

csv = "dois_cuba_social_sciences_2020_2024.csv"
dois = pd.read_csv(csv)

lotes = [dois.iloc[:1500], dois.iloc[1500:3000], dois.iloc[3000:]]

for i, lote in enumerate(lotes, start=1):
    fname = f"doi_lote{i}.csv"
    lote.to_csv(fname, index=False)
    print(f"Lote {i} guardado: {len(lote)} DOI")
