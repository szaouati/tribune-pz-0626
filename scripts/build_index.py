"""
Packaging final :
  - nettoie/dédoublonne le registre des sources -> data/raw/registre_sources_propre.csv
  - génère une galerie HTML (livrables/index.html) prévisualisant tous les graphiques
"""
import pandas as pd
from pathlib import Path
import config as C

ROOT = C.ROOT

# --- 1) Registre propre -----------------------------------------------------
reg = pd.read_csv(C.RAW / "_registre_sources.csv")
reg = reg[~reg.serie.astype(str).str.startswith("test")].drop_duplicates(subset=["serie", "source"], keep="last")
reg.to_csv(C.RAW / "registre_sources_propre.csv", index=False, encoding="utf-8-sig")
print(f"Registre propre : {len(reg)} séries.")

# --- 2) Galerie HTML --------------------------------------------------------
AXES = {
    "Axe 1 — Bonheur déclaré vs performance économique": {
        "dir": "axe1",
        "data": "data/axe1/axe1_bonheur_economie.xlsx",
        "note": "notes/axe1.html",
        "charts": [
            ("axe1_bulles_bonheur_pib", "Bonheur × PIB/habitant (bulles, 2024)"),
            ("axe1_easterlin_pib_bonheur", "Paradoxe d'Easterlin (USA, 1970-2024)"),
        ],
    },
    "Axe 2 — L'Europe heureuse et son déclin relatif": {
        "dir": "axe2",
        "data": "data/axe2/axe2_europe_declin.xlsx",
        "note": "notes/axe2.html",
        "charts": [
            ("axe2_part_pib_mondial", "Part du PIB mondial par zone (1990-2024)"),
            ("axe2_ecart_pib_bli", "Écart de PIB/hab + Better Life Index"),
            ("axe2_heures_travaillees", "Heures travaillées (2000-2023)"),
        ],
    },
    "Axe 3 — Composants du bonheur et sous-jacents économiques": {
        "dir": "axe3",
        "data": "data/axe3/axe3_composants_bonheur.xlsx",
        "note": "notes/axe3.html",
        "charts": [
            ("axe3_rd_esperance_vie", "R&D pharma vs espérance de vie (par zone)"),
            ("axe3_origine_molecules", "Origine des nouvelles molécules (2024)"),
            ("axe3_pm25_air", "Qualité de l'air — PM2.5 (1990-2020)"),
        ],
    },
    "Axe 4 — Tensions bonheur individuel / prospérité collective": {
        "dir": "axe4",
        "data": "data/axe4/axe4_arbitrages.xlsx",
        "note": "notes/axe4.html",
        "charts": [
            ("axe4_small_multiples", "Fécondité, investissement, défense (small multiples)"),
            ("axe4_soutenabilite_dette", "Dette publique & solde primaire"),
        ],
    },
    "Axe 5 — Le coût du territoire : densité, fragmentation, dépense publique": {
        "dir": "axe5",
        "data": "data/axe5/axe5_territoire_depense.xlsx",
        "note": "notes/axe5.html",
        "charts": [
            ("axe5_densite_superficie", "Densité & superficie (France / Allemagne / Pays-Bas)"),
            ("axe5_maillage_proximite", "Maillage : communes, écoles, police par habitant"),
            ("axe5_depense_publique", "Dépense publique : % PIB, par habitant (€/SPA), par fonction"),
            ("axe5_dispersion_regionale", "Dispersion des densités régionales (NUTS3)"),
            ("axe5_gradient_departements", "Test causal : densité × maillage, 96 départements français"),
        ],
    },
}

cards = []
for titre, ax in AXES.items():
    blocs = []
    for slug, leg in ax["charts"]:
        base = f"visualisations/{ax['dir']}/{slug}"
        blocs.append(f"""
        <figure class="chart">
          <img src="{base}.png" alt="{leg}" loading="lazy">
          <figcaption>{leg}</figcaption>
          <div class="links">
            <a href="{base}.html" target="_blank">↗ interactif (HTML)</a>
            <a href="{base}.svg" target="_blank">SVG</a>
            <a href="{base}.png" target="_blank">PNG 300dpi</a>
          </div>
        </figure>""")
    cards.append(f"""
    <section class="axe">
      <h2>{titre}</h2>
      <p class="meta">
        <a href="{ax['data']}">📊 Données (Excel)</a> ·
        <a href="{ax['note']}">📝 Note de synthèse</a>
      </p>
      <div class="grid">{''.join(blocs)}</div>
    </section>""")

html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tribune « La mesure du bonheur » — Livrables PZ-0626</title>
<style>
  :root {{ --encre:#1A1A1A; --gris:#595959; --fond:#FBF9F5; --accent:#9C2B2E; --grille:#E2DED7; }}
  * {{ box-sizing:border-box; }}
  body {{ font-family:'Helvetica Neue',Helvetica,Arial,sans-serif; color:var(--encre);
          background:var(--fond); margin:0; line-height:1.5; }}
  header {{ padding:48px 24px 28px; border-bottom:3px solid var(--accent); max-width:1100px; margin:0 auto; }}
  h1 {{ font-size:30px; margin:0 0 6px; }}
  .sub {{ color:var(--gris); font-size:16px; max-width:760px; }}
  main {{ max-width:1100px; margin:0 auto; padding:12px 24px 60px; }}
  .axe {{ margin:42px 0; }}
  h2 {{ font-size:21px; border-left:4px solid var(--accent); padding-left:12px; margin-bottom:6px; }}
  .meta a {{ color:var(--accent); text-decoration:none; margin-right:10px; font-size:14px; }}
  .meta a:hover {{ text-decoration:underline; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(330px,1fr)); gap:22px; margin-top:18px; }}
  figure.chart {{ margin:0; background:#fff; border:1px solid var(--grille); border-radius:8px;
                  overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.05); }}
  figure.chart img {{ width:100%; display:block; }}
  figcaption {{ font-size:14px; font-weight:600; padding:10px 14px 4px; }}
  .links {{ padding:0 14px 12px; font-size:13px; }}
  .links a {{ color:var(--gris); text-decoration:none; margin-right:12px; }}
  .links a:hover {{ color:var(--accent); }}
  footer {{ max-width:1100px; margin:0 auto; padding:24px; color:var(--gris); font-size:13px;
            border-top:1px solid var(--grille); }}
  .docs {{ background:#fff; border:1px solid var(--grille); border-radius:8px; padding:18px 22px; margin-top:20px; }}
  .docs a {{ color:var(--accent); }}
</style></head><body>
<header>
  <h1>La mesure du bonheur — et ses implications économiques</h1>
  <p class="sub">Base de données structurée &amp; visualisations prêtes à publier · 5 axes ·
     15 graphiques (HTML interactif + SVG + PNG 300 dpi) · Commande PZ-0626 · données extraites le 06/06/2026.</p>
</header>
<main>
  <div class="docs">
    <strong>Documents de cadrage &amp; pilotage :</strong>
    <a href="notes/charte.html">Charte graphique</a> ·
    <a href="notes/proposition.html">Proposition commerciale</a> ·
    <a href="notes/synthese-globale.html">Synthèse globale</a> ·
    <a href="notes/verification.html">Rapport de vérification</a> ·
    <a href="SOURCES.md">Documentation des sources</a> ·
    <a href="README.md">Guide de livraison</a>
  </div>
  {''.join(cards)}
</main>
<footer>
  Sources primaires : Banque mondiale (WDI) · FMI (WEO) · OCDE (Better Life Index, ANBERD, heures travaillées) ·
  Eurostat (COFOG, densité, PPA, écoles CITE 1, police) · INSEE (BPE, geo.api) · OFGL · Destatis / CBS · DEPP ·
  World Happiness Report / Gallup · General Social Survey (NORC) · EFPIA · OMS / SIPRI.<br>
  Tous les graphiques sont régénérables via la chaîne de production scriptée (dossier <code>scripts/</code>).
</footer>
</body></html>"""

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("Galerie écrite : index.html (racine du projet)")
