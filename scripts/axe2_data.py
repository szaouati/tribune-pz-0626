"""
AXE 2 — L'Europe heureuse et son déclin relatif : collecte des données.
  1) Part dans le PIB mondial (courant) par zone, 1990-2024  [Banque mondiale]
  2) Écart de PIB/hab PPA USA vs FRA/DEU/ITA/ESP, 2000-2024  [Banque mondiale]
  3) Scores Better Life Index (4 dimensions), dernière édition  [OCDE, DF_BLI]
  4) Heures travaillées annuelles par travailleur, 2000-2023  [OCDE via OWID]
"""
import json
import numpy as np
import pandas as pd
import config as C
import sources as S
import livraison as L

A = C.DATA / "axe2"; A.mkdir(parents=True, exist_ok=True)
meta = []
def M(serie, source, url, unite, periode, notes):
    meta.append(dict(serie=serie, source=source, url=url, unite=unite, periode=periode,
                     date_extraction=C.DATE_EXTRACTION, notes=notes))

# ---------------------------------------------------------------------------
# 1) PART DANS LE PIB MONDIAL (courant, $ US)
# ---------------------------------------------------------------------------
print("PIB mondial par zone…")
gdp = S.wb("NY.GDP.MKTP.CD", ["EUU", "USA", "CHN", "WLD"], 1990, 2024, serie="PIB_zones")
w = gdp.pivot_table(index="annee", columns="iso3", values="valeur")
parts = pd.DataFrame(index=w.index)
parts["Union européenne (27)"] = w["EUU"] / w["WLD"] * 100
parts["États-Unis"] = w["USA"] / w["WLD"] * 100
parts["Chine"] = w["CHN"] / w["WLD"] * 100
parts["Reste du monde"] = 100 - parts.sum(axis=1)
parts = parts.round(2).reset_index()
L.ecrire_csv(parts, A / "01_part_pib_mondial_zones_1990_2024.csv")
M("Part dans le PIB mondial (UE-27, USA, Chine, reste du monde)",
  "Banque mondiale — WDI (NY.GDP.MKTP.CD, PIB courant $US)",
  "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD",
  "% du PIB mondial courant", "1990-2024",
  "Agrégat « Union européenne » = composition actuelle à 27 (rétropolée). Reste du monde = solde.")

# ---------------------------------------------------------------------------
# 2) ÉCART DE PIB/HAB PPA — USA vs Europe
# ---------------------------------------------------------------------------
print("Écart PIB/hab PPA US vs Europe…")
pays = ["USA", "FRA", "DEU", "ITA", "ESP"]
g2 = S.wb("NY.GDP.PCAP.PP.CD", pays, 2000, 2024, serie="PIB_hab_PPA_axe2")
g2w = g2.pivot_table(index="annee", columns="iso3", values="valeur")
ecart = pd.DataFrame(index=g2w.index)
for p in ["FRA", "DEU", "ITA", "ESP"]:
    ecart[f"PIB/hab {C.PAYS[p]}"] = g2w[p].round(0)
ecart["PIB/hab États-Unis"] = g2w["USA"].round(0)
for p in ["FRA", "DEU", "ITA", "ESP"]:
    ecart[f"Écart US/{C.PAYS[p]} (%)"] = ((g2w["USA"] - g2w[p]) / g2w[p] * 100).round(1)
ecart = ecart.reset_index()
L.ecrire_csv(ecart, A / "02_ecart_pib_hab_us_europe_2000_2024.csv")
M("PIB/hab PPA et écart relatif États-Unis vs Europe",
  "Banque mondiale — WDI (NY.GDP.PCAP.PP.CD)",
  "https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD",
  "$ internationaux PPA ; écart en %", "2000-2024",
  "Écart = (PIB/hab USA − PIB/hab pays) / PIB/hab pays.")

# ---------------------------------------------------------------------------
# 3) BETTER LIFE INDEX — scores 0-10 reconstitués (méthode OCDE min-max)
# ---------------------------------------------------------------------------
print("Better Life Index (4 dimensions)…")
bli = json.load(open(C.RAW / "oecd_bli.json"))
df = S.parse_sdmx_json(bli)
df = df[df.INEQUALITY == "TOT"].copy()
df["valeur"] = pd.to_numeric(df["valeur"], errors="coerce")
piv = df.pivot_table(index="LOCATION", columns="INDICATOR", values="valeur")

# Dimensions retenues et leurs sous-indicateurs (sens : +/- = orientation positive/négative)
DIMS = {
    "Satisfaction de vie": {"SW_LIFS": +1},
    "Équilibre travail-vie": {"WL_EWLH": -1, "WL_TNOW": +1},
    "Logement": {"HO_NUMR": +1, "HO_HISH": -1, "HO_BASE": -1},
    "Sécurité": {"PS_FSAFEN": +1, "PS_REPH": -1},
}
def norm(col, sens):
    s = piv[col].dropna()
    lo, hi = s.min(), s.max()
    z = (piv[col] - lo) / (hi - lo) * 10
    return z if sens > 0 else 10 - z

scores = pd.DataFrame(index=piv.index)
for dim, comps in DIMS.items():
    parts_dim = [norm(c, s) for c, s in comps.items()]
    scores[dim] = pd.concat(parts_dim, axis=1).mean(axis=1).round(2)
scores = scores.reset_index().rename(columns={"LOCATION": "iso3"})
focus = ["USA", "DEU", "FRA", "ITA", "ESP"]
scores_focus = scores[scores.iso3.isin(focus)].copy()
scores_focus["pays"] = scores_focus["iso3"].map(C.PAYS)
# valeurs brutes (transparence)
bruts = piv.loc[[c for c in focus if c in piv.index],
                ["SW_LIFS","WL_EWLH","WL_TNOW","HO_NUMR","HO_HISH","HO_BASE","PS_FSAFEN","PS_REPH"]].round(2)
bruts = bruts.reset_index().rename(columns={"LOCATION":"iso3"})
L.ecrire_csv(scores_focus, A / "03_bli_scores_4dimensions.csv")
L.ecrire_csv(bruts, A / "03b_bli_indicateurs_bruts.csv")
M("Scores Better Life Index — 4 dimensions (satisfaction de vie, équilibre travail-vie, logement, sécurité)",
  "OCDE — Better Life Index (dataflow archivé DF_BLI, édition 2020, dernière disponible)",
  "https://data-explorer.oecd.org/vis?tenant=archive&df[id]=DF_BLI",
  "score 0-10 (normalisation min-max OCDE)", "édition 2020",
  "Scores reconstitués selon la méthode BLI : chaque sous-indicateur normalisé min-max sur l'OCDE (0-10, "
  "orientation corrigée), puis moyenne par dimension. Indicateurs bruts fournis en feuille séparée.")

# ---------------------------------------------------------------------------
# 4) HEURES TRAVAILLÉES ANNUELLES PAR TRAVAILLEUR (OCDE)
# ---------------------------------------------------------------------------
print("Heures travaillées…")
h = S.owid("annual-working-hours-per-worker", serie="heures_travaillees")
hcol = [c for c in h.columns if "hour" in c.lower()][0]
h = h.rename(columns={hcol: "heures_annuelles"})
h = h[h["code"].isin(focus) & (h["year"] >= 2000) & (h["year"] <= 2023)]
h = h[["code","year","heures_annuelles"]].rename(columns={"code":"iso3","year":"annee"})
h["pays"] = h["iso3"].map(C.PAYS)
h["heures_annuelles"] = h["heures_annuelles"].round(0)
L.ecrire_csv(h, A / "04_heures_travaillees_2000_2023.csv")
M("Heures travaillées annuelles par travailleur",
  "OCDE — Average annual hours actually worked (via Our World in Data)",
  "https://ourworldindata.org/grapher/annual-working-hours-per-worker",
  "heures/an/travailleur", "2000-2023",
  "Moyenne par personne en emploi (temps plein + partiel). Comparaisons de niveau à interpréter avec prudence (définitions nationales).")

# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------
L.construire_xlsx(A / "axe2_europe_declin.xlsx",
    feuilles={
        "Part_PIB_mondial": parts,
        "Ecart_PIB_hab_US_Europe": ecart,
        "BLI_scores_4dim": scores_focus[["iso3","pays"]+list(DIMS.keys())],
        "BLI_indicateurs_bruts": bruts,
        "Heures_travaillees": h,
    },
    metadonnees=pd.DataFrame(meta),
    titre_classeur="AXE 2 — L'Europe heureuse et son déclin relatif")

print("\nRécap Axe 2 :")
print("Part PIB 2024:", parts[parts.annee==2024].to_dict("records"))
print("BLI focus:\n", scores_focus[["pays"]+list(DIMS.keys())].to_string(index=False))
print("Heures 2023:\n", h[h.annee==2023][["pays","heures_annuelles"]].to_string(index=False))
