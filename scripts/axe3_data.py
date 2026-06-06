"""
AXE 3 — Composants du bonheur et sous-jacents économiques : collecte.
  1) Espérance de vie à la naissance, 1990-2023            [Banque mondiale]
  2) R&D pharmaceutique des entreprises par zone, 2000-2023 [OCDE ANBERD]
  3) Dépenses publiques de santé en % du PIB, 2000-2023     [Banque mondiale]
  4) Qualité de l'air (PM2.5) & désindustrialisation         [Banque mondiale]
  5) Origine géographique des nouvelles molécules           [EFPIA / IQVIA, documenté]
"""
import numpy as np
import pandas as pd
import config as C
import sources as S
import livraison as L

A = C.DATA / "axe3"; A.mkdir(parents=True, exist_ok=True)
meta = []
def M(serie, source, url, unite, periode, notes):
    meta.append(dict(serie=serie, source=source, url=url, unite=unite, periode=periode,
                     date_extraction=C.DATE_EXTRACTION, notes=notes))

PAYS_LE = ["USA","FRA","DEU","JPN","KOR","CHN","BTN"]  # espérance de vie (sélection)

# ---------------------------------------------------------------------------
# 1) ESPÉRANCE DE VIE À LA NAISSANCE
# ---------------------------------------------------------------------------
print("Espérance de vie…")
le = S.wb("SP.DYN.LE00.IN", PAYS_LE, 1990, 2023, serie="esperance_vie")
le["pays"] = le["iso3"].map(C.PAYS)
le = le[["iso3","pays","annee","valeur"]].rename(columns={"valeur":"esperance_vie"})
le["esperance_vie"] = le["esperance_vie"].round(2)
L.ecrire_csv(le, A / "01_esperance_vie_1990_2023.csv")
M("Espérance de vie à la naissance",
  "Banque mondiale — WDI (SP.DYN.LE00.IN ; source OMS/Nations Unies)",
  "https://data.worldbank.org/indicator/SP.DYN.LE00.IN",
  "années", "1990-2023", "Total (hommes+femmes).")

# ---------------------------------------------------------------------------
# 2) R&D PHARMACEUTIQUE DES ENTREPRISES (ANBERD, C21), par zone
# ---------------------------------------------------------------------------
print("R&D pharma (ANBERD)…")
flow = "OECD.STI.STP,DSD_ANBERD@DF_ANBERDi4,1.0"
key = ".A.MA.C21.USD_PPP.V.B"  # REF_AREA(all).FREQ.CRITERIA.ACTIVITY.UNIT.PRICE.MEASURE
raw = S.oecd_sdmx(flow, key, params={"startPeriod": "2000", "endPeriod": "2023"}, serie="RD_pharma")
rd = S.parse_sdmx_json(raw)
rd["annee"] = rd["TIME_PERIOD"].astype(int)
rd["valeur"] = pd.to_numeric(rd["valeur"], errors="coerce") / 1e9  # -> milliards USD PPA
EUROPE = ["AUT","BEL","BGR","CZE","DEU","DNK","ESP","EST","FIN","FRA","GRC","HRV","HUN",
          "IRL","ITA","LTU","LVA","NLD","POL","PRT","ROU","SVK","SVN","SWE","CHE","NOR","ISL"]
def zone(iso):
    if iso == "USA": return "États-Unis"
    if iso == "JPN": return "Japon"
    if iso == "CHN": return "Chine"
    if iso in EUROPE: return "Europe (UE + AELE)"
    return None
rd["zone"] = rd["REF_AREA"].map(zone)
rd_z = rd.dropna(subset=["zone"]).groupby(["zone","annee"])["valeur"].sum().round(2).reset_index()
rd_w = rd_z.pivot_table(index="annee", columns="zone", values="valeur").reset_index()
L.ecrire_csv(rd_z, A / "02_rd_pharma_zones_2000_2023.csv")
L.ecrire_csv(rd_w, A / "02b_rd_pharma_zones_large.csv")
M("Dépenses de R&D pharmaceutique des entreprises (industrie C21)",
  "OCDE — base ANBERD (R&D des entreprises par industrie, ISIC Rév.4 division 21)",
  "https://data-explorer.oecd.org (DSD_ANBERD@DF_ANBERDi4)",
  "milliards USD PPA, prix courants", "2000-2023",
  "Zone Europe = UE-27 (hors CYP/LUX/MLT) + Suisse, Norvège, Islande. ⚠ Royaume-Uni non couvert par ANBERD "
  "(Europe légèrement sous-estimée). « Reste du monde » non disponible (base OCDE + partenaires).")

# ---------------------------------------------------------------------------
# 3) DÉPENSES PUBLIQUES DE SANTÉ (% PIB)
# ---------------------------------------------------------------------------
print("Dépenses publiques de santé…")
PAYS_SANTE = ["USA","FRA","DEU","ITA","ESP","JPN","KOR","CHN"]
sh = S.wb("SH.XPD.GHED.GD.ZS", PAYS_SANTE, 2000, 2023, serie="sante_publique")
sh["pays"] = sh["iso3"].map(C.PAYS)
sh = sh[["iso3","pays","annee","valeur"]].rename(columns={"valeur":"depenses_sante_pub_pct_pib"})
sh["depenses_sante_pub_pct_pib"] = sh["depenses_sante_pub_pct_pib"].round(2)
L.ecrire_csv(sh, A / "03_depenses_sante_publique_2000_2023.csv")
M("Dépenses publiques de santé",
  "Banque mondiale — WDI (SH.XPD.GHED.GD.ZS ; source OMS Global Health Expenditure)",
  "https://data.worldbank.org/indicator/SH.XPD.GHED.GD.ZS",
  "% du PIB", "2000-2023", "Dépenses courantes de santé des administrations publiques.")

# ---------------------------------------------------------------------------
# 4) QUALITÉ DE L'AIR (PM2.5) & DÉSINDUSTRIALISATION
# ---------------------------------------------------------------------------
print("PM2.5 & industrie…")
pm = S.wb("EN.ATM.PM25.MC.M3", PAYS_SANTE, 1990, 2022, serie="pm25")
pm["pays"] = pm["iso3"].map(C.PAYS)
pm = pm[["iso3","pays","annee","valeur"]].rename(columns={"valeur":"pm25_ug_m3"}).round({"pm25_ug_m3":2})
L.ecrire_csv(pm, A / "04_pm25_qualite_air.csv")
man = S.wb("NV.IND.MANF.ZS", PAYS_SANTE, 2000, 2023, serie="industrie_manuf")
man["pays"] = man["iso3"].map(C.PAYS)
man = man[["iso3","pays","annee","valeur"]].rename(columns={"valeur":"manuf_pct_pib"}).round({"manuf_pct_pib":2})
L.ecrire_csv(man, A / "04b_industrie_manufacturiere_pct_pib.csv")
M("Qualité de l'air — exposition moyenne aux PM2.5",
  "Banque mondiale — WDI (EN.ATM.PM25.MC.M3 ; source OMS / van Donkelaar et al.)",
  "https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3",
  "µg/m³ (exposition annuelle moyenne)", "1990-2020",
  "Donnée disponible jusqu'à 2020. À corréler avec la part de l'industrie manufacturière.")
M("Industrie manufacturière (valeur ajoutée)",
  "Banque mondiale — WDI (NV.IND.MANF.ZS)",
  "https://data.worldbank.org/indicator/NV.IND.MANF.ZS",
  "% du PIB", "2000-2023", "Indicateur de (dés)industrialisation.")

# ---------------------------------------------------------------------------
# 5) ORIGINE GÉOGRAPHIQUE DES NOUVELLES MOLÉCULES (placeholder à compléter)
# ---------------------------------------------------------------------------
# Renseigné dans un second temps à partir des données EFPIA / IQVIA documentées.

L.construire_xlsx(A / "axe3_composants_bonheur.xlsx",
    feuilles={
        "Esperance_vie": le,
        "RD_pharma_zones (long)": rd_z,
        "RD_pharma_zones (large)": rd_w,
        "Depenses_sante_publique": sh,
        "Qualite_air_PM25": pm,
        "Industrie_manuf_pctPIB": man,
    },
    metadonnees=pd.DataFrame(meta),
    titre_classeur="AXE 3 — Composants du bonheur et sous-jacents économiques")

print("\nRécap Axe 3 :")
print("Espérance de vie 2023:", le[le.annee==2023].set_index('pays')['esperance_vie'].to_dict())
print("R&D pharma par zone 2021:\n", rd_z[rd_z.annee==2021].to_string(index=False))
print("Années R&D dispo:", sorted(rd_z.annee.unique()))
