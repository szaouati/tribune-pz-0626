"""AXE 3 — visualisations.
  1) Combiné : R&D pharma (barres, par zone) vs espérance de vie (courbes), 2000-2023
  2) Origine des nouvelles molécules (2024) — déclin européen
  3) (complément) PM2.5 vs désindustrialisation
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config as C
import theme as T

A = C.DATA / "axe3"; OUT = C.VIZ / "axe3"
le  = pd.read_csv(A / "01_esperance_vie_1990_2023.csv")
rdz = pd.read_csv(A / "02_rd_pharma_zones_2000_2023.csv")
orig = pd.read_csv(A / "05_origine_nouvelles_molecules_2024.csv")
pm  = pd.read_csv(A / "04_pm25_qualite_air.csv")
man = pd.read_csv(A / "04b_industrie_manufacturiere_pct_pib.csv")

ZCOL = {"États-Unis": "#9C2B2E", "Europe (UE + AELE)": "#2E5E8C",
        "Japon": "#6E5A8C", "Chine": "#D9A441"}

# ===========================================================================
# 1) COMBINÉ — R&D pharma (barres) + espérance de vie (courbes)
# ===========================================================================
fig = make_subplots(specs=[[{"secondary_y": True}]])
snaps = [2000, 2004, 2008, 2012, 2016, 2020, 2023]
rd_s = rdz[rdz.annee.isin(snaps)]
for zone, coul in ZCOL.items():
    s = rd_s[rd_s.zone == zone]
    fig.add_trace(go.Bar(x=s["annee"], y=s["valeur"], name=zone, marker_color=coul,
        opacity=0.92, hovertemplate=f"{zone} — R&D %{{x}} : %{{y:.1f}} Md$<extra></extra>"),
        secondary_y=False)
# Espérance de vie (courbes) — représentants de zone ; étiquetées en bout de ligne
LE_REP = {"JPN": ("Japon", "#6E5A8C"), "FRA": ("Europe (France)", "#2E5E8C"),
          "USA": ("États-Unis", "#9C2B2E"), "CHN": ("Chine", "#D9A441")}
for iso, (lab, coul) in LE_REP.items():
    s = le[(le.iso3 == iso) & (le.annee >= 2000)].sort_values("annee")
    fig.add_trace(go.Scatter(x=s["annee"], y=s["esperance_vie"], showlegend=False,
        mode="lines", line=dict(color=coul, width=2.6),
        hovertemplate=f"{lab} — %{{x}} : %{{y:.1f}} ans<extra></extra>"), secondary_y=True)
    yv = s[s.annee == 2023]["esperance_vie"].values[0]
    fig.add_annotation(x=2023.4, y=yv, yref="y2", text=lab, showarrow=False, xanchor="left",
                       font=dict(size=10, color=coul))

fig.update_layout(template="tribune", barmode="group", width=860, height=580,
    paper_bgcolor=C.COULEURS["fond_web"], plot_bgcolor=C.COULEURS["fond_web"],
    legend=dict(orientation="h", y=-0.17, x=0.5, xanchor="center", font=dict(size=11),
                title=dict(text="R&D pharmaceutique (barres) :  ", font=dict(size=11))),
    margin=dict(l=72, r=140, t=110, b=150))
fig.update_xaxes(title="", dtick=4, tickvals=snaps)
fig.update_yaxes(title="R&D pharmaceutique des entreprises (Md$ PPA)", secondary_y=False,
                 showgrid=True, gridcolor=C.COULEURS["gris_grille"], range=[0, 140])
fig.update_yaxes(title="Espérance de vie à la naissance (années) — courbes", secondary_y=True,
                 range=[70, 86], showgrid=False)
fig.add_annotation(x=2001.5, y=134, yref="y", xanchor="left",
                   text="<b>Les États-Unis financent l'essentiel de la R&D pharmaceutique…</b>",
                   showarrow=False, font=dict(size=11, color=C.COULEURS["USA"]), align="left")
fig.add_annotation(x=2012, y=78.6, yref="y2", text="…mais y vivent le moins longtemps",
                   showarrow=True, arrowhead=0, arrowwidth=1, arrowcolor=C.COULEURS["gris_texte"],
                   ax=0, ay=-34, font=dict(size=11, color=C.COULEURS["USA"]),
                   bgcolor="rgba(251,249,245,0.92)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3)
T.finaliser(fig,
    titre="Qui paie l'innovation, qui en profite ?",
    soustitre="R&D pharmaceutique des entreprises (barres) et espérance de vie (courbes), par zone, 2000-2023",
    source="OCDE, base ANBERD (R&D, industrie C21, Md$ PPA) ; Banque mondiale (espérance de vie). Extraction : 06/2026.",
    note="Lecture : la R&D pharmaceutique américaine dépasse de loin celle de l'Europe et du Japon ; l'espérance de vie américaine reste pourtant la plus basse des grandes économies avancées.",
    source_y=-0.34)
T.exporter(fig, str(OUT / "axe3_rd_esperance_vie"))

# ===========================================================================
# 2) ORIGINE DES NOUVELLES MOLÉCULES (2024)
# ===========================================================================
fig2 = T.figure_base(largeur=740, hauteur=460)
COURT = {"Chine (Chine + Hong Kong)": "Chine (+ Hong Kong)", "États-Unis": "États-Unis",
         "Europe": "Europe", "Reste du monde": "Reste du monde"}
o = orig.sort_values("nb_molecules_2024", ascending=True).copy()
o["lab"] = o["zone"].map(COURT)
cols = {"Chine (Chine + Hong Kong)": "#D9A441", "États-Unis": "#9C2B2E",
        "Europe": "#2E5E8C", "Reste du monde": "#BBB3A8"}
fig2.add_trace(go.Bar(y=o["lab"], x=o["nb_molecules_2024"], orientation="h",
    marker_color=[cols[z] for z in o["zone"]],
    text=[f"{n} molécules ({p:.0f} %)" for n, p in zip(o["nb_molecules_2024"], o["part_pct"])],
    textposition="outside", cliponaxis=False,
    hovertemplate="%{y} : %{x} molécules<extra></extra>"))
fig2.update_xaxes(title="Nombre de nouvelles substances actives (2024, sur 81 au total)", range=[0, 34])
fig2.update_yaxes(title="")
fig2.update_layout(margin=dict(l=140, r=40, t=90, b=85))
fig2.add_annotation(x=18, y="Europe", text="L'Europe, n°1 mondial<br>des originateurs en 2000,<br>est 3e en 2024",
                    showarrow=True, arrowhead=0, arrowwidth=1, arrowcolor=C.COULEURS["gris_texte"],
                    ax=70, ay=0, font=dict(size=10.5, color=C.COULEURS["FRA"]),
                    bgcolor="rgba(251,249,245,0.9)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3)
T.finaliser(fig2,
    titre="L'Europe déclassée dans l'origine des nouveaux médicaments",
    soustitre="Origine géographique des nouvelles substances actives lancées dans le monde en 2024",
    source="EFPIA, The Pharmaceutical Industry in Figures 2025 (selon la nationalité de la société mère). Extraction : 06/2026.",
    note="Lecture : la Chine (28) et les États-Unis (25) devancent désormais l'Europe (18) comme berceaux des nouveaux médicaments.")
T.exporter(fig2, str(OUT / "axe3_origine_molecules"))

# ===========================================================================
# 3) COMPLÉMENT — PM2.5 vs part de l'industrie manufacturière
# ===========================================================================
fig3 = T.figure_base(largeur=760, hauteur=500)
for iso in ["USA", "DEU", "CHN", "FRA"]:
    p = pm[pm.iso3 == iso].sort_values("annee")
    fig3.add_trace(go.Scatter(x=p["annee"], y=p["pm25_ug_m3"], name=C.PAYS[iso],
        mode="lines", line=dict(color=C.couleur(iso), width=2.4),
        hovertemplate=f"{C.PAYS[iso]} — %{{x}} : %{{y:.1f}} µg/m³<extra></extra>"))
fig3.add_hline(y=5, line=dict(color=C.COULEURS["accent"], width=1, dash="dot"))
fig3.add_annotation(x=1992, y=5.6, text="Seuil OMS recommandé : 5 µg/m³", showarrow=False,
                    font=dict(size=10, color=C.COULEURS["accent"]), xanchor="left")
fig3.update_xaxes(title="", dtick=5, range=[1990, 2020])
fig3.update_yaxes(title="Exposition moyenne aux PM2.5 (µg/m³)")
fig3.update_layout(legend=dict(orientation="h", y=-0.13, x=0), margin=dict(l=70, r=40, t=90, b=120))
T.finaliser(fig3,
    titre="Qualité de l'air : l'avantage des économies désindustrialisées",
    soustitre="Exposition moyenne de la population aux particules fines PM2.5, 1990-2020",
    source="Banque mondiale / OMS (EN.ATM.PM25.MC.M3). Extraction : 06/2026.",
    note="Lecture : la Chine, atelier industriel du monde, respire un air bien plus pollué que les économies de services occidentales — un coût du bien-être délocalisé.",
    source_y=-0.24)
T.exporter(fig3, str(OUT / "axe3_pm25_air"))

print("Axe 3 — visualisations exportées.")
