import json, pandas as pd, pathlib

filas = []
for path in pathlib.Path("raw_altmetric").glob("*.json"):
    data = json.loads(path.read_bytes())

    # Saltar DOIs sin cobertura
    if data.get("status") == 404:
        continue

    filas.append({
        "doi":      data.get("doi", "").lower(),
        "score":    data.get("score", 0),
        "twitter":  data.get("cited_by_tweeters_count", 0),
        "news":     data.get("cited_by_msm_count", 0),
        "blogs":    data.get("cited_by_feeds_count", 0),
        "wikipedia":data.get("cited_by_wikipedia_count", 0),
        "policy":   data.get("cited_by_policy_documents_count", 0),
        "mendeley": data.get("readers", {}).get("mendeley", 0)
    })

pd.DataFrame(filas).to_csv("altmetrics_table.csv", index=False, encoding="utf-8")
print("Tabla altmetrics_table.csv regenerada con", len(filas), "registros")
