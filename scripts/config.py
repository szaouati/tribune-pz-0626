"""
Configuration centrale — Tribune "Mesure du bonheur & implications économiques"
Commande PZ-0626

Définit la sélection de pays, les codes ISO, la charte chromatique par entité,
et les chemins du projet. Importé par tous les scripts de collecte et de viz.
"""
from pathlib import Path
import datetime

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
VIZ = ROOT / "visualisations"
NOTES = ROOT / "notes"
LIVRABLES = ROOT / "livrables"

# Date d'extraction (gelée à la date de la commande pour la traçabilité)
DATE_EXTRACTION = "2026-06-06"
ANNEE_COLLECTE = 2026

# ---------------------------------------------------------------------------
# Sélection de pays (codes ISO3) et libellés FR
# ---------------------------------------------------------------------------
# Pays cœur de l'analyse (Axe 1)
PAYS = {
    "BTN": "Bhoutan",
    "DNK": "Danemark",
    "FIN": "Finlande",
    "NOR": "Norvège",
    "SWE": "Suède",
    "ISL": "Islande",
    "USA": "États-Unis",
    "FRA": "France",
    "DEU": "Allemagne",
    "NLD": "Pays-Bas",
    "ITA": "Italie",
    "ESP": "Espagne",
    "JPN": "Japon",
    "KOR": "Corée du Sud",
    "CHN": "Chine",
}

# Sous-ensembles utiles
NORDIQUES = ["DNK", "FIN", "NOR", "SWE", "ISL"]
EUROPE_PRINCIPALE = ["FRA", "DEU", "ITA", "ESP"]   # Axe 2 / comparaison USA
PAYS_AXE1 = ["BTN", "DNK", "FIN", "NOR", "SWE", "ISL", "USA", "FRA", "DEU", "JPN", "KOR", "CHN"]

# Zones agrégées (codes World Bank / OWID)
ZONES = {
    "EUU": "Union européenne (27)",
    "USA": "États-Unis",
    "CHN": "Chine",
    "WLD": "Monde",
    "OED": "OCDE",
}

# ---------------------------------------------------------------------------
# CHARTE CHROMATIQUE
# Palette éditoriale sobre — inspiration presse économique sérieuse
# (Les Échos / The Economist / FT). Couleurs assignées par entité pour
# garantir la cohérence visuelle sur l'ensemble des graphiques.
# ---------------------------------------------------------------------------
COULEURS = {
    # Couleurs structurantes
    "encre":        "#1A1A1A",   # texte principal
    "gris_texte":   "#595959",   # texte secondaire / légendes
    "gris_grille":  "#E2DED7",   # gridlines
    "fond":         "#FFFFFF",   # fond impression
    "fond_web":     "#FBF9F5",   # fond crème léger pour embeds web
    "accent":       "#9C2B2E",   # rouge brique éditorial (mise en exergue)

    # Palette par entité (consistante sur tous les axes)
    "USA":          "#9C2B2E",   # rouge brique  — fil rouge "modèle de marché"
    "FRA":          "#2E5E8C",   # bleu France
    "DEU":          "#C28F2C",   # ocre/or
    "NLD":          "#2E7D5B",   # vert (contraste net avec le bleu FR et l'or DE — axe 5)
    "ITA":          "#4E7A5A",   # vert sobre
    "ESP":          "#B8633A",   # terracotta
    "JPN":          "#6E5A8C",   # prune
    "KOR":          "#3B8080",   # sarcelle
    "CHN":          "#7A1F22",   # rouge sombre
    "BTN":          "#C9A227",   # safran (drapeau bhoutanais)
    "DNK":          "#5B8BB0",
    "FIN":          "#3E6E94",
    "NOR":          "#2F567A",
    "SWE":          "#7AA6C4",
    "ISL":          "#9CBFD6",

    # Zones
    "EUU":          "#2E5E8C",   # UE = bleu
    "WLD":          "#9A9A9A",
    "RDM":          "#BBB3A8",   # reste du monde
    "OED":          "#8C8C8C",
    "Europe":       "#2E5E8C",
    "nordiques":    "#3E6E94",
}

def couleur(code: str, defaut: str = "#8C8C8C") -> str:
    return COULEURS.get(code, defaut)

# Ordre de tri lisible pour les légendes
ORDRE_PAYS = ["USA", "DEU", "FRA", "NLD", "ITA", "ESP", "JPN", "KOR", "CHN",
              "FIN", "DNK", "NOR", "SWE", "ISL", "BTN"]

# ---------------------------------------------------------------------------
# Typographie & gabarits
# ---------------------------------------------------------------------------
# Web : largeur ~700px ; Impression : ~180mm.
GABARIT = {
    "web_largeur_px": 700,
    "web_hauteur_px": 460,
    "print_largeur_mm": 180,
    "dpi": 300,
}
# 180 mm @ 300 dpi = 2126 px ; on rend en grand puis export.
PRINT_W_PX = int(GABARIT["print_largeur_mm"] / 25.4 * GABARIT["dpi"])  # ~2126

FONT_FAMILLE = "Helvetica Neue, Helvetica, Arial, sans-serif"

SOURCE_PREFIX = "Source : "
CREDIT = "Données : voir fiche méthodologique — Tribune PZ-0626"

if __name__ == "__main__":
    print("Racine projet :", ROOT)
    print("Pays cœur :", len(PAYS))
    print("Print width px (180mm @300dpi) :", PRINT_W_PX)
    print("Date extraction :", DATE_EXTRACTION)
