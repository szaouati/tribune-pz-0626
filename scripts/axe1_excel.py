"""AXE 1 — assemblage du classeur Excel livrable + version large lisible."""
import pandas as pd
import config as C
import livraison as L

A = C.DATA / "axe1"

whr = pd.read_csv(A / "01_whr_score_bonheur_2012_2024.csv")
gdp = pd.read_csv(A / "02_pib_hab_ppa_2012_2024.csv")
pop = pd.read_csv(A / "03_population_2012_2024.csv")
gdp_us = pd.read_csv(A / "04_pib_reel_hab_us_1970_2024.csv")
gss = pd.read_csv(A / "05_gss_bonheur_us_1972_2024.csv")

# Tables larges (lecture humaine)
whr_w = whr.pivot_table(index="annee", columns="iso3", values="score_bonheur").round(3).reset_index()
gdp_w = gdp.pivot_table(index="annee", columns="iso3", values="pib_hab_ppa").round(0).reset_index()

metadonnees = pd.DataFrame([
    dict(serie="Score de bonheur (échelle de Cantril 0-10)",
         source="World Happiness Report / Gallup World Poll (via Our World in Data)",
         url="https://ourworldindata.org/grapher/happiness-cantril-ladder",
         unite="score 0-10 (moyenne mobile 3 ans)", periode="2012-2024",
         date_extraction=C.DATE_EXTRACTION,
         notes="Échelle de Cantril (« échelle de la vie »). Bhoutan : données arrêtées en 2018 (sortie du Gallup World Poll)."),
    dict(serie="PIB par habitant en PPA",
         source="Banque mondiale — World Development Indicators (NY.GDP.PCAP.PP.CD)",
         url="https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD",
         unite="$ internationaux courants (PPA)", periode="2012-2024",
         date_extraction=C.DATE_EXTRACTION,
         notes="Parité de pouvoir d'achat. Bhoutan : dernière donnée 2023."),
    dict(serie="Population totale",
         source="Banque mondiale — WDI (SP.POP.TOTL)",
         url="https://data.worldbank.org/indicator/SP.POP.TOTL",
         unite="habitants", periode="2012-2024", date_extraction=C.DATE_EXTRACTION,
         notes="Sert à dimensionner les bulles du nuage de points."),
    dict(serie="PIB réel par habitant — États-Unis",
         source="Banque mondiale — WDI (NY.GDP.PCAP.KD)",
         url="https://data.worldbank.org/indicator/NY.GDP.PCAP.KD",
         unite="$ US constants 2015", periode="1970-2024", date_extraction=C.DATE_EXTRACTION,
         notes="Volet « revenu réel » du paradoxe d'Easterlin."),
    dict(serie="Bonheur déclaré — États-Unis (% « very happy »)",
         source="General Social Survey (NORC, Univ. Chicago), microdonnées GSS 1972-2024 (release R3)",
         url="https://gss.norc.org/us/en/gss/get-the-data.html",
         unite="% des répondants", periode="1972-2024", date_extraction=C.DATE_EXTRACTION,
         notes="Calcul propre à partir du fichier cumulatif (var. HAPPY, pondération WTSSPS). Volet « bien-être subjectif » du paradoxe d'Easterlin. Rupture 2021 (refonte du protocole + COVID)."),
])

L.construire_xlsx(
    A / "axe1_bonheur_economie.xlsx",
    feuilles={
        "WHR_score (long)": whr,
        "WHR_score (large)": whr_w,
        "PIB_hab_PPA (long)": gdp,
        "PIB_hab_PPA (large)": gdp_w,
        "Population": pop,
        "Easterlin_PIB_reel_US": gdp_us,
        "Easterlin_bonheur_GSS_US": gss,
    },
    metadonnees=metadonnees,
    titre_classeur="AXE 1 — Bonheur déclaré vs performance économique",
)
print("Axe 1 — Excel + CSV prêts.")
