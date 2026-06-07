# Tribune « La mesure du bonheur et ses implications économiques » — Livrables
### Commande PZ-0626 · livré le 06/06/2026

Base de données structurée **et** visualisations prêtes à publier, sur **5 axes**, accompagnées de
notes de synthèse et d'une documentation complète des sources.

## 👉 Par où commencer
- **`index.html`** — galerie de prévisualisation : tous les graphiques + liens vers données et notes. *(à ouvrir dans un navigateur)*
- **`notes/note_synthese_globale.md`** — la lecture transversale au service de la thèse.

## Structure des livrables

```
tribune-pz-0626/
├── index.html                         ← galerie de tous les graphiques (ouvrir en 1er)
├── livrables/
│   ├── charte/charte_graphique.md     ← charte graphique (à valider)
│   └── proposition/…commerciale.md    ← délai + tarification
├── data/
│   ├── axe1/ … axe5/                  ← 1 Excel + CSV unitaires par axe (avec métadonnées)
│   └── raw/                           ← fichiers sources bruts + registre des sources
├── visualisations/
│   └── axe1/ … axe5/                  ← chaque graphique en .html / .svg / .png / _print.png
├── notes/
│   ├── axe1…axe5_note_synthese.md     ← 1 note d'une page par axe
│   ├── note_synthese_globale.md       ← synthèse transversale
│   └── rapport_verification_donnees.md← contrôle qualité indépendant
├── scripts/                           ← chaîne de production (collecte + graphiques)
├── SOURCES.md                         ← documentation des sources (URL + dates)
└── README.md
```

## Les 5 axes & 15 graphiques

| Axe | Données (Excel) | Graphiques |
|---|---|---|
| **1 — Bonheur vs économie** | `axe1_bonheur_economie.xlsx` | bulles bonheur×PIB ; paradoxe d'Easterlin |
| **2 — Europe & déclin** | `axe2_europe_declin.xlsx` | part PIB mondial ; écart PIB+BLI ; heures travaillées |
| **3 — Composants du bonheur** | `axe3_composants_bonheur.xlsx` | R&D pharma vs espérance de vie ; origine molécules ; PM2.5 |
| **4 — Arbitrages présent/futur** | `axe4_arbitrages.xlsx` | small multiples (fécondité/investissement/défense) ; dette & solde primaire |
| **5 — Coût du territoire** (FR/DE/NL) | `axe5_territoire_depense.xlsx` | densité & superficie ; maillage (communes/écoles/police) ; dépense (%PIB / €-SPA / fonction) ; dispersion NUTS3 ; **test causal par département (96)** |

## Formats de graphiques
Chaque graphique est fourni en **4 fichiers** :
- `.html` — **interactif** (embed web, info-bulles FR, responsive)
- `.svg` — **vectoriel** (édition, impression haute qualité)
- `.png` — raster **300 dpi**, fond crème (web)
- `_print.png` — raster **300 dpi**, fond blanc (impression presse)

## Reproductibilité
Toute la chaîne est scriptée (Python) dans `scripts/` :
`config.py` (charte/pays) · `theme.py` (thème + export) · `sources.py` (connecteurs API) ·
`livraison.py` (Excel) · `axeN_data.py` / `axeN_viz.py` (collecte / graphiques par axe) ·
`build_index.py` (galerie).

Pour régénérer un axe : `python3 scripts/axeN_data.py && python3 scripts/axeN_viz.py`.
Après ajustement de la **charte** (couleurs, police), tous les graphiques sont reconstruits en quelques minutes.

## Contrôle qualité
35 chiffres clés ont fait l'objet d'une **vérification croisée indépendante** (4 contrôleurs + synthèse) :
29 exacts, 6 points de présentation traités. Détail : `notes/rapport_verification_donnees.md`.
**Verdict : base fiable, exploitable pour publication.**

## Points en attente de votre validation
1. Charte graphique (palette, police, fond) — cf. `livrables/charte/charte_graphique.md`.
2. Priorisation confirmée : axes 1 & 2 d'abord (déjà livrés intégralement).
3. Périmètre pays / variantes de visualisation éventuelles.

*Sources : Banque mondiale, FMI, OCDE, Eurostat, INSEE/Destatis/CBS, DEPP, World Happiness Report/Gallup, GSS/NORC, EFPIA, OMS/SIPRI. Voir `SOURCES.md`.*
