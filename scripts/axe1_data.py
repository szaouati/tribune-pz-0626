"""
AXE 1 — Bonheur déclaré vs performance économique : collecte des données.
Sorties : data/axe1/*.csv + data/axe1/axe1_bonheur_economie.xlsx
"""
import pandas as pd
import config as C
import sources as S
import livraison as L

A = C.DATA / "axe1"
A.mkdir(parents=True, exist_ok=True)
meta_rows = []

def meta(serie, source, url, unite, periode, notes):
    meta_rows.append(dict(serie=serie, source=source, url=url, unite=unite,
                          periode=periode, date_extraction=C.DATE_EXTRACTION, notes=notes))

# ---------------------------------------------------------------------------
# 1) World Happiness Report — échelle de Cantril (0-10), via OWID
# ---------------------------------------------------------------------------
print("WHR Cantril ladder…")
whr = S.owid("happiness-cantril-ladder", serie="WHR_cantril")
col = [c for c in whr.columns if "cantril" in c.lower() or "ladder" in c.lower()][0]
whr = whr.rename(columns={col: "score_bonheur"})
whr = whr[whr["code"].isin(C.PAYS.keys())]
whr = whr[(whr["year"] >= 2012) & (whr["year"] <= 2024)].copy()
whr["pays_fr"] = whr["code"].map(C.PAYS)
whr = whr[["code", "pays_fr", "year", "score_bonheur"]].rename(
    columns={"code": "iso3", "year": "annee"}).sort_values(["iso3", "annee"])
L.ecrire_csv(whr, A / "01_whr_score_bonheur_2012_2024.csv")
meta("Score de bonheur (échelle de Cantril 0-10)",
     "World Happiness Report (Gallup World Poll), via Our World in Data",
     "https://ourworldindata.org/grapher/happiness-cantril-ladder",
     "Score 0-10 (moy. 3 ans)", "2012-2024",
     "Moyenne mobile sur 3 ans de l'échelle de Cantril (Gallup). Bhoutan : couverture partielle.")
print("  pays couverts:", sorted(whr['iso3'].unique()), "| années:", whr['annee'].min(), "-", whr['annee'].max())

# ---------------------------------------------------------------------------
# 2) PIB par habitant en PPA ($ internationaux courants) — Banque mondiale
# ---------------------------------------------------------------------------
print("PIB/hab PPA…")
gdp = S.wb("NY.GDP.PCAP.PP.CD", list(C.PAYS.keys()), 2012, 2024, serie="PIB_hab_PPA")
gdp["pays_fr"] = gdp["iso3"].map(C.PAYS)
gdp = gdp[["iso3", "pays_fr", "annee", "valeur"]].rename(columns={"valeur": "pib_hab_ppa"})
L.ecrire_csv(gdp, A / "02_pib_hab_ppa_2012_2024.csv")
meta("PIB par habitant en PPA",
     "Banque mondiale — World Development Indicators (NY.GDP.PCAP.PP.CD)",
     "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.CD",
     "$ internationaux courants (PPA)", "2012-2024",
     "Parité de pouvoir d'achat, dollars internationaux courants. Bhoutan : données jusqu'à 2022.")

# ---------------------------------------------------------------------------
# 3) Population (taille des bulles) — Banque mondiale
# ---------------------------------------------------------------------------
print("Population…")
pop = S.wb("SP.POP.TOTL", list(C.PAYS.keys()), 2012, 2024, serie="population")
pop["pays_fr"] = pop["iso3"].map(C.PAYS)
pop = pop[["iso3", "pays_fr", "annee", "valeur"]].rename(columns={"valeur": "population"})
L.ecrire_csv(pop, A / "03_population_2012_2024.csv")
meta("Population totale",
     "Banque mondiale — WDI (SP.POP.TOTL)",
     "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL",
     "habitants", "2012-2024", "Utilisée pour dimensionner les bulles du nuage de points.")

# ---------------------------------------------------------------------------
# 4) Paradoxe d'Easterlin — PIB réel/hab US (constant) 1970-2024
# ---------------------------------------------------------------------------
print("PIB réel/hab US (Easterlin)…")
gdp_us = S.wb("NY.GDP.PCAP.KD", ["USA"], 1970, 2024, serie="PIB_reel_hab_US")
gdp_us = gdp_us[["annee", "valeur"]].rename(columns={"valeur": "pib_reel_hab_usd2015"})
L.ecrire_csv(gdp_us, A / "04_pib_reel_hab_us_1970_2024.csv")
meta("PIB réel par habitant — États-Unis",
     "Banque mondiale — WDI (NY.GDP.PCAP.KD)",
     "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.PCAP.KD",
     "$ US constants 2015", "1970-2024",
     "Volet 'revenu' du paradoxe d'Easterlin (croissance réelle du niveau de vie).")

print("\nRécapitulatif Axe 1 :")
print(" WHR:", whr.shape, "| PIB PPA:", gdp.shape, "| Pop:", pop.shape, "| PIB réel US:", gdp_us.shape)

# Sauvegarde des dataframes pour la suite (Easterlin GSS ajouté ensuite)
whr.to_pickle(A / "_whr.pkl"); gdp.to_pickle(A / "_gdp.pkl")
pop.to_pickle(A / "_pop.pkl"); gdp_us.to_pickle(A / "_gdpus.pkl")
pd.DataFrame(meta_rows).to_pickle(A / "_meta.pkl")
print("OK — pickles intermédiaires sauvegardés.")
