# Charte graphique — Tribune « La mesure du bonheur »
### Commande PZ-0626 · proposition à valider avant exécution finale

> Le client a souhaité valider la charte chromatique et les choix de visualisation avant l'exécution
> finale. Ce document formalise les choix appliqués aux graphiques livrés ; ils restent **ajustables**
> selon vos retours (notamment la palette).

---

## 1. Parti pris éditorial

Style **sobre et crédible**, adapté à une publication de presse sérieuse (référents :
*Les Échos*, *The Economist*, *Financial Times*). Pas d'infographie grand public : pas de dégradés
tape-à-l'œil, pas d'effets 3D, pas d'icônes superflues. La donnée prime ; la couleur ne sert qu'à
porter le sens.

Principes :
- **Fond crème léger** (`#FBF9F5`) pour la version web, **blanc** pour l'impression.
- **Grille discrète** horizontale uniquement, axes épurés (pas de cadre).
- **Titre court et éditorialisé** (qui pose la question / l'enseignement), **sous-titre descriptif**.
- **Source et clé de lecture** systématiques en pied de graphique.
- **Annotations textuelles** sur les points clés (crises, ruptures, écarts).

---

## 2. Palette chromatique

### Couleurs structurantes
| Rôle | HEX | Usage |
|---|---|---|
| Encre | `#1A1A1A` | Texte principal, titres |
| Gris texte | `#595959` | Sous-titres, légendes, sources |
| Gris grille | `#E2DED7` | Lignes de grille, axes |
| Fond web | `#FBF9F5` | Arrière-plan des embeds |
| Fond impression | `#FFFFFF` | Arrière-plan print |
| Accent éditorial | `#9C2B2E` | Mise en exergue, repères critiques |

### Couleurs par entité (cohérentes sur tous les axes)
Chaque pays/zone garde **la même couleur d'un graphique à l'autre**, pour une lecture fluide de
la série.

| Entité | HEX | | Entité | HEX |
|---|---|---|---|---|
| États-Unis | `#9C2B2E` (rouge brique) | | Japon | `#6E5A8C` (prune) |
| France | `#2E5E8C` (bleu) | | Corée du Sud | `#3B8080` / `#C77B30` |
| Allemagne | `#C28F2C` (ocre) | | Chine | `#C9A227` / `#D9A441` (or) |
| Italie | `#4E7A5A` (vert) | | Union européenne | `#2E5E8C` (bleu) |
| Espagne | `#B8633A` (terracotta) | | Reste du monde | `#C9C3B8` (gris-sable) |
| Bhoutan | `#C9A227` (safran) | | Pays nordiques | dégradé de bleus |

> Le rouge brique des **États-Unis** fait office de fil rouge de la tribune (« modèle de marché »).
> Pour les graphiques de zones (parts de PIB, R&D), la **Chine** est rendue en **or** afin d'être
> nettement distincte du rouge américain.

---

## 3. Typographie

- Famille : **sans-serif neutre** — *Helvetica Neue / Helvetica / Arial* (substituables par la police
  maison de la rédaction : Söhne, Founders Grotesk, ou équivalent).
- Hiérarchie : Titre 19 px gras · Sous-titre 13 px gris · Axes 12-13 px · Source 11 px.
- **Nombres au format français** : virgule décimale, espace pour les milliers (`62 600`, `7,7`).

---

## 4. Gabarits & formats d'export

| Support | Largeur | Format livré |
|---|---|---|
| Web / embed | ~700-860 px (responsive) | **HTML interactif** (Plotly, JS via CDN) |
| Impression presse | ~180 mm | **PNG 300 dpi** + **SVG** vectoriel |

Chaque graphique est livré en **4 fichiers** : `.html` (interactif), `.svg` (vectoriel éditable),
`.png` (haute résolution, fond crème), `_print.png` (haute résolution, fond blanc).

---

## 5. Conventions de visualisation par type

- **Nuage de points / bulles** : taille ∝ √population, étiquettes directes, ligne de tendance pointillée.
- **Aires empilées** : étiquetage direct des bandes (pas de légende séparée), repères temporels (crises).
- **Séries temporelles** : épaisseur accrue (2,6 px) pour l'entité mise en avant, labels en bout de ligne.
- **Barres groupées / small multiples** : axes partagés, lignes de repère annotées (seuil 2,1 ; cible OTAN 2 %).
- **Double axe** : couleur de l'axe = couleur de la série correspondante.

---

## 6. Points à arbitrer avec vous

1. **Police définitive** (police maison de la publication ?).
2. **Fond** : crème `#FBF9F5` ou blanc pur pour le web ?
3. **Couleur d'accent** : rouge brique `#9C2B2E` ou autre teinte signature de la rédaction ?
4. **Niveau d'annotation** : sobre (actuel) ou plus appuyé (encadrés pédagogiques) ?
5. **Langue des graphiques interactifs** : info-bulles en français (activé) — à confirmer.

*Une fois ces points validés, l'ensemble des graphiques est régénéré automatiquement en quelques
minutes (chaîne de production scriptée).*
