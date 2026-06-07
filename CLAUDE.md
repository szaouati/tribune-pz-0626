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
python3 axe5_data.py          # axe 5 : territoire & dépense (Eurostat ; FR/DE/NL ; PPA/SPA, CITE-1, métropole)
python3 axe5_gradient_data.py # axe 5 : test causal interne France par dép. (BPE + OFGL) ; À LANCER APRÈS axe5_data
python3 axe5_viz.py           # axe 5 : 5 graphiques (densité, maillage, dépense, dispersion, gradient)
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
| `scripts/sources.py` | Connecteurs : `wb()` (Banque mondiale), `owid()`, `imf()`, `oecd_sdmx()`+`parse_sdmx_json()`, `eurostat()`+`parse_jsonstat()`, `opendatasoft()` (OFGL…), `insee_melodi()` (BPE). Journalise dans `data/raw/_registre_sources.csv`. |
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
- **Eurostat** (API dissemination JSON-stat, axe 5) : `gov_10a_exp` (dépenses COFOG : TOTAL/GF09 éducation/GF03 ordre & sécurité), `demo_r_d3dens` (densité NUTS3), `demo_pjan`/`demo_r_pjanaggr3` (population nat./NUTS3), `crim_just_job` (police, CITP-08 `OC5412`), `prc_ppp_ind` (PPA du PIB → SPA/hab), `educ_uoe_enra01` (élèves CITE 1, `isced11=ED1`). Comptages communes/écoles = compilation INSEE/Destatis/CBS/DEPP.
- **Open data France (axe 5, test de gradient interne)** : **OFGL** (`data.ofgl.fr`, Opendatasoft v2.1 ; champ `euros_par_habitant`, filtrer `type_de_budget="Budget principal"` et `year(exer)=AAAA` car `exer` est de type date) ; **INSEE BPE** via API Mélodi (`DS_BPE`, `BPE_MEASURE=FACILITIES`, `GEO=DEP` pour tous les dép. d'un coup ; types : écoles `C107/C108/C109`, collège `C201`, lycées `C301/C302/C303`, **police `A101`, gendarmerie `A104`** — PAS `F1xx`) ; superficies par dép. via `geo.api.gouv.fr/communes` (champ `surface` en hectares, agréger par `codeDepartement`).

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
- **Eurostat `demo_r_d3dens`** : un `geo=FR` renvoie la **densité nationale** (pas les régions) ; pour les NUTS3, tirer **sans filtre `geo`** puis garder les codes de **longueur 5** (FR/DE/NL) — écarte agrégats nationaux et NUTS1-2.
- **Axe 5 — piège du dénominateur** : la France a la dépense la plus lourde en **% PIB** (56,9 %) mais **pas** en **€/habitant** (les Pays-Bas, plus riches, dépensent plus par tête) ni **fonction par fonction**. Toujours préciser l'indicateur ; le « surcoût » est dans le poids global + l'émiettement, pas le prix unitaire.
- **Axe 5 — densité France** : `demo_r_d3dens` (107,6) est **France entière (incl. DOM)** ; la métropole est ~120. La traîne basse (Guyane 4 hab/km²) inclut l'outre-mer, mais plusieurs départements métropolitains restent sous les minima DE/NL.
- **Axe 5 — comptages d'écoles** : périmètres nationaux non identiques (« école » FR et basisschool NL = CITE 0+1 ; Grundschule DE = CITE 1 seul) → comptage écoles/hab à présenter avec réserve ; pour comparer, utiliser les **effectifs CITE 1 harmonisés** (`educ_uoe_enra01`, `isced11=ED1`). Communes (LAU) et police (Eurostat) sont harmonisés.
- **Axe 5 — test causal interne (gradient)** : faire le gradient densité→maillage **par département à l'intérieur de la France** (institutions constantes). Effet FORT sur le **nombre d'équipements/hab** (écoles r≈−0,74, sécurité r≈−0,69) ; mais la **dépense communale/hab** monte avec la densité (+0,54, effet ville) → le surcoût de dispersion est un coût de *maillage*, pas un coût en €/hab. `axe5_gradient_data.py` reconstruit l'Excel via openpyxl → **le lancer APRÈS `axe5_data.py`** (qui réécrit le xlsx avec xlsxwriter et effacerait les feuilles Gradient).
- **Axe 5 — €/hab vs SPA** : convertir €/hab en **SPA** (÷ PPA du PIB) pour comparer en volume ; en SPA les 3 pays sont quasi à parité (~21,5-22,1k), l'écart en € courants n'étant qu'un effet de niveau de prix. La densité FR en `demo_r_d3dens` (107,6) inclut les DOM ; **métropole = 120,9** (NUTS3 hors `FRY*`).
- **GitHub Pages** : `.nojekyll` présent à la racine (sinon Jekyll ignore certains fichiers). Repo **public** requis pour Pages gratuit.

## Qualité
35 chiffres clés vérifiés par contrôle croisé indépendant (29 OK, 0 erreur confirmée). Voir
`notes/rapport_verification_donnees.md`. Toujours afficher source + date sous chaque graphique.
