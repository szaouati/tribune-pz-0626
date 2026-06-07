"""
Connecteurs de données — accès programmatique aux sources primaires.

Sources couvertes :
  - Banque mondiale (World Development Indicators) — API REST v2
  - Our World in Data (OWID) — export CSV des "graphers"
  - FMI (IMF DataMapper / WEO) — API v1
  - OCDE — SDMX-JSON REST
  - Eurostat — API dissemination (JSON-stat 2.0)

Chaque appel est mis en cache dans data/raw/ pour la reproductibilité et
journalise (source, URL, date d'extraction) dans un registre central.
"""
from __future__ import annotations
import json, time, io, csv
import requests
import pandas as pd
from pathlib import Path
import config as C

RAW = C.RAW
RAW.mkdir(parents=True, exist_ok=True)
_REGISTRE = RAW / "_registre_sources.csv"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "tribune-pz-0626 data collection (research)"})


def _journaliser(serie: str, source: str, url: str, n: int):
    nouveau = not _REGISTRE.exists()
    with open(_REGISTRE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nouveau:
            w.writerow(["serie", "source", "url", "date_extraction", "n_observations"])
        w.writerow([serie, source, url, C.DATE_EXTRACTION, n])


def _get(url: str, params=None, tries=4, timeout=40):
    last = None
    for i in range(tries):
        try:
            r = SESSION.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = str(e)
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"Échec requête {url} : {last}")


# ---------------------------------------------------------------------------
# Banque mondiale
# ---------------------------------------------------------------------------
def wb(indicator: str, countries, start: int, end: int,
       serie: str = "", libelle: str = "") -> pd.DataFrame:
    """Indicateur WDI pour une liste de pays (ISO3). -> DataFrame long."""
    if isinstance(countries, str):
        countries = [countries]
    codes = ";".join(countries)
    url = f"https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}"
    params = {"format": "json", "date": f"{start}:{end}", "per_page": 20000}
    r = _get(url, params=params)
    payload = r.json()
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise RuntimeError(f"WB: pas de données pour {indicator} / {codes}")
    rows = []
    for d in payload[1]:
        if d["value"] is None:
            continue
        rows.append({
            "iso3": d["countryiso3code"],
            "pays": d["country"]["value"],
            "annee": int(d["date"]),
            "valeur": float(d["value"]),
            "indicateur": indicator,
            "libelle": libelle or d["indicator"]["value"],
        })
    df = pd.DataFrame(rows).sort_values(["iso3", "annee"]).reset_index(drop=True)
    _journaliser(serie or indicator, "Banque mondiale (WDI)",
                 r.url.split("&per_page")[0], len(df))
    return df


# ---------------------------------------------------------------------------
# Our World in Data
# ---------------------------------------------------------------------------
def owid(slug: str, serie: str = "") -> pd.DataFrame:
    """Télécharge le CSV complet d'un grapher OWID. -> DataFrame."""
    url = (f"https://ourworldindata.org/grapher/{slug}.csv"
           f"?v=1&csvType=full&useColumnShortNames=true")
    cache = RAW / f"owid_{slug}.csv"
    r = _get(url)
    cache.write_bytes(r.content)
    df = pd.read_csv(io.BytesIO(r.content))
    # Normalisation colonnes communes
    df = df.rename(columns={"Entity": "entity", "Code": "code", "Year": "year"})
    _journaliser(serie or slug, "Our World in Data", url, len(df))
    return df


# ---------------------------------------------------------------------------
# FMI — DataMapper (séries WEO)
# ---------------------------------------------------------------------------
def imf(indicator: str, countries, serie: str = "") -> pd.DataFrame:
    """Série FMI DataMapper. countries: liste ISO3 ou groupes (ex 'EU','WEOWORLD')."""
    import subprocess, json as _json
    if isinstance(countries, str):
        countries = [countries]
    keep = set(countries)
    # L'API FMI (Akamai) bloque l'empreinte TLS de `requests` -> on passe par curl.
    url = f"https://www.imf.org/external/datamapper/api/v1/{indicator}"
    out = subprocess.run(["curl", "-s", "--max-time", "40", url],
                         capture_output=True, text=True)
    if out.returncode != 0 or not out.stdout:
        raise RuntimeError(f"Échec requête FMI {url} : curl rc={out.returncode}")
    payload = _json.loads(out.stdout)
    vals = payload.get("values", {}).get(indicator, {})
    rows = []
    for ent, serie_an in vals.items():
        if ent not in keep:
            continue
        for an, v in serie_an.items():
            if v is None:
                continue
            rows.append({"entity": ent, "annee": int(an), "valeur": float(v),
                         "indicateur": indicator})
    df = pd.DataFrame(rows).sort_values(["entity", "annee"]).reset_index(drop=True)
    _journaliser(serie or indicator, "FMI (World Economic Outlook / DataMapper)", url, len(df))
    return df


# ---------------------------------------------------------------------------
# OCDE — SDMX-JSON
# ---------------------------------------------------------------------------
def oecd_sdmx(dataflow: str, key: str, params: dict = None, serie: str = "") -> dict:
    """
    Récupère un dataset OCDE en SDMX-JSON.
    dataflow ex: 'OECD.ELS.SAE,DSD_HOURS_WORKED@DF_AVG_ANN_HRS_WKD,1.0'
    key ex: 'FRA+DEU.....'
    Renvoie le JSON brut (à parser selon la structure).
    """
    base = "https://sdmx.oecd.org/public/rest/data"
    url = f"{base}/{dataflow}/{key}"
    p = {"dimensionAtObservation": "AllDimensions"}
    if params:
        p.update(params)
    headers = {"Accept": "application/vnd.sdmx.data+json; charset=utf-8; version=1.0"}
    r = SESSION.get(url, params=p, headers=headers, timeout=60)
    r.raise_for_status()
    cache = RAW / f"oecd_{serie or 'data'}.json"
    cache.write_bytes(r.content)
    _journaliser(serie or dataflow, "OCDE (SDMX)", r.url, 0)
    return r.json()


def parse_sdmx_json(payload: dict) -> pd.DataFrame:
    """Aplatit un SDMX-JSON (dimensionAtObservation=AllDimensions) en DataFrame."""
    data = payload["data"]
    structure = data.get("structures", data.get("structure"))
    if isinstance(structure, list):
        structure = structure[0]
    dims = structure["dimensions"]["observation"]
    obs = data["dataSets"][0]["observations"]
    rows = []
    for key, val in obs.items():
        idx = [int(i) for i in key.split(":")]
        rec = {}
        for d, i in zip(dims, idx):
            rec[d["id"]] = d["values"][i]["id"]
            rec[d["id"] + "_label"] = d["values"][i].get("name")
        rec["valeur"] = val[0]
        rows.append(rec)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Eurostat — API dissemination (JSON-stat 2.0)
# ---------------------------------------------------------------------------
_EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"


def parse_jsonstat(j: dict) -> pd.DataFrame:
    """Aplatit une réponse JSON-stat 2.0 d'Eurostat en DataFrame long.

    L'index plat des observations (`value`) se décompose en row-major (ordre C)
    sur les tailles `size` des dimensions `id`. Pour chaque dimension on ajoute
    la colonne `<dim>` (code) et `<dim>_label` (libellé).
    """
    dims, sizes = j["id"], j["size"]
    cats = []
    for d in dims:
        c = j["dimension"][d]["category"]
        inv = {pos: code for code, pos in c["index"].items()}
        labels = c.get("label", {})
        cats.append([(inv[i], labels.get(inv[i], inv[i])) for i in range(len(inv))])
    rows = []
    for flat, val in j["value"].items():
        n = int(flat); coords = []
        for s in reversed(sizes):
            coords.append(n % s); n //= s
        coords = coords[::-1]
        rec = {}
        for di, d in enumerate(dims):
            code, lab = cats[di][coords[di]]
            rec[d] = code
            rec[d + "_label"] = lab
        rec["valeur"] = val
        rows.append(rec)
    return pd.DataFrame(rows)


def eurostat(dataset: str, serie: str = "", **filters) -> pd.DataFrame:
    """Récupère un dataset Eurostat via l'API dissemination (JSON-stat).

    Les filtres sont passés en kwargs : valeur unique (`unit="PC_GDP"`) ou liste
    (`geo=["FR", "DE", "NL"]`, encodée en clés répétées que l'API accepte).
    -> DataFrame long (une ligne par observation), cf. parse_jsonstat().
    """
    params = {"format": "JSON"}
    params.update({k: v for k, v in filters.items() if v is not None})
    r = _get(_EUROSTAT_BASE + dataset, params=params, timeout=90)
    payload = r.json()
    (RAW / f"eurostat_{serie or dataset}.json").write_bytes(r.content)
    df = parse_jsonstat(payload)
    _journaliser(serie or dataset, "Eurostat", r.url.split("&format")[0], len(df))
    return df


# ---------------------------------------------------------------------------
# OpenDataSoft — Explore API v2.1 (portails OFGL, data.economie.gouv.fr…)
# ---------------------------------------------------------------------------
def opendatasoft(portail: str, dataset: str, serie: str = "",
                 where: str = "", select: str = "", group_by: str = "",
                 order_by: str = "", page: int = 100, max_rows: int = 100000) -> pd.DataFrame:
    """Récupère des enregistrements d'un portail OpenDataSoft (Explore API v2.1).

    portail ex: 'data.ofgl.fr' ; dataset ex: 'ofgl-base-communes'.
    Pagination automatique par `offset` (limite 100/req côté ODS). -> DataFrame.
    """
    base = f"https://{portail}/api/explore/v2.1/catalog/datasets/{dataset}/records"
    rows, offset = [], 0
    last_url = base
    while offset < max_rows:
        params = {"limit": page, "offset": offset}
        for k, v in (("where", where), ("select", select),
                     ("group_by", group_by), ("order_by", order_by)):
            if v:
                params[k] = v
        r = _get(base, params=params)
        last_url = r.url
        results = r.json().get("results", [])
        rows.extend(results)
        if len(results) < page:
            break
        offset += page
    df = pd.DataFrame(rows)
    _journaliser(serie or dataset, f"OpenDataSoft ({portail})", last_url, len(df))
    return df


# ---------------------------------------------------------------------------
# INSEE — API Mélodi (données SDMX, ex. Base Permanente des Équipements)
# ---------------------------------------------------------------------------
def insee_melodi(dataset: str, serie: str = "", max_result: int = 20000, **filters) -> pd.DataFrame:
    """Récupère un jeu de l'API Mélodi de l'INSEE. -> DataFrame (1 ligne/observation).

    dataset ex: 'DS_BPE'. filters ex: FACILITY_TYPE='C107', BPE_MEASURE='FACILITIES', GEO='DEP'.
    Aplatit les dimensions + la mesure OBS_VALUE_NIVEAU en colonnes.
    """
    url = f"https://api.insee.fr/melodi/V2/data/{dataset}"
    params = {"maxResult": max_result}
    params.update({k: v for k, v in filters.items() if v is not None})
    r = _get(url, params=params)
    payload = r.json()
    rows = []
    for o in payload.get("observations", []):
        rec = dict(o.get("dimensions", {}))
        mes = o.get("measures", {}).get("OBS_VALUE_NIVEAU", {})
        rec["valeur"] = mes.get("value")
        rows.append(rec)
    df = pd.DataFrame(rows)
    _journaliser(serie or dataset, "INSEE (API Mélodi)", r.url, len(df))
    return df


if __name__ == "__main__":
    print("Test WB :")
    df = wb("NY.GDP.PCAP.PP.CD", ["FRA", "USA"], 2020, 2023, serie="test")
    print(df.head())
    print("\nTest Eurostat (dépense publique % PIB) :")
    e = eurostat("gov_10a_exp", serie="test_eurostat", sector="S13", na_item="TE",
                 cofog99="TOTAL", unit="PC_GDP", geo=["FR", "DE", "NL"], time="2022")
    print(e[["geo", "valeur"]].to_string(index=False))
