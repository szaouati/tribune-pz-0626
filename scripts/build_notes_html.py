"""
Génère, pour chaque note de synthèse, une page HTML propre et responsive :
  - graphique(s) de l'axe en haut
  - texte de la note bien mis en page (markdown -> HTML)
  - lisible sur mobile (viewport, colonne fluide, tableaux défilables)
Sorties : notes/<slug>.html
"""
import re
import markdown
import config as C

ROOT = C.ROOT
NOTES = ROOT / "notes"

# note -> (slug de sortie, titre onglet, [ (chemin_png, legende, lien_interactif) ])
def chart(axe, slug, leg):
    return (f"../visualisations/{axe}/{slug}.png", leg, f"../visualisations/{axe}/{slug}.html")

PAGES = {
    "axe1_note_synthese.md": ("axe1", "Axe 1 — Bonheur vs économie", [
        chart("axe1", "axe1_bulles_bonheur_pib", "Bonheur × PIB/habitant (bulles, 2024)"),
        chart("axe1", "axe1_easterlin_pib_bonheur", "Paradoxe d'Easterlin (USA, 1970-2024)")]),
    "axe2_note_synthese.md": ("axe2", "Axe 2 — Europe & déclin", [
        chart("axe2", "axe2_part_pib_mondial", "Part du PIB mondial par zone (1990-2024)"),
        chart("axe2", "axe2_ecart_pib_bli", "Écart de PIB/hab + Better Life Index"),
        chart("axe2", "axe2_heures_travaillees", "Heures travaillées (2000-2023)")]),
    "axe3_note_synthese.md": ("axe3", "Axe 3 — Composants du bonheur", [
        chart("axe3", "axe3_rd_esperance_vie", "R&D pharma vs espérance de vie (par zone)"),
        chart("axe3", "axe3_origine_molecules", "Origine des nouvelles molécules (2024)"),
        chart("axe3", "axe3_pm25_air", "Qualité de l'air — PM2.5 (1990-2020)")]),
    "axe4_note_synthese.md": ("axe4", "Axe 4 — Arbitrages présent/futur", [
        chart("axe4", "axe4_small_multiples", "Fécondité, investissement, défense"),
        chart("axe4", "axe4_soutenabilite_dette", "Dette publique & solde primaire")]),
    "note_synthese_globale.md": ("synthese-globale", "Synthèse globale", [
        chart("axe1", "axe1_easterlin_pib_bonheur", "Axe 1 — paradoxe d'Easterlin"),
        chart("axe2", "axe2_part_pib_mondial", "Axe 2 — part du PIB mondial"),
        chart("axe3", "axe3_rd_esperance_vie", "Axe 3 — R&D pharma vs espérance de vie"),
        chart("axe4", "axe4_small_multiples", "Axe 4 — arbitrages présent/futur")]),
    "rapport_verification_donnees.md": ("verification", "Rapport de vérification", []),
    # documents de cadrage (texte seul) — lus hors du dossier notes/
    "../livrables/charte/charte_graphique.md": ("charte", "Charte graphique", []),
    "../livrables/proposition/proposition_commerciale.md": ("proposition", "Proposition commerciale", []),
}

CSS = """
:root{--encre:#1A1A1A;--gris:#595959;--fond:#FBF9F5;--accent:#9C2B2E;--grille:#E2DED7;}
*{box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;color:var(--encre);
     background:var(--fond);margin:0;line-height:1.62;font-size:17px;}
.bar{max-width:820px;margin:0 auto;padding:16px 20px 0;}
.bar a{color:var(--accent);text-decoration:none;font-size:14px;}
.bar a:hover{text-decoration:underline;}
main{max-width:820px;margin:0 auto;padding:8px 20px 64px;}
h1.page{font-size:27px;line-height:1.2;margin:14px 0 6px;}
.charts{margin:18px 0 30px;display:flex;flex-direction:column;gap:16px;}
figure{margin:0;background:#fff;border:1px solid var(--grille);border-radius:10px;overflow:hidden;
       box-shadow:0 1px 3px rgba(0,0,0,.05);}
figure img{width:100%;height:auto;display:block;}
figcaption{font-size:14px;font-weight:600;padding:10px 14px 2px;}
figure .lk{display:block;padding:0 14px 12px;font-size:13px;}
figure .lk a{color:var(--gris);text-decoration:none;}
figure .lk a:hover{color:var(--accent);}
article h1{font-size:22px;margin:30px 0 4px;border-left:4px solid var(--accent);padding-left:12px;}
article h2{font-size:20px;margin:28px 0 6px;}
article h3{font-size:15px;color:var(--gris);font-weight:600;margin:4px 0 18px;}
article p{margin:12px 0;}
article ul{padding-left:22px;}
article li{margin:6px 0;}
article strong{color:var(--encre);}
article em{color:var(--gris);}
article a{color:var(--accent);}
article code{background:#efeae1;padding:1px 5px;border-radius:4px;font-size:.9em;}
hr{border:0;border-top:1px solid var(--grille);margin:26px 0;}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:16px 0;}
table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:420px;}
th,td{border:1px solid var(--grille);padding:7px 10px;text-align:left;vertical-align:top;}
th{background:#f0ebe1;}
footer{max-width:820px;margin:0 auto;padding:22px 20px;color:var(--gris);font-size:13px;
       border-top:1px solid var(--grille);}
@media(max-width:600px){body{font-size:16px;}h1.page{font-size:23px;}main{padding:8px 16px 56px;}}
"""

def build(md_name, slug, titre, charts):
    md_text = (NOTES / md_name).read_text(encoding="utf-8")
    lines = md_text.splitlines()
    # extrait le 1er titre H1 -> titre de page
    page_title = titre
    body_lines = []
    h1_done = False
    for ln in lines:
        if not h1_done and ln.startswith("# "):
            page_title = ln[2:].strip()
            h1_done = True
            continue
        body_lines.append(ln)
    body_md = "\n".join(body_lines)
    html_body = markdown.markdown(body_md, extensions=["tables", "sane_lists", "attr_list"])
    # tableaux défilables sur mobile
    html_body = html_body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    # liens .md internes -> .html générés
    for src, (dslug, _, _) in PAGES.items():
        html_body = html_body.replace(f'href="notes/{src}"', f'href="{dslug}.html"')
        html_body = html_body.replace(f'href="{src}"', f'href="{dslug}.html"')

    figs = ""
    for png, leg, inter in charts:
        figs += f"""
      <figure>
        <img src="{png}" alt="{leg}" loading="lazy">
        <figcaption>{leg}</figcaption>
        <span class="lk"><a href="{inter}" target="_blank">↗ version interactive</a></span>
      </figure>"""
    charts_block = f'<div class="charts">{figs}</div>' if charts else ""

    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title} — Tribune PZ-0626</title>
<style>{CSS}</style></head><body>
<nav class="bar"><a href="../index.html">← Tous les livrables</a></nav>
<main>
  <h1 class="page">{page_title}</h1>
  {charts_block}
  <article>{html_body}</article>
</main>
<footer>Tribune « La mesure du bonheur » · Commande PZ-0626 · données extraites le 06/06/2026.
Sources : Banque mondiale, FMI, OCDE, World Happiness Report/Gallup, GSS/NORC, EFPIA, OMS/SIPRI.</footer>
</body></html>"""
    out = NOTES / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    print(f"  ✓ notes/{slug}.html  ({len(charts)} graphique(s))")

if __name__ == "__main__":
    for md_name, (slug, titre, charts) in PAGES.items():
        build(md_name, slug, titre, charts)
    print("Pages de notes générées.")
