"""
Thème graphique partagé (Plotly) + helpers d'export multi-format.

Applique la charte définie dans config.py :
  - fond crème léger pour le web, blanc pour l'impression
  - typographie sans-serif sobre
  - grille discrète, pas de bordures superflues
  - titre / sous-titre / source en pied de graphique
  - export simultané : HTML interactif (embed), SVG, PNG 300 dpi

Usage type :
    from theme import figure_base, finaliser, exporter
    fig = figure_base()
    ... # traces
    finaliser(fig, titre=..., soustitre=..., source=..., note=...)
    exporter(fig, "visualisations/axe1/mon_graphe")
"""
from __future__ import annotations
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path
import config as C

# ---------------------------------------------------------------------------
# Template Plotly maison
# ---------------------------------------------------------------------------
_template = go.layout.Template()
_template.layout = go.Layout(
    font=dict(family=C.FONT_FAMILLE, size=14, color=C.COULEURS["encre"]),
    paper_bgcolor=C.COULEURS["fond_web"],
    plot_bgcolor=C.COULEURS["fond_web"],
    colorway=[C.COULEURS["USA"], C.COULEURS["FRA"], C.COULEURS["DEU"],
              C.COULEURS["ITA"], C.COULEURS["ESP"], C.COULEURS["JPN"],
              C.COULEURS["KOR"], C.COULEURS["CHN"]],
    xaxis=dict(showgrid=False, zeroline=False, ticks="outside",
               ticklen=5, tickcolor=C.COULEURS["gris_grille"],
               linecolor=C.COULEURS["gris_grille"], linewidth=1,
               title_font=dict(size=13, color=C.COULEURS["gris_texte"]),
               tickfont=dict(size=12, color=C.COULEURS["gris_texte"])),
    yaxis=dict(showgrid=True, gridcolor=C.COULEURS["gris_grille"], gridwidth=1,
               zeroline=False, linecolor="rgba(0,0,0,0)",
               title_font=dict(size=13, color=C.COULEURS["gris_texte"]),
               tickfont=dict(size=12, color=C.COULEURS["gris_texte"])),
    legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                font=dict(size=12, color=C.COULEURS["encre"])),
    margin=dict(l=70, r=40, t=90, b=80),
    hoverlabel=dict(font=dict(family=C.FONT_FAMILLE, size=13)),
    separators=", ",   # format FR : virgule décimale, espace insécable pour les milliers
)
pio.templates["tribune"] = _template


def figure_base(largeur=None, hauteur=None) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        template="tribune",
        width=largeur or C.GABARIT["web_largeur_px"],
        height=hauteur or C.GABARIT["web_hauteur_px"],
    )
    return fig


def finaliser(fig: go.Figure, titre: str, soustitre: str = "",
              source: str = "", note: str = "", source_y: float = -0.16) -> go.Figure:
    """Ajoute titre / sous-titre / source selon la charte presse."""
    titre_html = f"<b>{titre}</b>"
    if soustitre:
        titre_html += f"<br><span style='font-size:13px;color:{C.COULEURS['gris_texte']}'>{soustitre}</span>"
    fig.update_layout(
        title=dict(text=titre_html, x=0.012, xanchor="left", y=0.96, yanchor="top",
                   font=dict(size=19, color=C.COULEURS["encre"])),
    )
    pied = []
    if source:
        pied.append(C.SOURCE_PREFIX + source)
    if note:
        pied.append(note)
    if pied:
        fig.add_annotation(
            text="<span style='font-size:11px'>" + "<br>".join(pied) + "</span>",
            xref="paper", yref="paper", x=0, y=source_y, xanchor="left", yanchor="top",
            showarrow=False, align="left", font=dict(color=C.COULEURS["gris_texte"]),
        )
    return fig


def annoter(fig, x, y, texte, ax=0, ay=-30, xref="x", yref="y"):
    """Annotation textuelle éditoriale (ex : '2008 : crise financière')."""
    fig.add_annotation(
        x=x, y=y, text=texte, xref=xref, yref=yref,
        showarrow=True, arrowhead=0, arrowwidth=1,
        arrowcolor=C.COULEURS["gris_texte"], ax=ax, ay=ay,
        font=dict(size=11, color=C.COULEURS["encre"]),
        bgcolor="rgba(251,249,245,0.85)", bordercolor=C.COULEURS["gris_grille"],
        borderwidth=1, borderpad=3, align="left",
    )
    return fig


def exporter(fig: go.Figure, chemin_sans_ext: str, web=True, svg=True, png=True,
             print_blanc=True):
    """
    Exporte une figure dans tous les formats demandés par le client :
      - .html  : embed interactif (web)
      - .svg   : vectoriel (impression / édition)
      - .png   : raster 300 dpi (impression)
    """
    p = Path(chemin_sans_ext)
    p.parent.mkdir(parents=True, exist_ok=True)
    produits = []

    if web:
        # Embed autonome, responsive, fond crème
        cfg = {"displayModeBar": False, "responsive": True, "locale": "fr"}
        fig.write_html(str(p) + ".html", include_plotlyjs="cdn",
                       full_html=True, config=cfg)
        produits.append(p.name + ".html")

    if svg:
        fig.write_image(str(p) + ".svg", format="svg",
                        width=fig.layout.width, height=fig.layout.height)
        produits.append(p.name + ".svg")

    if png:
        # PNG haute résolution : scale pour atteindre ~300 dpi en colonne presse
        scale = max(3, C.PRINT_W_PX / (fig.layout.width or 700))
        fig.write_image(str(p) + ".png", format="png",
                        width=fig.layout.width, height=fig.layout.height,
                        scale=scale)
        produits.append(p.name + ".png")

    if print_blanc:
        # Variante fond blanc pour l'impression (sans le crème web)
        fig_p = go.Figure(fig)
        fig_p.update_layout(paper_bgcolor="white", plot_bgcolor="white")
        scale = max(3, C.PRINT_W_PX / (fig.layout.width or 700))
        fig_p.write_image(str(p) + "_print.png", format="png",
                          width=fig.layout.width, height=fig.layout.height, scale=scale)
        produits.append(p.name + "_print.png")

    print(f"  ✓ {p.name} → {', '.join(produits)}")
    return produits
