"""
AXE 5 — Le coût du territoire : densité, fragmentation et dépense publique.
Comparaison France / Allemagne / Pays-Bas.

Thèse explorée : un territoire vaste, peu dense et très émietté impose un
maillage de services publics (communes, écoles, sécurité) plus serré — donc
un surcoût d'argent public. Les données nuancent : la France a bien le maillage
le plus dense et la dépense publique la plus lourde (% PIB), mais PAS la dépense
la plus élevée par habitant ni par fonction (les Pays-Bas, plus riches, dépensent
plus en € par tête). Le « surcoût » se lit dans le poids global, pas fonction par
fonction.

  1) Densité nationale + superficie + population        [Eurostat demo_r_d3dens, demo_pjan]
  2) Densité régionale (NUTS3) — dispersion du territoire [Eurostat demo_r_d3dens]
  3) Communes / unités administratives locales           [INSEE, Destatis, CBS — compilation]
  4) Dépense publique COFOG : total, éducation, sécurité  [Eurostat gov_10a_exp]
  5) Maillage de proximité : écoles + police              [DEPP/Destatis/CBS ; Eurostat crim_just_job]
"""
import numpy as np
import pandas as pd
import config as C
import sources as S
import livraison as L

A = C.DATA / "axe5"; A.mkdir(parents=True, exist_ok=True)

# Eurostat utilise des codes pays à 2 lettres ; on les rapatrie en ISO3 maison.
EU2ISO = {"FR": "FRA", "DE": "DEU", "NL": "NLD"}
ISO2EU = {v: k for k, v in EU2ISO.items()}
EU = list(EU2ISO)                       # ["FR", "DE", "NL"]
ISO = list(EU2ISO.values())             # ["FRA", "DEU", "NLD"]
ANNEE_FLUX = "2023"                     # dernier millésime COFOG complet
ANNEE_DENS = "2022"                    # dernier millésime densité régionale complet
ANNEE_POLICE = "2022"                  # dernier millésime police couvrant FR+DE+NL

meta = []
def M(serie, source, url, unite, periode, notes):
    meta.append(dict(serie=serie, source=source, url=url, unite=unite, periode=periode,
                     date_extraction=C.DATE_EXTRACTION, notes=notes))

# ---------------------------------------------------------------------------
# 1) DENSITÉ NATIONALE + SUPERFICIE + POPULATION
# ---------------------------------------------------------------------------
print("Densité nationale + régionale + population…")
dn = S.eurostat("demo_r_d3dens", serie="densite_nationale", geo=EU, time=ANNEE_DENS)
dn = dn[dn.geo.isin(EU)].set_index("geo")["valeur"]
pj = S.eurostat("demo_pjan", serie="population", sex="T", age="TOTAL", geo=EU, time=ANNEE_FLUX)
pj = pj[pj.geo.isin(EU)].set_index("geo")["valeur"]
# Densité NUTS3 (toutes régions) — réutilisée pour la dispersion (série 2) ET le calcul
# de la densité « France métropolitaine » (hors DOM).
dr_all = S.eurostat("demo_r_d3dens", serie="densite_nuts3", time=ANNEE_DENS)
popn3 = S.eurostat("demo_r_pjanaggr3", serie="population_nuts3",
                   sex="T", age="TOTAL", unit="NR", time=ANNEE_DENS)

# #4 — Densité France métropolitaine : NUTS3 hors DOM (codes FRY*). superficie = pop / densité.
d3 = dr_all[(dr_all.geo.str.len() == 5) & dr_all.valeur.notna()][["geo", "valeur"]].rename(columns={"valeur": "dens"})
p3 = popn3[(popn3.geo.str.len() == 5) & popn3.valeur.notna()][["geo", "valeur"]].rename(columns={"valeur": "pop"})
m3 = d3.merge(p3, on="geo"); m3["area"] = m3["pop"] / m3["dens"]
metro = m3[m3.geo.str.startswith("FR") & ~m3.geo.str.startswith("FRY")]
DENS_METRO_FR = round(metro["pop"].sum() / metro["area"].sum(), 1)

rows = []
for eu in EU:
    dens = float(dn[eu]); pop = float(pj[eu])
    rows.append(dict(iso3=EU2ISO[eu], pays=C.PAYS[EU2ISO[eu]],
                     densite_hab_km2=round(dens, 1),
                     densite_metropole_hab_km2=(DENS_METRO_FR if eu == "FR" else round(dens, 1)),
                     population=int(pop), superficie_km2=int(round(pop / dens))))
df1 = pd.DataFrame(rows)
POP = df1.set_index("iso3")["population"].to_dict()   # réutilisé pour les ratios
L.ecrire_csv(df1, A / "01_densite_superficie_population.csv")
M("Densité de population, superficie et population (FR/DE/NL)",
  "Eurostat — densité (demo_r_d3dens), population (demo_pjan), population NUTS3 (demo_r_pjanaggr3)",
  "https://ec.europa.eu/eurostat/databrowser/product/page/demo_r_d3dens",
  "habitants/km² ; km² ; habitants", f"densité {ANNEE_DENS}, population {ANNEE_FLUX}",
  "Superficie déduite (population / densité), cohérente avec la surface terrestre Eurostat. "
  f"densite_metropole_hab_km2 = France hors DOM (NUTS3 hors FRY*) = {DENS_METRO_FR} hab/km² "
  "(vs France entière, qui inclut les départements d'outre-mer). DE/NL : pas d'outre-mer, valeur identique.")

# ---------------------------------------------------------------------------
# 2) DENSITÉ RÉGIONALE (NUTS3) — la diversité du territoire
# ---------------------------------------------------------------------------
print("Densité régionale NUTS3…")
# NUTS3 = code à 5 caractères ; on garde FR/DE/NL et on écarte les agrégats nationaux/NUTS1-2.
dr = dr_all[(dr_all.geo.str.len() == 5) & (dr_all.geo.str[:2].isin(EU)) & dr_all.valeur.notna()].copy()
dr["iso3"] = dr.geo.str[:2].map(EU2ISO)
dr["pays"] = dr["iso3"].map(C.PAYS)
df2 = dr.rename(columns={"geo": "nuts3", "geo_label": "region", "valeur": "densite_hab_km2"})
df2 = df2[["iso3", "pays", "nuts3", "region", "densite_hab_km2"]].sort_values(["iso3", "densite_hab_km2"])
df2["densite_hab_km2"] = df2["densite_hab_km2"].round(1)
L.ecrire_csv(df2, A / "02_densite_regionale_nuts3.csv")
M("Densité de population par région NUTS3 (FR/DE/NL)",
  "Eurostat — population density by NUTS3 region (demo_r_d3dens)",
  "https://ec.europa.eu/eurostat/databrowser/product/page/demo_r_d3dens",
  "habitants/km²", ANNEE_DENS,
  f"{len(df2)} régions NUTS3. Mesure la dispersion interne du territoire "
  "(la France conserve des régions très peu peuplées que ni l'Allemagne ni les Pays-Bas ne connaissent).")

# ---------------------------------------------------------------------------
# 3) COMMUNES / UNITÉS ADMINISTRATIVES LOCALES (compilation sources nationales)
# ---------------------------------------------------------------------------
print("Communes / émiettement administratif…")
# Comptes officiels — pas d'API unique comparable, compilation documentée.
COMMUNES = {"FRA": 34935, "DEU": 10753, "NLD": 342}
SRC_COMMUNES = {
    "FRA": "INSEE / vie-publique.fr — 34 935 communes au 1er janvier 2024",
    "DEU": "Statistisches Bundesamt (Destatis) — 10 753 Gemeinden au 1er janvier 2024",
    "NLD": "CBS — 342 gemeenten en 2024 (hors 3 communes spéciales caribéennes)",
}
sup = df1.set_index("iso3")["superficie_km2"].to_dict()
rows = []
for iso in ISO:
    n = COMMUNES[iso]
    rows.append(dict(iso3=iso, pays=C.PAYS[iso], nb_communes=n,
                     communes_pour_100k_hab=round(n / POP[iso] * 1e5, 1),
                     hab_moyen_par_commune=int(round(POP[iso] / n)),
                     km2_moyen_par_commune=round(sup[iso] / n, 1),
                     source=SRC_COMMUNES[iso]))
df3 = pd.DataFrame(rows)
L.ecrire_csv(df3, A / "03_communes_fragmentation.csv")
M("Nombre de communes (unités administratives locales) et émiettement",
  "INSEE (FR), Destatis (DE), CBS (NL) — compilation",
  "https://www.insee.fr/fr/information/2549968",
  "nombre ; pour 100 000 hab ; hab/commune ; km²/commune", "2024",
  "La France compte ~40 % de toutes les communes de l'Union européenne. Comptes officiels "
  "non disponibles par une API unique : compilation manuelle des instituts nationaux (millésime 2024).")

# ---------------------------------------------------------------------------
# 4) DÉPENSE PUBLIQUE COFOG : total / éducation / ordre & sécurité
# ---------------------------------------------------------------------------
print("Dépense publique COFOG…")
COFOG = {"TOTAL": "Dépense publique totale",
         "GF09": "Éducation",
         "GF03": "Ordre et sécurité publics"}
exp = S.eurostat("gov_10a_exp", serie="cofog", sector="S13", na_item="TE",
                 cofog99=list(COFOG), unit=["PC_GDP", "MIO_EUR"], geo=EU, time=ANNEE_FLUX)
piv = exp.pivot_table(index=["geo", "cofog99"], columns="unit", values="valeur")
# #3 — Parité de pouvoir d'achat : facteur de conversion PPA du PIB (EU27_2020=1).
# SPA/hab = €/hab / PPA -> neutralise l'écart de niveau de prix entre pays.
ppp = S.eurostat("prc_ppp_ind", serie="ppp_pib", na_item="PPP_EU27_2020",
                 ppp_cat="GDP", geo=EU, time=ANNEE_FLUX)
ppp = ppp[ppp.geo.isin(EU)].set_index("geo")["valeur"].astype(float)
rows = []
for eu in EU:
    iso = EU2ISO[eu]
    for code, libelle in COFOG.items():
        pc = float(piv.loc[(eu, code), "PC_GDP"])
        mio = float(piv.loc[(eu, code), "MIO_EUR"])
        eur_hab = mio * 1e6 / POP[iso]
        rows.append(dict(iso3=iso, pays=C.PAYS[iso], fonction=libelle, cofog=code,
                         pct_pib=round(pc, 1),
                         eur_par_hab=int(round(eur_hab)),
                         spa_par_hab=int(round(eur_hab / float(ppp[eu])))))
df4 = pd.DataFrame(rows)
L.ecrire_csv(df4, A / "04_depense_publique_cofog.csv")
M("Dépense publique par fonction (COFOG) : total, éducation, ordre et sécurité",
  "Eurostat — dépenses publiques par fonction (gov_10a_exp, S13) ; PPA du PIB (prc_ppp_ind)",
  "https://ec.europa.eu/eurostat/databrowser/product/page/gov_10a_exp",
  "% du PIB ; € par habitant ; SPA par habitant", ANNEE_FLUX,
  "€/hab calculé (dépense M€ / population). spa_par_hab = €/hab converti en standard de pouvoir d'achat "
  "(÷ PPA du PIB, EU27_2020=1) : neutralise le niveau de prix national. En SPA, l'écart entre les trois "
  "pays se resserre fortement — la France n'est plus « en dessous », elle est quasi à parité.")

# ---------------------------------------------------------------------------
# 5) MAILLAGE DE PROXIMITÉ : écoles du 1er degré + forces de police
# ---------------------------------------------------------------------------
print("Maillage : écoles + police…")
pol = S.eurostat("crim_just_job", serie="police", isco08="OC5412", sex="T",
                 unit="P_HTHAB", geo=EU, time=ANNEE_POLICE)
pol = pol[pol.geo.isin(EU)].set_index("geo")["valeur"]
# #2 — Effectifs scolarisés en CITE 1 (primaire, ~6-11 ans), périmètre HARMONISÉ Eurostat,
# pour comparer à base égale (le comptage d'écoles, lui, reste de périmètre national).
cite1 = S.eurostat("educ_uoe_enra01", serie="eleves_cite1", isced11="ED1", sex="T",
                   unit="NR", worktime="TOTAL", sector="TOT_SEC", geo=EU, time=ANNEE_FLUX)
cite1 = cite1[cite1.geo.isin(EU)].set_index("geo")["valeur"]

# Écoles du premier degré : comptes nationaux (pas d'API comparable). Périmètres non
# identiques -> on fournit aussi les effectifs CITE 1 harmonisés (ci-dessus) pour la comparaison.
ECOLES = {  # (nb écoles 1er degré, élèves 1er degré, source)
    "FRA": (47792, 6_339_900, "DEPP — RERS 2025 (écoles du 1er degré, public+privé, rentrée 2023 ; périmètre CITE 0+1, maternelle incluse)"),
    "DEU": (15531, 3_098_664, "Destatis — Allgemeinbildende Schulen 2023/24 (Grundschulen = CITE 1 ; Kindergarten hors champ)"),
    "NLD": (6038,  1_359_278, "CBS tab. 03753 / OCW — basisscholen 2023/24 (basisonderwijs ; groep 1-2 = CITE 0 + groep 3-8 = CITE 1)"),
}
rows = []
for iso in ISO:
    eu = ISO2EU[iso]
    n_ec, eleves, _ = ECOLES[iso]
    rows.append(dict(iso3=iso, pays=C.PAYS[iso],
                     ecoles_1er_degre=n_ec,
                     ecoles_pour_100k_hab=round(n_ec / POP[iso] * 1e5, 1),
                     eleves_1er_degre=eleves,
                     eleves_primaire_cite1=int(cite1[eu]),
                     policiers_pour_100k_hab=round(float(pol[eu]), 1)))
df5 = pd.DataFrame(rows)
L.ecrire_csv(df5, A / "05_maillage_ecoles_police.csv")
M("Maillage de proximité : écoles du 1er degré, élèves (CITE 1 harmonisé) et police",
  "DEPP (FR), Destatis (DE), CBS/OCW (NL) pour les écoles ; Eurostat educ_uoe_enra01 (CITE 1) et crim_just_job (OC5412)",
  "https://ec.europa.eu/eurostat/databrowser/product/page/educ_uoe_enra01",
  "nombre ; pour 100 000 hab ; élèves", f"écoles 2023/24, élèves CITE 1 {ANNEE_FLUX}, police {ANNEE_POLICE}",
  "Police : agents pour 100 000 hab (CITP-08 OC5412). eleves_primaire_cite1 = effectif CITE 1 (primaire) "
  "harmonisé Eurostat — comparable entre pays. Le COMPTAGE d'écoles reste de périmètre national : l'« école » "
  "FR et le basisschool NL couvrent CITE 0+1, la Grundschule DE le seul CITE 1 ; comparaison à interpréter avec cette réserve.")

# ---------------------------------------------------------------------------
# Excel multi-feuilles
# ---------------------------------------------------------------------------
L.construire_xlsx(A / "axe5_territoire_depense.xlsx",
    feuilles={
        "Densite_superficie_pop": df1,
        "Densite_regionale_NUTS3": df2,
        "Communes_fragmentation": df3,
        "Depense_publique_COFOG": df4,
        "Maillage_ecoles_police": df5,
    },
    metadonnees=pd.DataFrame(meta),
    titre_classeur="AXE 5 — Le coût du territoire : densité, fragmentation, dépense publique")

print("\nRécap Axe 5 :")
print("Densité (hab/km²) :", dict(zip(df1.pays, df1.densite_hab_km2)))
print("  dont France métropole (hors DOM) :", DENS_METRO_FR, "hab/km²")
print("Communes /100k    :", dict(zip(df3.pays, df3.communes_pour_100k_hab)))
print("Dépense % PIB     :", {r.pays: r.pct_pib for r in df4.itertuples() if r.cofog == "TOTAL"})
print("Dépense €/hab tot :", {r.pays: r.eur_par_hab for r in df4.itertuples() if r.cofog == "TOTAL"})
print("Dépense SPA/hab   :", {r.pays: r.spa_par_hab for r in df4.itertuples() if r.cofog == "TOTAL"})
print("Écoles /100k      :", dict(zip(df5.pays, df5.ecoles_pour_100k_hab)))
print("Élèves CITE 1     :", dict(zip(df5.pays, df5.eleves_primaire_cite1)))
print("Police /100k      :", dict(zip(df5.pays, df5.policiers_pour_100k_hab)))
print("NUTS3 densité — médiane par pays :")
print(df2.groupby("pays")["densite_hab_km2"].agg(["count", "min", "median", "max"]).round(0).to_string())
