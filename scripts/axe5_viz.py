"""AXE 5 — visualisations : le coût du territoire (France / Allemagne / Pays-Bas).
  1) Le décor : densité + superficie (un territoire vaste et peu dense)
  2) Le maillage de proximité : communes, écoles, policiers par habitant
  3) Le coût : dépense publique totale (% PIB) + éducation & sécurité
  4) La diversité du territoire : dispersion des densités régionales (NUTS3)
  5) Le test causal interne : densité × maillage par habitant, 96 départements français
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config as C
import theme as T

A = C.DATA / "axe5"; OUT = C.VIZ / "axe5"
df1 = pd.read_csv(A / "01_densite_superficie_population.csv")
df2 = pd.read_csv(A / "02_densite_regionale_nuts3.csv")
df3 = pd.read_csv(A / "03_communes_fragmentation.csv")
df4 = pd.read_csv(A / "04_depense_publique_cofog.csv")
df5 = pd.read_csv(A / "05_maillage_ecoles_police.csv")
df6 = pd.read_csv(A / "06_gradient_departements_fr.csv")

ISO = ["FRA", "DEU", "NLD"]
NOMS = [C.PAYS[i] for i in ISO]
COLS = [C.couleur(i) for i in ISO]
CREME = C.COULEURS["fond_web"]

def fr(v, dec=0):
    """Format français : espace pour les milliers, virgule décimale."""
    s = f"{v:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s

def cadre(fig, w, h, b=120, t=110, l=60, r=30):
    fig.update_layout(template="tribune", width=w, height=h,
        paper_bgcolor=CREME, plot_bgcolor=CREME,
        margin=dict(l=l, r=r, t=t, b=b))

# ===========================================================================
# 1) LE DÉCOR — densité + superficie
# ===========================================================================
d = df1.set_index("iso3")
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.18,
    subplot_titles=("Densité de population (hab/km²)", "Superficie (milliers de km²)"))
fig.add_trace(go.Bar(x=NOMS, y=[d.loc[i, "densite_hab_km2"] for i in ISO],
    marker_color=COLS, showlegend=False, width=0.6,
    text=[fr(d.loc[i, "densite_hab_km2"]) for i in ISO], textposition="outside",
    hovertemplate="%{x} : %{y:.0f} hab/km²<extra></extra>"), row=1, col=1)
fig.add_trace(go.Bar(x=NOMS, y=[d.loc[i, "superficie_km2"] / 1000 for i in ISO],
    marker_color=COLS, showlegend=False, width=0.6,
    text=[fr(d.loc[i, "superficie_km2"] / 1000) for i in ISO], textposition="outside",
    hovertemplate="%{x} : %{y:,.0f} milliers de km²<extra></extra>"), row=1, col=2)
fig.update_yaxes(range=[0, 600], row=1, col=1)
fig.update_yaxes(range=[0, 720], row=1, col=2)
# Repère densité France métropolitaine (hors DOM), distincte de la France entière
dens_metro = d.loc["FRA", "densite_metropole_hab_km2"]
fig.add_trace(go.Scatter(x=["France"], y=[dens_metro], mode="markers",
    marker=dict(symbol="line-ew", size=30, line=dict(width=2, color=C.COULEURS["encre"])),
    showlegend=False, hovertemplate=f"France métropolitaine (hors DOM) : {dens_metro:.0f} hab/km²<extra></extra>"),
    row=1, col=1)
fig.add_annotation(x="France", y=dens_metro, text=f"métropole : {dens_metro:.0f}", showarrow=False,
    font=dict(size=9, color=C.COULEURS["encre"]), xanchor="left", xshift=20, row=1, col=1)
fig.add_annotation(x="France", y=107.6, text="5× moins dense<br>que les Pays-Bas", showarrow=True,
    arrowhead=0, ax=-4, ay=-52, font=dict(size=10, color=C.COULEURS["encre"]),
    bgcolor="rgba(251,249,245,0.9)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1,
    borderpad=3, row=1, col=1)
cadre(fig, 860, 500, b=110, l=64)
T.finaliser(fig,
    titre="La France : un territoire vaste, mais clairsemé",
    soustitre="Densité et superficie comparées — France, Allemagne, Pays-Bas",
    source="Eurostat (densité demo_r_d3dens, 2022 ; population demo_pjan, 2023). Extraction : 06/2026.",
    note="Lecture : la France est cinq fois moins dense que les Pays-Bas et près de vingt fois plus vaste.<br>"
         "À population comparable, c'est un territoire bien plus étendu à équiper et à administrer.",
    source_y=-0.22)
T.exporter(fig, str(OUT / "axe5_densite_superficie"))

# ===========================================================================
# 2) LE MAILLAGE — communes / écoles / policiers par habitant
# ===========================================================================
c3 = df3.set_index("iso3"); c5 = df5.set_index("iso3")
fig2 = make_subplots(rows=1, cols=3, horizontal_spacing=0.07,
    subplot_titles=("Communes pour 100 000 hab",
                    "Écoles du 1<sup>er</sup> degré pour 100 000 hab",
                    "Policiers pour 100 000 hab"))

def panel_bars(col, vals, fmt, hov):
    fig2.add_trace(go.Bar(x=NOMS, y=vals, marker_color=COLS, showlegend=False, width=0.6,
        text=[fmt(v) for v in vals], textposition="outside",
        hovertemplate=hov), row=1, col=col)

panel_bars(1, [c3.loc[i, "communes_pour_100k_hab"] for i in ISO],
           lambda v: fr(v, 1), "%{x} : %{y:.1f} communes / 100 000 hab<extra></extra>")
panel_bars(2, [c5.loc[i, "ecoles_pour_100k_hab"] for i in ISO],
           lambda v: fr(v, 1), "%{x} : %{y:.1f} écoles / 100 000 hab<extra></extra>")
panel_bars(3, [c5.loc[i, "policiers_pour_100k_hab"] for i in ISO],
           lambda v: fr(v, 0), "%{x} : %{y:.0f} policiers / 100 000 hab<extra></extra>")
fig2.update_yaxes(range=[0, 60], row=1, col=1)
fig2.update_yaxes(range=[0, 82], row=1, col=2)
fig2.update_yaxes(range=[0, 420], row=1, col=3)
fig2.add_annotation(x="France", y=c3.loc["FRA", "communes_pour_100k_hab"],
    text="34 935 communes<br>≈ 40 % de l'UE", showarrow=True, arrowhead=0, ax=62, ay=26,
    font=dict(size=9.5, color=C.COULEURS["encre"]), bgcolor="rgba(251,249,245,0.9)",
    bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3, row=1, col=1)
cadre(fig2, 980, 510, b=135, l=52, r=24)
T.finaliser(fig2,
    titre="Un maillage de proximité plus serré, à chaque échelon",
    soustitre="Nombre d'équipements et d'agents publics rapportés à la population",
    source="Communes : INSEE, Destatis, CBS (2024). Écoles : DEPP, Destatis, CBS (2023/24). Police : Eurostat crim_just_job (2021). Extraction : 06/2026.",
    note="Lecture : à population égale, la France entretient 4× plus de communes que l'Allemagne et 27× plus<br>"
         "que les Pays-Bas, plus d'écoles et plus de policiers — le coût d'une présence publique de proximité.<br>"
         "(Périmètres scolaires non strictement comparables : voir note méthodologique.)",
    source_y=-0.26)
T.exporter(fig2, str(OUT / "axe5_maillage_proximite"))

# ===========================================================================
# 3) LE COÛT — poids (% PIB) · par habitant (€ vs SPA) · par fonction (% PIB)
# ===========================================================================
tot = df4[df4.cofog == "TOTAL"].set_index("iso3")
fonctions = ["Éducation", "Ordre et sécurité publics"]
fct_court = {"Éducation": "Éducation", "Ordre et sécurité publics": "Ordre &<br>sécurité"}
fig3 = make_subplots(rows=1, cols=3, horizontal_spacing=0.08,
    subplot_titles=("Poids dans le PIB (%)",
                    "Par habitant : € courants vs pouvoir d'achat",
                    "Par fonction (% du PIB)"))
for iso, coul in zip(ISO, COLS):
    nom = C.PAYS[iso]
    # Panneau 1 — dépense totale en % du PIB
    fig3.add_trace(go.Bar(name=nom, legendgroup=iso, showlegend=True, x=["Total"],
        y=[tot.loc[iso, "pct_pib"]], marker_color=coul, width=0.7,
        text=[f"{fr(tot.loc[iso, 'pct_pib'], 1)} %"], textposition="outside",
        hovertemplate=f"{nom} : %{{y:.1f}} %% du PIB<extra></extra>"), row=1, col=1)
    # Panneau 2 — dépense totale par habitant : € courants vs SPA
    fig3.add_trace(go.Bar(name=nom, legendgroup=iso, showlegend=False,
        x=["€ courants", "SPA"], y=[tot.loc[iso, "eur_par_hab"], tot.loc[iso, "spa_par_hab"]],
        marker_color=coul, width=0.7,
        text=[f"{tot.loc[iso, 'eur_par_hab']/1000:.1f}k", f"{tot.loc[iso, 'spa_par_hab']/1000:.1f}k"],
        textposition="outside", textfont=dict(size=10),
        hovertemplate=f"{nom} — %{{x}} : %{{y:,.0f}} par hab.<extra></extra>"), row=1, col=2)
    # Panneau 3 — éducation + ordre/sécurité en % du PIB
    sub = df4[(df4.iso3 == iso) & (df4.cofog != "TOTAL")].set_index("fonction")
    fig3.add_trace(go.Bar(name=nom, legendgroup=iso, showlegend=False,
        x=[fct_court[f] for f in fonctions], y=[sub.loc[f, "pct_pib"] for f in fonctions],
        marker_color=coul, text=[fr(sub.loc[f, "pct_pib"], 1) for f in fonctions],
        textposition="outside", textfont=dict(size=10),
        hovertemplate=f"{nom} — %{{x}} : %{{y:.1f}} %% du PIB<extra></extra>"), row=1, col=3)
fig3.update_yaxes(range=[0, 66], ticksuffix=" %", row=1, col=1)
fig3.update_yaxes(range=[0, 30000], tickformat=",.0f", title="par habitant", row=1, col=2)
fig3.update_yaxes(range=[0, 6.6], ticksuffix=" %", row=1, col=3)
fig3.update_layout(barmode="group",
    legend=dict(orientation="h", y=-0.16, x=0.5, xanchor="center"))
cadre(fig3, 1000, 540, b=150, l=56, r=24)
T.finaliser(fig3,
    titre="La dépense la plus lourde — mais pas la plus élevée par habitant",
    soustitre="Trois lectures du même budget : le poids dans le PIB, le niveau par habitant, et le détail par fonction",
    source="Eurostat — dépenses publiques par fonction (gov_10a_exp, COFOG, 2023) ; parités de pouvoir d'achat (prc_ppp_ind). Extraction : 06/2026.",
    note="Lecture : la France consacre la plus grande part de son PIB à la dépense publique (56,9 %). Mais une fois corrigée du<br>"
         "niveau des prix (en SPA, standard de pouvoir d'achat), sa dépense par habitant rejoint celle de l'Allemagne et des Pays-Bas —<br>"
         "et sur l'éducation comme la sécurité, elle ne dépense pas plus en proportion. Le « surcoût » est un poids global, pas un prix par fonction.",
    source_y=-0.28)
T.exporter(fig3, str(OUT / "axe5_depense_publique"))

# ===========================================================================
# 4) LA DIVERSITÉ — dispersion des densités régionales (NUTS3, échelle log)
# ===========================================================================
fig4 = T.figure_base(largeur=780, hauteur=560)
for iso, coul in zip(ISO, COLS):
    s = df2[df2.iso3 == iso]
    fig4.add_trace(go.Box(y=s["densite_hab_km2"], name=C.PAYS[iso],
        marker=dict(color=coul, size=4, opacity=0.55),
        line=dict(color=coul), fillcolor="rgba(0,0,0,0)",
        boxpoints="all", jitter=0.5, pointpos=0, whiskerwidth=0.4, showlegend=False,
        hovertemplate=f"{C.PAYS[iso]} — densité : %{{y:.0f}} hab/km²<extra></extra>"))
fig4.update_yaxes(type="log", title="Densité de la région (hab/km², échelle log)",
    tickvals=[1, 10, 100, 1000, 10000],
    ticktext=["1", "10", "100", "1 000", "10 000"])
fig4.update_xaxes(title="")
fig4.add_annotation(x="France", y=np.log10(20420), text="Paris : 20 420", showarrow=True,
    arrowhead=0, ax=46, ay=0, font=dict(size=10, color=C.COULEURS["encre"]),
    bgcolor="rgba(251,249,245,0.9)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3)
fig4.add_annotation(x="France", y=np.log10(4), text="Guyane : 4 hab/km²<br>(9 régions sous 30)",
    showarrow=True, arrowhead=0, ax=60, ay=-6, font=dict(size=10, color=C.COULEURS["encre"]),
    bgcolor="rgba(251,249,245,0.9)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3)
fig4.add_annotation(x="Pays-Bas", y=np.log10(142), text="aucune région<br>sous 140 hab/km²",
    showarrow=True, arrowhead=0, ax=-2, ay=44, font=dict(size=9.5, color=C.couleur("NLD")),
    bgcolor="rgba(251,249,245,0.9)", bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=3)
fig4.update_layout(margin=dict(l=80, r=40, t=110, b=125))
T.finaliser(fig4,
    titre="La France a des territoires que ses voisins ne connaissent pas",
    soustitre="Densité de chaque région (NUTS3) — l'écart entre la plus dense et la plus vide",
    source="Eurostat — densité de population par région NUTS3 (demo_r_d3dens), 2022. Extraction : 06/2026.",
    note="Lecture : les 101 régions françaises s'étalent de 4 à plus de 20 000 hab/km². Neuf sont sous 30 hab/km²,<br>"
         "contre aucune en Allemagne (401 régions) ni aux Pays-Bas (35) — cette « longue traîne » de territoires<br>"
         "très peu denses qu'il faut malgré tout équiper est une singularité française.",
    source_y=-0.17)
T.exporter(fig4, str(OUT / "axe5_dispersion_regionale"))

# ===========================================================================
# 5) LE TEST CAUSAL INTERNE — densité × maillage/hab, 96 départements français
# ===========================================================================
# À institutions et richesse constantes (un seul pays), la densité commande-t-elle
# le nombre d'équipements publics par habitant ? Régression sur la densité en log10.
NOMS_DEP = {"48": "Lozère", "23": "Creuse", "75": "Paris", "92": "Hauts-de-Seine",
            "05": "Hautes-Alpes", "15": "Cantal"}
logd = np.log10(df6["densite_hab_km2"].values)
xfit = np.linspace(logd.min(), logd.max(), 50)

def panel_gradient(fig, col, ycol, coul, ylab):
    y = df6[ycol].values
    r = np.corrcoef(logd, y)[0, 1]
    a, b = np.polyfit(logd, y, 1)
    fig.add_trace(go.Scatter(
        x=df6["densite_hab_km2"], y=y, mode="markers",
        marker=dict(size=7, color=coul, opacity=0.6, line=dict(width=0.5, color="white")),
        showlegend=False, customdata=df6["dep"],
        hovertemplate="Dép. %{customdata} — densité %{x:.0f} hab/km²<br>" + ylab + " : %{y:.1f}<extra></extra>"),
        row=1, col=col)
    fig.add_trace(go.Scatter(x=10**xfit, y=a * xfit + b, mode="lines",
        line=dict(color=C.COULEURS["encre"], width=1.6, dash="dash"), showlegend=False,
        hoverinfo="skip"), row=1, col=col)
    # repères : Lozère / Paris
    for code in ("48", "75"):
        row_ = df6[df6.dep == code]
        if len(row_):
            fig.add_annotation(x=np.log10(row_["densite_hab_km2"].values[0]), y=row_[ycol].values[0],
                text=NOMS_DEP[code], showarrow=True, arrowhead=0, arrowwidth=1,
                arrowcolor=C.COULEURS["gris_texte"], ax=(28 if code == "48" else -22), ay=-22,
                font=dict(size=10, color=C.COULEURS["encre"]), bgcolor="rgba(251,249,245,0.9)",
                bordercolor=C.COULEURS["gris_grille"], borderwidth=1, borderpad=2, row=1, col=col)
    xr = "x domain" if col == 1 else f"x{col} domain"
    yr = "y domain" if col == 1 else f"y{col} domain"
    fig.add_annotation(x=0.5, y=0.97, xref=xr, yref=yr,
        text=f"r = {r:+.2f}", showarrow=False, font=dict(size=13, color=C.COULEURS["accent"]),
        xanchor="center")

fig5 = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
    subplot_titles=("Écoles du 1<sup>er</sup> degré pour 10 000 hab",
                    "Police + gendarmerie pour 10 000 hab"))
panel_gradient(fig5, 1, "ecoles_pour_10k", C.couleur("FRA"), "Écoles/10k")
panel_gradient(fig5, 2, "securite_pour_10k", C.COULEURS["accent"], "Sécurité/10k")
for col in (1, 2):
    fig5.update_xaxes(type="log", title="Densité du département (hab/km², échelle log)",
        tickvals=[10, 100, 1000, 10000], ticktext=["10", "100", "1 000", "10 000"], row=1, col=col)
fig5.update_yaxes(title="nombre pour 10 000 hab", rangemode="tozero", row=1, col=1)
fig5.update_yaxes(title="nombre pour 10 000 hab", rangemode="tozero", row=1, col=2)
cadre(fig5, 900, 540, b=150, l=64)
T.finaliser(fig5,
    titre="À l'intérieur de la France, le vide commande le maillage",
    soustitre="Chaque point = un département métropolitain (2024) ; plus il est peu dense, plus il porte d'équipements par habitant",
    source="INSEE — Base permanente des équipements 2024 (écoles, police, gendarmerie) ; densité geo.api.gouv.fr. Extraction : 06/2026.",
    note="Lecture : dans un même pays — donc à institutions, salaires et richesse identiques — la densité explique fortement le maillage par habitant "
         "(r = −0,7 environ). La Lozère porte 3 à 4× plus d'écoles et de points de sécurité par habitant que Paris.<br>"
         "C'est la démonstration interne du mécanisme « territoire dispersé → plus de points de service à financer », que la seule comparaison entre pays ne pouvait pas établir.",
    source_y=-0.26)
T.exporter(fig5, str(OUT / "axe5_gradient_departements"))

print("Axe 5 — visualisations exportées.")
