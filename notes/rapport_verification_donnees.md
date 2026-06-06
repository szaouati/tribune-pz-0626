# Rapport de vérification des données — Tribune PZ-0626
### Contrôle croisé indépendant · 06/06/2026

Méthode : 4 contrôleurs indépendants (un par axe) ont relu les fichiers livrés et confronté les
chiffres clés aux sources publiques de référence (Banque mondiale, FMI, OCDE, World Happiness Report,
General Social Survey, EFPIA, SIPRI), suivis d'une synthèse adversariale. **35 points** contrôlés.

## Récapitulatif

| Axe | Contrôles | OK | À documenter | Résolu |
|---|---|---|---|---|
| Axe 1 — Bonheur vs économie | 11 | 8 | 3 | ✓ |
| Axe 2 — Europe & déclin | 10 | 9 | 1 | ✓ |
| Axe 3 — Composants du bonheur | 4 | 4 | 0 | ✓ |
| Axe 4 — Arbitrages | 10 | 8 | 2 | ✓ |
| **Total** | **35** | **29 (83 %)** | **6** | **✓** |

**Verdict : fiabilité élevée.** Les ordres de grandeur, ratios et sommes bouclent et concordent avec
les sources publiques. Aucune erreur de donnée n'a été confirmée après instruction des alertes.

## Traitement des alertes

1. **Dette publique Japon (214 % en 2024)** — *signalé comme possible erreur (~252 % attendu).*
   → **Vérifié : donnée correcte.** Elle correspond exactement au dernier millésime du FMI (WEO,
   datamapper, `GGXWDG_NGDP`). Le « ~250 % » correspond à des millésimes antérieurs / à d'autres
   périmètres. **Action prise** : note explicite ajoutée (millésime + dette brute vs nette).

2. **Lacunes WHR États-Unis** — *signalé : 2013, 2022, 2023 manquants.*
   → **Vérifié : seule 2013 manque** (2022 et 2023 sont bien présents). Lacune unique et marginale,
   héritée de la source OWID. Sans impact sur les graphiques (basés sur 2024).

3. **GSS post-2021 (série courte)** — *3 observations, 2023 absente (GSS biennal).*
   → **Action prise** : la note de l'Axe 1 distingue désormais explicitement le **paradoxe d'Easterlin**
   (stabilité 1972-2018) du **choc COVID** post-2020, à ne pas confondre.

4. **Easterlin vs choc COVID** — *ne pas attribuer l'effondrement post-2020 au seul Easterlin.*
   → **Action prise** : reformulation dans la note de l'Axe 1 (cf. ci-dessus).

5. **Échelle Better Life Index** — *crainte d'échelles hétérogènes.*
   → **Vérifié : faux positif.** Les scores livrés sont **tous normalisés 0-10** (méthode BLI min-max),
   les écarts entre dimensions (logement 8,6 ; équilibre travail-vie 4,1) reflètent la réalité, pas une
   incohérence d'échelle. Indicateurs bruts fournis pour transparence.

6. **Défense Europe ~1,5 %** — *Allemagne (1,49 %) et Espagne (1,47 %) légèrement sous 1,5 %.*
   → **Action prise** : formulation nuancée (« autour de 1,5 %, plusieurs pays en-dessous de la cible
   OTAN »).

## Recommandations de publication
- Conserver la mention du **millésime** des sources (les agrégats FMI/WEO sont révisés).
- Présenter le décrochage du bonheur US post-2020 comme un **choc** distinct du paradoxe d'Easterlin.
- Toujours afficher la **source + date d'extraction** sous chaque graphique (déjà en place).

*Conclusion : base de données exploitable pour publication, sous réserve des précautions de
présentation ci-dessus, désormais intégrées aux notes de synthèse.*
