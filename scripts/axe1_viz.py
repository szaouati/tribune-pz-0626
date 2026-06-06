"""AXE 1 — visualisations.
  1) Nuage de bulles : bonheur (Y) vs PIB/hab PPA (X), taille = population (2024)
  2) Double axe : paradoxe d'Easterlin, USA 1970-2024
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import config as C
import theme as T

A = C.DATA / "axe1"
OUT = C.VIZ / "axe1"

whr = pd.read_csv(A / "01_whr_score_bonheur_2012_2024.csv")
gdp = pd.read_csv(A / "02_pib_hab_ppa_2012_2024.csv")
pop = pd.read_csv(A / "03_population_2012_2024.csv")
gdp_us = pd.read_csv(A / "04_pib_reel_hab_us_1970_2024.csv")
gss = pd.read_csv(A / "05_gss_bonheur_us_1972_2024.csv")

# ===========================================================================
# 1) NUAGE DE BULLES — 2024 (Bhoutan : dernière année dispo = 2018)
# ===========================================================================
def derniere(df, iso, col, an_max=2024):
    s = df[(df.iso3 == iso) & (df.annee <= an_max)].sort_values("annee")
    return (s.iloc[-1][col], int(s.iloc[-1]["annee"])) if len(s) else (np.nan, None)

rows = []
for iso in C.PAYS_AXE1:                       # sélection conforme au brief (sans IT/ES)
    nom = C.PAYS[iso]
    b, ba = derniere(whr, iso, "score_bonheur")
    g, ga = derniere(gdp, iso, "pib_hab_ppa")
    p, pa = derniere(pop, iso, "population")
    if np.isnan(b) or np.isnan(g):
        continue
    rows.append(dict(iso3=iso, pays=nom, bonheur=b, an_b=ba, pib=g, an_g=ga, pop=p))
bub = pd.DataFrame(rows)
bub["est_2024"] = bub["an_b"] == 2024

fig = T.figure_base(largeur=760, hauteur=560)
# tailles de bulles (∝ racine de la population)
smax = 72; smin = 16
pmin, pmax = bub["pop"].min(), bub["pop"].max()
bub["taille"] = smin + (np.sqrt(bub["pop"]) - np.sqrt(pmin)) / (np.sqrt(pmax) - np.sqrt(pmin)) * (smax - smin)
# placement des étiquettes pour limiter les recouvrements
POS = {"FIN": "top center", "SWE": "middle left", "DNK": "top center",
       "NOR": "middle right", "ISL": "bottom center", "DEU": "middle left",
       "USA": "top center", "FRA": "bottom center", "KOR": "bottom center",
       "JPN": "middle left", "CHN": "middle center", "BTN": "middle right"}

for _, r in bub.iterrows():
    coul = C.couleur(r.iso3)
    daté = "" if r.est_2024 else f" ({r.an_b})"
    pos = POS.get(r.iso3, "top center")
    dedans = pos == "middle center"
    fig.add_trace(go.Scatter(
        x=[r.pib], y=[r.bonheur], mode="markers+text",
        marker=dict(size=r.taille, color=coul, opacity=0.80,
                    line=dict(width=1.3, color="white")),
        text=[f"{r.pays}{daté}"], textposition=pos,
        textfont=dict(size=11, color="white" if dedans else C.COULEURS["encre"]),
        cliponaxis=False, name=r.pays, showlegend=False,
        hovertemplate=(f"<b>{r.pays}</b><br>PIB/hab PPA : %{{x:,.0f}} $ ({r.an_g})"
                       f"<br>Bonheur : %{{y:.2f}}/10 ({r.an_b})"
                       f"<br>Population : {r['pop']/1e6:,.1f} M<extra></extra>")))

# Ligne de tendance (régression log)
m = bub[bub.est_2024]
coef = np.polyfit(np.log(m["pib"]), m["bonheur"], 1)
xs = np.linspace(bub["pib"].min()*0.9, bub["pib"].max()*1.05, 50)
fig.add_trace(go.Scatter(x=xs, y=coef[0]*np.log(xs)+coef[1], mode="lines",
              line=dict(color=C.COULEURS["gris_texte"], width=1.2, dash="dot"),
              name="Tendance (log)", hoverinfo="skip", showlegend=False))

fig.update_xaxes(title="PIB par habitant en PPA ($ internationaux, 2024 — échelle log)", type="log",
                 tickvals=[10000,20000,40000,80000],
                 ticktext=["10 000","20 000","40 000","80 000"])
fig.update_yaxes(title="Score de bonheur (échelle de Cantril, 0-10)", range=[3.8, 8.2])
# Annotations (axe X log → coordonnées en log10)
fig.add_annotation(x=np.log10(m[m.iso3=='USA'].pib.values[0]), y=m[m.iso3=='USA'].bonheur.values[0],
                   text="États-Unis : revenu très élevé,<br>bonheur sous les pays nordiques",
                   xref="x", yref="y", showarrow=True, arrowhead=0, arrowwidth=1,
                   arrowcolor=C.COULEURS["gris_texte"], ax=-20, ay=60,
                   font=dict(size=10, color=C.COULEURS["encre"]), bgcolor="rgba(251,249,245,0.85)",
                   bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3, align="left")
fig.add_annotation(x=np.log10(bub[bub.iso3=='BTN'].pib.values[0]), y=bub[bub.iso3=='BTN'].bonheur.values[0],
                   text="Bhoutan : sorti du<br>panel mondial après 2018", xref="x", yref="y",
                   showarrow=True, arrowhead=0, arrowwidth=1, arrowcolor=C.COULEURS["gris_texte"],
                   ax=55, ay=-30, font=dict(size=10, color=C.COULEURS["encre"]),
                   bgcolor="rgba(251,249,245,0.85)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3)
T.finaliser(fig,
    titre="Plus riche, vraiment plus heureux ?",
    soustitre="Bonheur déclaré et PIB par habitant — taille des bulles ∝ population (2024 ; Bhoutan : 2018)",
    source="World Happiness Report / Gallup ; Banque mondiale (PIB PPA, population). Extraction : 06/2026.",
    note="Lecture : au-delà d'un certain seuil de richesse, le supplément de PIB n'achète qu'un faible supplément de bonheur déclaré.")
T.exporter(fig, str(OUT / "axe1_bulles_bonheur_pib"))

# ===========================================================================
# 2) PARADOXE D'EASTERLIN — USA, double axe
# ===========================================================================
fig2 = T.figure_base(largeur=760, hauteur=520)
fig2.add_trace(go.Scatter(
    x=gdp_us["annee"], y=gdp_us["pib_reel_hab_usd2015"], name="PIB réel / habitant",
    mode="lines", line=dict(color=C.COULEURS["USA"], width=3), yaxis="y",
    hovertemplate="%{x} : %{y:,.0f} $ (constants 2015)<extra>PIB réel/hab</extra>"))
fig2.add_trace(go.Scatter(
    x=gss["year"], y=gss["pct_very_happy"], name="« Très heureux » (GSS)",
    mode="lines+markers", line=dict(color=C.COULEURS["FRA"], width=2.4),
    marker=dict(size=5), yaxis="y2",
    hovertemplate="%{x} : %{y:.1f} %% « very happy »<extra>Bonheur déclaré</extra>"))

fig2.update_layout(
    yaxis=dict(title=dict(text="PIB réel par habitant ($ constants 2015)", font=dict(color=C.COULEURS["USA"])),
               tickfont=dict(color=C.COULEURS["USA"]), tickformat=",.0f"),
    yaxis2=dict(title=dict(text="Part se déclarant « très heureux » (%)", font=dict(color=C.COULEURS["FRA"])),
                tickfont=dict(color=C.COULEURS["FRA"]), overlaying="y", side="right",
                range=[0, 45], showgrid=False),
    legend=dict(orientation="h", y=1.02, x=0, yanchor="bottom"),
    margin=dict(l=80, r=80, t=110, b=85),
)
fig2.update_xaxes(title="", dtick=10, range=[1969, 2025])
T.annoter(fig2, 2008, gdp_us[gdp_us.annee==2008]["pib_reel_hab_usd2015"].values[0],
          "2008 : crise<br>financière", ax=-5, ay=-40)
fig2.add_annotation(x=2021, y=gss[gss.year==2021]["pct_very_happy"].values[0], yref="y2",
                    text="2021 : COVID +<br>refonte du protocole GSS", showarrow=True, arrowhead=0,
                    arrowwidth=1, arrowcolor=C.COULEURS["gris_texte"], ax=-30, ay=35,
                    font=dict(size=10, color=C.COULEURS["encre"]), bgcolor="rgba(251,249,245,0.85)",
                    bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3)
fig2.add_annotation(x=1990, y=33, yref="y2", text="Bonheur ~ stable<br>(≈ 30-36 %)", showarrow=False,
                    font=dict(size=11, color=C.COULEURS["FRA"]))
T.finaliser(fig2,
    titre="Le paradoxe d'Easterlin aux États-Unis",
    soustitre="Le revenu réel a plus que doublé depuis 1972 ; la part des Américains « très heureux » n'a pas progressé",
    source="Banque mondiale (PIB réel/hab, $2015) ; General Social Survey, NORC (var. HAPPY, pondérée). Extraction : 06/2026.",
    note="Lecture : la croissance économique de long terme ne se traduit pas mécaniquement en hausse du bien-être subjectif moyen.")
T.exporter(fig2, str(OUT / "axe1_easterlin_pib_bonheur"))

print("Axe 1 — visualisations exportées.")
