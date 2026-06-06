# Axe 1 — Bonheur déclaré vs performance économique
### Note de synthèse · Tribune PZ-0626 · données extraites le 06/06/2026

## Ce que montrent les données

**Le bonheur croît avec le revenu, mais à rendement décroissant.** En 2024, le nuage de points
bonheur/PIB confirme une corrélation positive mais fortement concave (logarithmique) : passer de
5 000 à 40 000 $ de PIB/habitant fait gagner plusieurs points de bonheur ; passer de 60 000 à
100 000 $ n'en fait gagner presque aucun. Les **pays nordiques** dominent le classement (Finlande
**7,74**, Danemark 7,52, Islande 7,52, Suède 7,35, Norvège 7,26) sans être les plus riches : la
Norvège mise à part (102 k$ PPA, dopé par les hydrocarbures), ils se situent **en-dessous des
États-Unis en PIB/habitant** (85,8 k$) tout en le devançant nettement en bonheur déclaré.

**Le cas américain est emblématique de la déconnexion.** Les États-Unis affichent le 2ᵉ PIB/habitant
de l'échantillon mais un score de bonheur (**6,72**) inférieur à l'Allemagne (6,75) et désormais sorti
du Top 20 mondial du *World Happiness Report*. La richesse marginale n'y « achète » plus de
bien-être déclaré.

**Le paradoxe d'Easterlin, vérifié sur 50 ans.** Entre 1972 et 2024, le **PIB réel par habitant
américain a été multiplié par ~2,5** (26 700 → 66 400 $ constants 2015). Sur la même période, la
part d'Américains se déclarant « très heureux » est restée **remarquablement stable autour de
30-36 %** jusqu'en 2018 (30,3 % en 1972 ; 31,5 % en 2018), avant de chuter à 19 % en 2021 puis de
remonter partiellement (23,4 % en 2024). La croissance de long terme ne s'est pas traduite par une
hausse du bonheur moyen — cœur de l'argument de la tribune.

## Tensions et corrélations remarquables

- **Effet de seuil / saturation** : au-delà de ~40 000 $ PPA, la pente bonheur/revenu s'aplatit. Le
  débat n'est donc pas « le PIB ne compte pas » mais « le PIB compte de moins en moins ».
- **Prime institutionnelle nordique** : à revenu comparable (voire inférieur), les pays nordiques
  « sur-performent » en bonheur — un capital de confiance, d'égalité et de services publics qui
  n'apparaît pas dans le PIB.
- **Décrochage du bien-être subjectif américain post-2010** : la baisse tendancielle (puis le
  décrochage de 2021) suggère que d'autres déterminants (santé mentale, isolement, défiance)
  pèsent davantage que le revenu.

## Limites des données

- **Échelle de Cantril (WHR)** : moyenne mobile sur 3 ans, sensible au contexte de l'enquête ;
  comparaisons inter-pays à interpréter en ordre de grandeur, non au centième.
- **Bhoutan** : sorti du Gallup World Poll après 2018 — point daté (score ~5,1 en 2018), non
  comparable aux valeurs 2024. Le « Bonheur National Brut » bhoutanais relève d'une méthodologie
  distincte (indice multidimensionnel), non strictement comparable à l'échelle de Cantril.
- **Rupture GSS 2021 — à distinguer du paradoxe d'Easterlin** : la chute de la part « très heureux »
  après 2018 reflète un **choc exogène** (pandémie **+** refonte du protocole, passage partiel au web)
  et repose sur une série courte (2021, 2022, 2024). Le paradoxe d'Easterlin proprement dit est porté
  par la **stabilité 1972-2018** (≈ 30-36 %) malgré le doublement du revenu — c'est cette tendance
  longue, et non le décrochage COVID, qu'il faut mettre en avant dans la tribune.
- **PIB PPA en $ courants** : non corrigé de l'inflation entre années — pertinent pour une comparaison
  transversale (2024), à ne pas lire comme une série temporelle réelle (pour cela : série « PIB réel »
  en $ constants, utilisée pour l'Easterlin).

## Visualisations livrées
- `axe1_bulles_bonheur_pib` — nuage de bulles bonheur × PIB/hab PPA, taille ∝ population (2024).
- `axe1_easterlin_pib_bonheur` — double axe PIB réel/hab vs « très heureux », USA 1970-2024.

*Sources primaires : World Happiness Report / Gallup World Poll (via Our World in Data) ;
Banque mondiale (WDI) ; General Social Survey, NORC (microdonnées 1972-2024, var. HAPPY pondérée WTSSPS).*
