# CLAUDE.md — Tribune « La mesure du bonheur » (PZ-0626)

Projet de **data-journalisme** : base de données structurée + visualisations prêtes à publier pour une
tribune sur la mesure du bonheur et ses implications économiques. 4 axes thématiques.
Brief client d'origine : `../Commande.md` (dossier parent).
En ligne : https://szaouati.github.io/tribune-pz-0626/ (GitHub Pages, repo public `szaouati/tribune-pz-0626`).

## Commandes

Tout le pipeline est en Python 3.11 ; dépendances : `pandas numpy plotly kaleido openpyxl xlsxwriter requests pdfplumber markdown`.
Exécuter depuis `scripts/` (les imports sont relatifs au dossier `scripts/`).

```bash
cd scripts
python3 axeN_data.py     # (re)collecte les données de l'axe N -> data/axeN/*.csv + .xlsx
python3 axeN_viz.py      # (re)génère les graphiques de l'axe N -> visualisations/axeN/*.{html,svg,png}
python3 axe1_excel.py    # axe 1 : assemblage Excel (séparé du data)
python3 axe3_origin.py   # axe 3 : ajoute l'origine des molécules (EFPIA) + rebuild Excel
python3 build_notes_html.py   # notes .md -> pages HTML responsives (notes/*.html)
python3 build_index.py        # galerie d'accueil -> index.html (racine) + registre propre
```

Déploiement : `git add -A && git commit && git push` → GitHub Pages se reconstruit (~1-2 min).
Aperçu local sans navigateur (bloqué par politique org) : capture headless
`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --window-size=390,1800 --screenshot=/tmp/x.png file://…`

## Architecture

| Fichier | Rôle |
|---|---|
| `scripts/config.py` | **Socle** : pays/ISO, palette par entité (`COULEURS`), gabarits, chemins. À éditer pour changer la charte. |
| `scripts/theme.py` | Thème Plotly `tribune` + `figure_base()`, `finaliser()`, `annoter()`, `exporter()` (HTML+SVG+PNG 300dpi+print). |
| `scripts/sources.py` | Connecteurs : `wb()` (Banque mondiale), `owid()`, `imf()`, `oecd_sdmx()`+`parse_sdmx_json()`. Journalise dans `data/raw/_registre_sources.csv`. |
| `scripts/livraison.py` | Écriture CSV + Excel multi-feuilles avec feuille « Métadonnées ». |
| `scripts/axeN_data.py` / `axeN_viz.py` | Collecte / graphiques par axe. |
| `scripts/build_notes_html.py` / `build_index.py` | Pages HTML des notes + galerie d'accueil. |
| `data/axeN/` | 1 Excel + CSV unitaires par axe. `data/raw/` = sources brutes (gros fichiers gitignorés). |
| `visualisations/axeN/` | chaque graphe en `.html` (interactif), `.svg`, `.png` (crème), `_print.png` (blanc). |
| `notes/` | notes `.md` + leurs pages `.html` générées. |
| `livrables/` | charte graphique + proposition commerciale (`.md`). |

## Sources de données (toutes par API, reproductibles ; extraction figée au 2026-06-06)
- **Banque mondiale** WDI (clé : code indicateur, ex. `NY.GDP.PCAP.PP.CD`).
- **FMI** WEO datamapper : `GGXWDG_NGDP` (dette), `pb` (solde primaire).
- **OCDE** SDMX : `DF_BLI` (Better Life Index, archive), `DF_ANBERDi4` (R&D pharma C21), heures via OWID.
- **OWID** : `happiness-cantril-ladder`, `annual-working-hours-per-worker`.
- **GSS/NORC** : microdonnées (paradoxe d'Easterlin) ; **EFPIA 2025** PDF (origine des molécules).

## Conventions & charte
- Palette **par entité** dans `config.COULEURS` (USA rouge brique, France bleu…) — cohérente entre graphiques.
  Pour les graphes de **zones** (parts PIB, R&D), la Chine est rendue en **or** (distincte du rouge USA).
- Nombres au **format français** : virgule décimale, espace milliers (`separators=", "` dans le template Plotly).
- Style éditorial sobre (fond crème `#FBF9F5` web / blanc print), titre éditorialisé + sous-titre + source + clé de lecture.
- Pages web/notes : **mobile-first** (viewport, colonne fluide, tableaux dans `.tw` défilables).

## Pièges connus (déjà corrigés — ne pas réintroduire)
- **Plotly 6** : utiliser `yaxis=dict(title=dict(font=…))`, PAS `titlefont` (erreur).
- **`%`** : doubler (`%%`) UNIQUEMENT dans `hovertemplate` ; dans les `annotation.text`, un seul `%`.
- **Axes log** : les coordonnées d'annotation doivent être en **log10** de la valeur (ex. axe 1 bulles).
- **FMI** : `requests` est bloqué (403, empreinte TLS) → `sources.imf()` passe par **curl** ; l'API renvoie TOUS les pays (filtrer côté client).
- **GSS** : `axe1` télécharge un .dta de ~598 Mo (dans un zip 47 Mo) puis le supprime ; calcul pondéré `WTSSPS`.
- **Bhoutan** : WHR s'arrête en **2018** (sorti du Gallup World Poll) → point daté dans le nuage de l'axe 1.
- **Dette Japon** : ~214 % (dernier millésime FMI), PAS ~250 % (millésimes anciens) — documenté.
- **« Europe » R&D (ANBERD)** : UE-27 (hors CYP/LUX/MLT) + CHE/NOR/ISL ; **Royaume-Uni non couvert** (Europe sous-estimée).
- **GitHub Pages** : `.nojekyll` présent à la racine (sinon Jekyll ignore certains fichiers). Repo **public** requis pour Pages gratuit.

## Qualité
35 chiffres clés vérifiés par contrôle croisé indépendant (29 OK, 0 erreur confirmée). Voir
`notes/rapport_verification_donnees.md`. Toujours afficher source + date sous chaque graphique.
