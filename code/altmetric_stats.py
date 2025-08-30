import glob, json, collections, pandas as pd

def campos_altmetricos(path_pattern='*.json'):
    union = collections.Counter()
    for fname in glob.glob(path_pattern):
        with open(fname) as f:
            data = json.load(f)
        if data.get('status') == 404:
            continue
        for k in data:
            if k.startswith('cited_by_') and k.endswith('_count'):
                union[k] += 1
    return pd.Series(union).sort_values(ascending=False)

print(campos_altmetricos('/ruta/a/tus/json/*.json'))
