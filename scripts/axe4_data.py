"""
AXE 4 — Tensions entre bonheur individuel et prospérité collective : collecte.
  1) Taux de fécondité, 1990-2023                       [Banque mondiale]
  2) FBCF (investissement) en % du PIB, 2000-2023        [Banque mondiale]
  3) Dépenses de défense en % du PIB, 2000-2023          [Banque mondiale / SIPRI]
  4) Dette publique brute en % du PIB, 2000-2024         [FMI WEO]
  5) Solde primaire en % du PIB, 2000-2024               [FMI WEO]
"""
import numpy as np
import pandas as pd
import config as C
import sources as S
import livraison as L

A = C.DATA / "axe4"; A.mkdir(parents=True, exist_ok=True)
PAYS4 = ["USA","FRA","DEU","ITA","ESP","JPN","KOR","CHN"]
meta = []
def M(serie, source, url, unite, periode, notes):
    meta.append(dict(serie=serie, source=source, url=url, unite=unite, periode=periode,
                     date_extraction=C.DATE_EXTRACTION, notes=notes))

# 1) Fécondité
print("Fécondité…")
fec = S.wb("SP.DYN.TFRT.IN", PAYS4, 1990, 2023, serie="fecondite")
fec["pays"] = fec["iso3"].map(C.PAYS)
fec = fec[["iso3","pays","annee","valeur"]].rename(columns={"valeur":"fecondite"}).round({"fecondite":3})
L.ecrire_csv(fec, A / "01_fecondite_1990_2023.csv")
M("Taux de fécondité", "Banque mondiale — WDI (SP.DYN.TFRT.IN)",
  "https://data.worldbank.org/indicator/SP.DYN.TFRT.IN", "enfants par femme", "1990-2023",
  "Seuil de remplacement des générations ≈ 2,1.")

# 2) FBCF
print("FBCF…")
fbcf = S.wb("NE.GDI.FTOT.ZS", PAYS4, 2000, 2023, serie="FBCF")
fbcf["pays"] = fbcf["iso3"].map(C.PAYS)
fbcf = fbcf[["iso3","pays","annee","valeur"]].rename(columns={"valeur":"fbcf_pct_pib"}).round({"fbcf_pct_pib":2})
L.ecrire_csv(fbcf, A / "02_fbcf_investissement_2000_2023.csv")
M("Formation brute de capital fixe (investissement)", "Banque mondiale — WDI (NE.GDI.FTOT.ZS)",
  "https://data.worldbank.org/indicator/NE.GDI.FTOT.ZS", "% du PIB", "2000-2023",
  "Investissement en capital productif — proxy de l'effort tourné vers l'avenir.")

# 3) Défense
print("Défense…")
defe = S.wb("MS.MIL.XPND.GD.ZS", PAYS4, 2000, 2023, serie="defense")
defe["pays"] = defe["iso3"].map(C.PAYS)
defe = defe[["iso3","pays","annee","valeur"]].rename(columns={"valeur":"defense_pct_pib"}).round({"defense_pct_pib":3})
L.ecrire_csv(defe, A / "03_defense_2000_2023.csv")
M("Dépenses militaires", "Banque mondiale — WDI (MS.MIL.XPND.GD.ZS ; source SIPRI)",
  "https://data.worldbank.org/indicator/MS.MIL.XPND.GD.ZS", "% du PIB", "2000-2023",
  "Effort de défense — bien collectif différé. Cible OTAN : 2 % du PIB.")

# 4) Dette publique (FMI)
print("Dette publique (FMI)…")
dette = S.imf("GGXWDG_NGDP", PAYS4, serie="dette_publique")
dette = dette[(dette.annee >= 2000) & (dette.annee <= 2024)].copy()
dette["pays"] = dette["entity"].map(C.PAYS)
dette = dette[["entity","pays","annee","valeur"]].rename(columns={"entity":"iso3","valeur":"dette_pct_pib"}).round({"dette_pct_pib":2})
L.ecrire_csv(dette, A / "04_dette_publique_2000_2024.csv")
M("Dette publique brute des administrations", "FMI — World Economic Outlook (GGXWDG_NGDP)",
  "https://www.imf.org/external/datamapper/GGXWDG_NGDP", "% du PIB", "2000-2024",
  "Dette publique brute (general government gross debt).")

# 5) Solde primaire (FMI)
print("Solde primaire (FMI)…")
pb = S.imf("pb", PAYS4, serie="solde_primaire")
pb = pb[(pb.annee >= 2000) & (pb.annee <= 2024)].copy()
pb["pays"] = pb["entity"].map(C.PAYS)
pb = pb[["entity","pays","annee","valeur"]].rename(columns={"entity":"iso3","valeur":"solde_primaire_pct_pib"}).round({"solde_primaire_pct_pib":2})
L.ecrire_csv(pb, A / "05_solde_primaire_2000_2024.csv")
M("Solde primaire des administrations publiques", "FMI — World Economic Outlook (solde primaire, % PIB)",
  "https://www.imf.org/external/datamapper/pb", "% du PIB", "2000-2024",
  "Solde budgétaire hors charge d'intérêts. Négatif = déficit primaire.")

L.construire_xlsx(A / "axe4_arbitrages.xlsx",
    feuilles={"Fecondite": fec, "FBCF_investissement": fbcf, "Defense": defe,
              "Dette_publique": dette, "Solde_primaire": pb},
    metadonnees=pd.DataFrame(meta),
    titre_classeur="AXE 4 — Tensions bonheur individuel / prospérité collective")

print("\nRécap Axe 4 :")
print("Fécondité 2023:", {C.PAYS[i]:v for i,v in fec[fec.annee==2023].set_index('iso3').fecondite.items()})
print("Défense 2023:", {C.PAYS[i]:round(v,1) for i,v in defe[defe.annee==2023].set_index('iso3').defense_pct_pib.items()})
print("Dette 2024:", {C.PAYS[i]:round(v) for i,v in dette[dette.annee==2024].set_index('iso3').dette_pct_pib.items()})
print("FBCF 2023:", {C.PAYS[i]:round(v,1) for i,v in fbcf[fbcf.annee==2023].set_index('iso3').fbcf_pct_pib.items()})
