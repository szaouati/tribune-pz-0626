"""AXE 3 — addendum : origine géographique des nouvelles molécules + reconstruction Excel."""
import pandas as pd
import config as C
import livraison as L

A = C.DATA / "axe3"

# Origine des nouvelles substances actives lancées pour la 1re fois sur le marché mondial, 2024
# Source : EFPIA, The Pharmaceutical Industry in Figures 2025 (selon la nationalité de la société mère).
origine = pd.DataFrame([
    {"zone": "Chine (Chine + Hong Kong)", "nb_molecules_2024": 28},
    {"zone": "États-Unis", "nb_molecules_2024": 25},
    {"zone": "Europe", "nb_molecules_2024": 18},
    {"zone": "Reste du monde", "nb_molecules_2024": 10},
])
total = origine["nb_molecules_2024"].sum()  # = 81
origine["part_pct"] = (origine["nb_molecules_2024"] / total * 100).round(1)
L.ecrire_csv(origine, A / "05_origine_nouvelles_molecules_2024.csv")

# Reconstruction de l'Excel avec toutes les feuilles + la nouvelle
le  = pd.read_csv(A / "01_esperance_vie_1990_2023.csv")
rdz = pd.read_csv(A / "02_rd_pharma_zones_2000_2023.csv")
rdw = pd.read_csv(A / "02b_rd_pharma_zones_large.csv")
sh  = pd.read_csv(A / "03_depenses_sante_publique_2000_2023.csv")
pm  = pd.read_csv(A / "04_pm25_qualite_air.csv")
man = pd.read_csv(A / "04b_industrie_manufacturiere_pct_pib.csv")

meta = pd.DataFrame([
 dict(serie="Espérance de vie à la naissance",
      source="Banque mondiale — WDI (SP.DYN.LE00.IN ; OMS/ONU)",
      url="https://data.worldbank.org/indicator/SP.DYN.LE00.IN",
      unite="années", periode="1990-2023", date_extraction=C.DATE_EXTRACTION, notes="Total (H+F)."),
 dict(serie="R&D pharmaceutique des entreprises (industrie C21), par zone",
      source="OCDE — base ANBERD (ISIC Rév.4 div. 21)",
      url="https://data-explorer.oecd.org (DSD_ANBERD@DF_ANBERDi4)",
      unite="milliards USD PPA, prix courants", periode="2000-2023", date_extraction=C.DATE_EXTRACTION,
      notes="Europe = UE-27 (hors CYP/LUX/MLT) + CHE/NOR/ISL. RU non couvert par ANBERD (Europe légèrement sous-estimée)."),
 dict(serie="Dépenses publiques de santé",
      source="Banque mondiale — WDI (SH.XPD.GHED.GD.ZS ; OMS GHED)",
      url="https://data.worldbank.org/indicator/SH.XPD.GHED.GD.ZS",
      unite="% du PIB", periode="2000-2023", date_extraction=C.DATE_EXTRACTION,
      notes="Dépenses courantes de santé des administrations publiques."),
 dict(serie="Qualité de l'air — PM2.5 (exposition moyenne)",
      source="Banque mondiale — WDI (EN.ATM.PM25.MC.M3 ; OMS)",
      url="https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3",
      unite="µg/m³", periode="1990-2020", date_extraction=C.DATE_EXTRACTION,
      notes="Disponible jusqu'à 2020. À mettre en regard de la part de l'industrie manufacturière."),
 dict(serie="Industrie manufacturière (valeur ajoutée)",
      source="Banque mondiale — WDI (NV.IND.MANF.ZS)",
      url="https://data.worldbank.org/indicator/NV.IND.MANF.ZS",
      unite="% du PIB", periode="2000-2023", date_extraction=C.DATE_EXTRACTION,
      notes="Indicateur de (dés)industrialisation."),
 dict(serie="Origine géographique des nouvelles substances actives (2024)",
      source="EFPIA — The Pharmaceutical Industry in Figures 2025",
      url="https://www.efpia.eu/media/uj0popel/the-pharmaceutical-industry-in-figures-2025.pdf",
      unite="nombre / % (sur 81 molécules)", periode="2024", date_extraction=C.DATE_EXTRACTION,
      notes="Selon la nationalité de la société mère. L'Europe, n°1 mondial des originateurs en 2000, est 3e en 2024."),
])

L.construire_xlsx(A / "axe3_composants_bonheur.xlsx",
    feuilles={
        "Esperance_vie": le,
        "RD_pharma_zones (long)": rdz,
        "RD_pharma_zones (large)": rdw,
        "Depenses_sante_publique": sh,
        "Qualite_air_PM25": pm,
        "Industrie_manuf_pctPIB": man,
        "Origine_molecules_2024": origine,
    },
    metadonnees=meta,
    titre_classeur="AXE 3 — Composants du bonheur et sous-jacents économiques")
print("Origine molécules 2024 :")
print(origine.to_string(index=False))
