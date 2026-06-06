# Axe 2 — L'Europe heureuse et son déclin relatif
### Note de synthèse · Tribune PZ-0626 · données extraites le 06/06/2026

## Ce que montrent les données

**Le décrochage économique européen est massif et continu.** La part de l'**UE-27 dans le PIB
mondial** (en dollars courants) est passée de **~28 % en 1990 à ~18 % en 2024**, soit une perte de
plus de dix points en trois décennies. Sur la même période, les **États-Unis se sont maintenus
autour de 26 %**, tandis que la **Chine bondissait de 1,6 % à ~17 %**, dépassant l'Union européenne
à partir de 2021. Le recul européen n'est donc pas un effet d'optique lié à la montée chinoise : c'est
un déclassement en valeur relative que les États-Unis, eux, n'ont pas connu.

**L'écart de richesse par habitant avec les États-Unis est durablement installé.** En PPA, le
PIB/habitant américain dépasse en 2024 celui de l'**Allemagne de +17 %**, de la **France de +37 %**,
de l'**Italie de +38 %** et de l'**Espagne de +48 %**. Cet écart US/France est resté quasi stable
depuis 2000 (≈ 40 % → 37 %) : l'Europe ne rattrape pas, elle décroche au rythme de l'économie
mondiale.

**Mais ce décrochage ne se lit pas dans la qualité de vie déclarée.** Sur les scores Better Life
Index, les pays européens **égalent ou surpassent les États-Unis** sur trois des quatre dimensions
étudiées : équilibre travail-vie (USA : 4,1/10 — le plus faible de l'échantillon), sécurité, et
satisfaction de vie pour l'Allemagne (8,0). Les États-Unis ne dominent nettement que sur le
**logement** (8,6/10 — surfaces et pièces par habitant). L'Europe « achète » donc, à PIB moindre,
un panier de bien-être au moins équivalent.

**Le temps libre est un arbitrage explicite.** Un travailleur américain effectue **~1 790 heures/an**
contre **~1 490 en France** et **~1 335 en Allemagne** (2023) — près de **450 heures d'écart**, soit
plus de onze semaines de 40 heures. L'écart de PIB s'explique en partie par un choix de société :
moins d'heures travaillées, davantage de temps hors travail.

## Tensions et corrélations remarquables

- **Le « bien-être à crédit de croissance »** : l'Europe maintient un niveau de vie élevé alors que
  son poids productif s'érode. La question de la tribune — ce bien-être est-il soutenable ? — trouve
  ici son terrain le plus concret.
- **Arbitrage travail/loisir** : une partie de l'écart de PIB/habitant US-Europe est un choix (moins
  d'heures), pas une pure infériorité de productivité — nuance essentielle à porter dans la tribune.
- **Découplage richesse / qualité de vie** : la corrélation PIB↔bien-être, forte entre pays pauvres et
  riches, se dissout au sein du club des pays riches.

## Limites des données

- **PIB en dollars courants** : la part dans le PIB mondial dépend du taux de change €/$. Une partie du
  recul européen post-2010 reflète l'appréciation du dollar, non un effondrement réel. À mentionner.
- **Agrégat « UE-27 »** : composition actuelle rétropolée (les 27 membres d'aujourd'hui sur tout
  l'historique) — cohérent dans le temps mais à préciser.
- **Better Life Index** : scores reconstitués par normalisation min-max sur l'OCDE (méthode officielle
  du BLI) à partir de l'édition archivée (2020, dernière disponible en libre accès) ; les valeurs sont
  des ordres de grandeur comparatifs, non des mesures absolues. Indicateurs bruts fournis pour
  transparence.
- **Heures travaillées** : définitions nationales hétérogènes (temps partiel, indépendants) ;
  comparaisons de niveau à prendre avec précaution, l'évolution étant plus robuste que le niveau.

## Visualisations livrées
- `axe2_part_pib_mondial` — aires empilées, part du PIB mondial par zone, 1990-2024.
- `axe2_ecart_pib_bli` — double panneau : PIB/hab USA vs Europe + scores Better Life Index.
- `axe2_heures_travaillees` — heures travaillées annuelles par travailleur, 2000-2023 (complément).

*Sources primaires : Banque mondiale (WDI) ; OCDE Better Life Index (DF_BLI) ; OCDE / Our World in Data (heures travaillées).*
