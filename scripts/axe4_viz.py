"""AXE 4 — visualisations.
  1) Small multiples : fécondité, investissement (FBCF), défense, par pays (période longue)
  2) Soutenabilité budgétaire : dette publique + solde primaire
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config as C
import theme as T

A = C.DATA / "axe4"; OUT = C.VIZ / "axe4"
fec = pd.read_csv(A / "01_fecondite_1990_2023.csv")
fbcf = pd.read_csv(A / "02_fbcf_investissement_2000_2023.csv")
defe = pd.read_csv(A / "03_defense_2000_2023.csv")
dette = pd.read_csv(A / "04_dette_publique_2000_2024.csv")
pb = pd.read_csv(A / "05_solde_primaire_2000_2024.csv")

# Palette distincte pour 6 pays (lisibilité multi-courbes)
PAYS6 = ["USA", "FRA", "DEU", "JPN", "KOR", "CHN"]
COL = {"USA": "#9C2B2E", "FRA": "#2E5E8C", "DEU": "#2E7D5B",
       "JPN": "#6E5A8C", "KOR": "#C77B30", "CHN": "#C9A227"}

# ===========================================================================
# 1) SMALL MULTIPLES — fécondité / investissement / défense
# ===========================================================================
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.055,
    subplot_titles=("Fécondité (enfants par femme)",
                    "Investissement — FBCF (% du PIB)",
                    "Dépenses de défense (% du PIB)"))

def trace_panel(df, col_val, c, x0, x1, refs=None):
    for iso in PAYS6:
        s = df[df.iso3 == iso].sort_values("annee")
        fig.add_trace(go.Scatter(x=s["annee"], y=s[col_val], name=C.PAYS[iso],
            legendgroup=iso, showlegend=(c == 1), mode="lines",
            line=dict(color=COL[iso], width=2),
            hovertemplate=f"{C.PAYS[iso]} — %{{x}} : %{{y:.2f}}<extra></extra>"), row=1, col=c)
    fig.update_xaxes(range=[x0, x1], dtick=10, row=1, col=c)

trace_panel(fec, "fecondite", 1, 1990, 2023)
trace_panel(fbcf, "fbcf_pct_pib", 2, 2000, 2023)
trace_panel(defe, "defense_pct_pib", 3, 2000, 2023)
# lignes de repère
fig.add_hline(y=2.1, line=dict(color=C.COULEURS["accent"], width=1, dash="dot"), row=1, col=1)
fig.add_annotation(x=1996, y=2.22, text="seuil de remplacement (2,1)", showarrow=False,
                   font=dict(size=9, color=C.COULEURS["accent"]), row=1, col=1, xanchor="left")
fig.add_hline(y=2.0, line=dict(color=C.COULEURS["accent"], width=1, dash="dot"), row=1, col=3)
fig.add_annotation(x=2003, y=2.15, text="cible OTAN (2 %)", showarrow=False,
                   font=dict(size=9, color=C.COULEURS["accent"]), row=1, col=3, xanchor="left")

fig.update_yaxes(range=[0.5, 2.5], row=1, col=1)
fig.update_yaxes(range=[15, 45], row=1, col=2)
fig.update_yaxes(range=[0.5, 5], row=1, col=3)
fig.update_layout(template="tribune", width=980, height=480,
    paper_bgcolor=C.COULEURS["fond_web"], plot_bgcolor=C.COULEURS["fond_web"],
    legend=dict(orientation="h", y=-0.16, x=0.5, xanchor="center"),
    margin=dict(l=55, r=30, t=110, b=120))
T.finaliser(fig,
    titre="Trois arbitrages entre présent et avenir",
    soustitre="Faire des enfants, investir, se défendre : l'effort tourné vers le futur, par pays",
    source="Banque mondiale (fécondité, FBCF) ; SIPRI via Banque mondiale (défense). Extraction : 06/2026.",
    note="Lecture : les économies avancées combinent une fécondité bien sous le seuil de remplacement, un investissement modéré et (en Europe) un faible effort de défense ; la Chine surinvestit mais voit sa fécondité s'effondrer.",
    source_y=-0.24)
T.exporter(fig, str(OUT / "axe4_small_multiples"))

# ===========================================================================
# 2) SOUTENABILITÉ — dette publique + solde primaire
# ===========================================================================
fig2 = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
    subplot_titles=("Dette publique brute (% du PIB)",
                    "Solde primaire (% du PIB)"))
for iso in PAYS6:
    s = dette[dette.iso3 == iso].sort_values("annee")
    fig2.add_trace(go.Scatter(x=s["annee"], y=s["dette_pct_pib"], name=C.PAYS[iso],
        legendgroup=iso, showlegend=True, mode="lines", line=dict(color=COL[iso], width=2),
        hovertemplate=f"{C.PAYS[iso]} — %{{x}} : %{{y:.0f}} %% du PIB<extra></extra>"), row=1, col=1)
for iso in PAYS6:
    s = pb[pb.iso3 == iso].sort_values("annee")
    fig2.add_trace(go.Scatter(x=s["annee"], y=s["solde_primaire_pct_pib"], name=C.PAYS[iso],
        legendgroup=iso, showlegend=False, mode="lines", line=dict(color=COL[iso], width=2),
        hovertemplate=f"{C.PAYS[iso]} — %{{x}} : %{{y:.1f}} %% du PIB<extra></extra>"), row=1, col=2)
fig2.add_hline(y=0, line=dict(color=C.COULEURS["gris_texte"], width=1), row=1, col=2)
fig2.add_annotation(x=2003, y=0.6, text="équilibre primaire", showarrow=False,
                    font=dict(size=9, color=C.COULEURS["gris_texte"]), row=1, col=2, xanchor="left")
fig2.update_xaxes(range=[2000, 2024], dtick=6, row=1, col=1)
fig2.update_xaxes(range=[2000, 2024], dtick=6, row=1, col=2)
fig2.update_yaxes(title="% du PIB", row=1, col=1)
fig2.update_yaxes(title="% du PIB", row=1, col=2)
fig2.update_layout(template="tribune", width=900, height=500,
    paper_bgcolor=C.COULEURS["fond_web"], plot_bgcolor=C.COULEURS["fond_web"],
    legend=dict(orientation="h", y=-0.16, x=0.5, xanchor="center"),
    margin=dict(l=60, r=30, t=110, b=120))
T.finaliser(fig2,
    titre="La dette, capital emprunté au futur",
    soustitre="Dette publique et solde primaire : qui finance son bien-être présent par l'endettement ?",
    source="FMI — World Economic Outlook (dette brute GGXWDG_NGDP ; solde primaire). Extraction : 06/2026.",
    note="Lecture : France, États-Unis et Japon conjuguent dette élevée et déficits primaires persistants — le confort présent s'appuie en partie sur l'endettement (l'Italie, dans les données, partage ce profil).",
    source_y=-0.26)
T.exporter(fig2, str(OUT / "axe4_soutenabilite_dette"))

print("Axe 4 — visualisations exportées.")
