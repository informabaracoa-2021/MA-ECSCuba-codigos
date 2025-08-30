import pandas as pd, requests, time, json, pathlib, argparse
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument("--lote", required=True, help="CSV con los DOI (ej. doi_lote1.csv)")
args = parser.parse_args()

API_KEY = "e1acaa96dca4a46a2721b47f7d99883e"          # ← reemplaza por tu clave de Altmetric
BASE = "https://api.altmetric.com/v1/doi/{}?key=" + API_KEY
PAUSA = 0.10                       # 0,1 s entre llamadas
LIMITE_ESPERA = 60                 # espera de 60 s si aparece rate-limit

# Carpeta donde guardaremos los JSON
out_dir = pathlib.Path("raw_altmetric")
out_dir.mkdir(exist_ok=True)

dois = pd.read_csv(args.lote, encoding="utf-8")["doi"]

for doi in dois:
    # 1) DOI “puro” sin https://doi.org/
    doi_clean = doi.lower().replace("https://doi.org/", "").strip()

    # 2) URL para la API (con DOI codificado)
    api_url = BASE.format(quote(doi_clean, safe=""))

    # 3) Nombre de archivo: sustituir / y : por _
    safe_name = doi_clean.replace("/", "_").replace(":", "_")
    fname = out_dir / f"{safe_name}.json"

    if fname.exists():
        continue

    try:
        r = requests.get(api_url, timeout=10)
        if r.status_code == 200:
            fname.write_bytes(r.content)          
        elif r.status_code == 404:
            fname.write_text('{"status":404}', encoding="utf-8")   
        elif r.status_code == 429:
            print("Rate limit alcanzado, esperando 60 s…")
            time.sleep(LIMITE_ESPERA)
            continue
        else:
            print(f"Error {r.status_code} en {doi_clean}")
    except requests.exceptions.RequestException as e:
        print(f"Excepción en {doi_clean}: {e}")
    time.sleep(PAUSA)
