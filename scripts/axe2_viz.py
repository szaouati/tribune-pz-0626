"""AXE 2 — visualisations.
  1) Aires empilées : part du PIB mondial par zone, 1990-2024
  2) Double panneau : écart de PIB/hab USA vs Europe + scores Better Life Index
  3) (complément) Heures travaillées annuelles, 2000-2023
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config as C
import theme as T

A = C.DATA / "axe2"; OUT = C.VIZ / "axe2"
parts = pd.read_csv(A / "01_part_pib_mondial_zones_1990_2024.csv")
ecart = pd.read_csv(A / "02_ecart_pib_hab_us_europe_2000_2024.csv")
bli = pd.read_csv(A / "03_bli_scores_4dimensions.csv")
heures = pd.read_csv(A / "04_heures_travaillees_2000_2023.csv")

# ===========================================================================
# 1) AIRES EMPILÉES — part du PIB mondial
# ===========================================================================
fig = T.figure_base(largeur=760, hauteur=520)
# couleurs distinctes pour ce graphe (4 zones bien séparées)
ZCOL = {"Union européenne (27)": "#2E5E8C", "États-Unis": "#9C2B2E",
        "Chine": "#D9A441", "Reste du monde": "#C9C3B8"}
ordre = list(ZCOL.items())  # bas -> haut : UE, USA, Chine, Reste
for nom, coul in ordre:
    fig.add_trace(go.Scatter(
        x=parts["annee"], y=parts[nom], name=nom, mode="lines",
        line=dict(width=0.5, color=coul), stackgroup="one", fillcolor=coul,
        showlegend=False,
        hovertemplate=f"{nom} : %{{y:.1f}} %% (%{{x}})<extra></extra>"))
# Étiquetage direct des bandes (au point médian de chaque bande en 2024)
p24 = parts[parts.annee == 2024].iloc[0]
cum = 0
for nom, coul in ordre:
    val = p24[nom]
    mid = cum + val / 2
    clair = nom in ("Chine", "Reste du monde")
    fig.add_annotation(x=2023.3, y=mid, text=f"<b>{nom}</b><br>{val:.0f} %",
                       showarrow=False, xanchor="right",
                       font=dict(size=11, color=C.COULEURS["encre"] if clair else "white"))
    cum += val
ue90, ue24 = parts.loc[parts.annee==1990, "Union européenne (27)"].values[0], p24["Union européenne (27)"]
fig.add_annotation(x=1991, y=ue90/2, text=f"UE-27 : {ue90:.0f} % en 1990…",
                   showarrow=False, font=dict(size=11, color="white"), xanchor="left")
fig.add_vline(x=2008, line=dict(color="rgba(255,255,255,0.45)", width=1, dash="dot"))
fig.add_annotation(x=2008, y=100, text="2008", showarrow=False,
                   font=dict(size=10, color=C.COULEURS["gris_texte"]), yref="y", yshift=8)
fig.update_xaxes(title="", dtick=5, range=[1990, 2024])
fig.update_yaxes(title="Part du PIB mondial courant (%)", range=[0, 100], ticksuffix=" %")
T.finaliser(fig,
    titre="Le poids économique relatif de l'Europe recule",
    soustitre="Répartition du PIB mondial (en dollars courants), 1990-2024",
    source="Banque mondiale, World Development Indicators (PIB courant $US). Extraction : 06/2026.",
    note="Lecture : la part de l'UE-27 dans le PIB mondial est passée d'environ un quart à moins d'un cinquième en trois décennies, dépassée par la Chine.")
T.exporter(fig, str(OUT / "axe2_part_pib_mondial"))

# ===========================================================================
# 2) DOUBLE PANNEAU — écart PIB/hab + scores BLI
# ===========================================================================
ordre_pays = ["USA", "DEU", "FRA", "ITA", "ESP"]
e24 = ecart[ecart.annee == 2024].iloc[0]
pib_vals = {"USA": e24["PIB/hab États-Unis"]}
for p in ["FRA","DEU","ITA","ESP"]:
    pib_vals[p] = e24[f"PIB/hab {C.PAYS[p]}"]

fig2 = make_subplots(rows=1, cols=2, horizontal_spacing=0.14,
    subplot_titles=("PIB par habitant en PPA (2024)",
                    "Bien-être : scores Better Life Index (0-10)"))
# Panneau gauche : PIB/hab barres
noms = [C.PAYS[p] for p in ordre_pays]
vals = [pib_vals[p] for p in ordre_pays]
cols = [C.couleur(p) for p in ordre_pays]
fig2.add_trace(go.Bar(x=noms, y=vals, marker_color=cols, showlegend=False,
    text=[f"{v/1000:.0f}k$" for v in vals], textposition="outside",
    hovertemplate="%{x} : %{y:,.0f} $<extra></extra>"), row=1, col=1)
# annotation écart US/France
fig2.add_annotation(x="France", y=pib_vals["FRA"], text=f"−{e24['Écart US/France (%)']:.0f} % vs USA",
                    showarrow=True, arrowhead=0, ax=0, ay=-30, font=dict(size=10, color=C.COULEURS["encre"]),
                    bgcolor="rgba(251,249,245,0.9)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1,
                    row=1, col=1)
# Panneau droit : BLI grouped bars
bli_o = bli.set_index("iso3").loc[ordre_pays]
dims = ["Satisfaction de vie", "Équilibre travail-vie", "Logement", "Sécurité"]
dim_cols = [C.COULEURS["FRA"], C.COULEURS["KOR"], C.COULEURS["DEU"], C.COULEURS["ITA"]]
for dim, c in zip(dims, dim_cols):
    fig2.add_trace(go.Bar(name=dim, x=[C.PAYS[p] for p in ordre_pays], y=bli_o[dim].values,
        marker_color=c, hovertemplate=f"{dim} — %{{x}} : %{{y:.1f}}/10<extra></extra>"), row=1, col=2)
fig2.update_yaxes(title="$ PPA", row=1, col=1, tickformat=",.0f")
fig2.update_yaxes(title="score 0-10", range=[0, 10], row=1, col=2)
fig2.update_layout(barmode="group", height=540, width=860,
    legend=dict(orientation="h", y=-0.14, x=0.5, xanchor="center"),
    template="tribune", paper_bgcolor=C.COULEURS["fond_web"], plot_bgcolor=C.COULEURS["fond_web"],
    margin=dict(l=70, r=40, t=110, b=150))
T.finaliser(fig2,
    titre="L'Europe décroche en richesse, pas en qualité de vie",
    soustitre="À gauche : revenu par habitant (les États-Unis loin devant). À droite : scores de bien-être (l'Europe rivalise ou dépasse)",
    source="Banque mondiale (PIB/hab PPA) ; OCDE Better Life Index (scores reconstitués, méthode min-max). Extraction : 06/2026.",
    note="Lecture : malgré un PIB/habitant inférieur de 30 à 45 %, les pays européens égalent ou surpassent les États-Unis sur l'équilibre travail-vie et la sécurité.",
    source_y=-0.26)
T.exporter(fig2, str(OUT / "axe2_ecart_pib_bli"))

# ===========================================================================
# 3) COMPLÉMENT — heures travaillées annuelles
# ===========================================================================
fig3 = T.figure_base(largeur=760, hauteur=480)
for p in ordre_pays:
    s = heures[heures.iso3 == p].sort_values("annee")
    fig3.add_trace(go.Scatter(x=s["annee"], y=s["heures_annuelles"], name=C.PAYS[p],
        mode="lines", line=dict(width=2.6 if p == "USA" else 2, color=C.couleur(p)),
        hovertemplate=f"{C.PAYS[p]} : %{{y:,.0f}} h (%{{x}})<extra></extra>"))
fig3.update_xaxes(title="", dtick=5, range=[2000, 2023])
fig3.update_yaxes(title="Heures travaillées par an et par travailleur")
fig3.update_layout(legend=dict(orientation="h", y=-0.14, x=0))
h23 = heures[heures.annee == 2023].set_index("iso3")["heures_annuelles"]
fig3.add_annotation(x=2023, y=h23.get("USA"), text="États-Unis", showarrow=False,
                    font=dict(size=10, color=C.COULEURS["USA"]), xanchor="left", xshift=5)
fig3.add_annotation(x=2023, y=h23.get("DEU"), text="Allemagne", showarrow=False,
                    font=dict(size=10, color=C.COULEURS["DEU"]), xanchor="left", xshift=5)
T.finaliser(fig3,
    titre="Les Européens travaillent moins d'heures",
    soustitre="Durée annuelle moyenne du travail par personne en emploi, 2000-2023",
    source="OCDE (Average annual hours actually worked), via Our World in Data. Extraction : 06/2026.",
    note="Lecture : un Allemand travaille ~450 heures de moins par an qu'un Américain — soit un arbitrage assumé en faveur du temps libre.")
T.exporter(fig3, str(OUT / "axe2_heures_travaillees"))

print("Axe 2 — visualisations exportées.")
