# Axe 3 — Composants du bonheur et leurs sous-jacents économiques
### Note de synthèse · Tribune PZ-0626 · données extraites le 06/06/2026

## Ce que montrent les données

**Le « free rider » de l'innovation : les États-Unis paient, le monde en profite.** La R&D
pharmaceutique des entreprises américaines a été **multipliée par dix en vingt ans** (≈ 13 Md$ PPA
en 2000 → **130 Md$ en 2023**). En 2023, elle dépasse à elle seule l'Europe (UE+AELE : ~34 Md$), le
Japon (~16 Md$) et la Chine (~33 Md$) **réunis**. Or l'espérance de vie — bénéfice ultime de cette
innovation — progresse partout, y compris dans les pays qui investissent peu.

**Le paradoxe sanitaire américain.** Les États-Unis dépensent le plus (R&D pharmaceutique massive,
dépenses de santé totales ≈ 17 % du PIB, les plus élevées de l'OCDE) mais affichent **l'espérance de
vie la plus basse des grandes économies avancées : 78,4 ans en 2023**, contre 84,0 au Japon, 82,8 en
France et 81,0 en Allemagne. La France « vit » 4,4 années de plus que les États-Unis tout en
dépensant beaucoup moins. Le lien dépense → longévité est tout sauf mécanique.

**Le basculement de l'innovation vers l'Asie.** Symbole fort : en **2024, sur 81 nouvelles
substances actives** lancées dans le monde, **28 sont d'origine chinoise, 25 américaine et seulement
18 européenne**. L'Europe, premier originateur mondial de nouveaux médicaments en 2000, est
désormais **reléguée à la 3ᵉ place**. Le modèle européen consomme l'innovation plus qu'il ne la
produit.

**Le coût environnemental délocalisé.** L'exposition aux particules fines PM2.5 illustre l'envers du
bien-être occidental : la Chine, « atelier du monde », respire un air 3 à 6 fois plus pollué (~50 µg/m³)
que les économies de services occidentales (~8-12 µg/m³) — toutes restant au-dessus du seuil OMS de
5 µg/m³. Une partie de la qualité de vie occidentale repose sur une industrie (et sa pollution)
exportée.

## Tensions et corrélations remarquables

- **Bien-être présent / capital d'innovation** : l'espérance de vie élevée de l'Europe repose en partie
  sur des médicaments dont la R&D est financée ailleurs (modèle de marché américain). C'est l'exemple
  pharmaceutique au cœur de la thèse de la tribune.
- **Découplage dépense/résultat aux États-Unis** : champion de l'investissement santé, lanterne rouge
  de la longévité — un signal que le bonheur (longévité) n'est pas qu'une affaire de moyens financiers.
- **Désindustrialisation = air pur, mais dépendance** : les pays qui ont exporté leur industrie
  respirent mieux mais dépendent d'autrui pour produire — biens, médicaments, pollution comprise.

## Limites des données

- **R&D pharma (ANBERD)** : R&D des entreprises de l'industrie pharmaceutique (ISIC C21). Le
  **Royaume-Uni n'est pas couvert** par ANBERD : l'agrégat « Europe » est légèrement sous-estimé.
  USD PPA prix courants (non corrigés de l'inflation).
- **Origine des nouvelles molécules** : comptage selon la nationalité de la société mère (EFPIA 2025) ;
  une molécule « chinoise » peut être co-développée ou commercialisée par des multinationales. Année
  unique (2024) — tendance robuste, niveau annuel volatil.
- **Espérance de vie** : indicateur synthétique sensible à des facteurs hors santé (violences, opioïdes,
  obésité aux États-Unis) — la sous-performance américaine n'est pas imputable à la seule pharmacie.
- **PM2.5** : exposition moyenne modélisée (satellite + stations), disponible jusqu'à 2020.
- **Dépenses publiques de santé** : la comparaison USA/Europe doit intégrer la part privée, très élevée
  aux États-Unis (dépense **totale** ≈ 17 % du PIB).

## Visualisations livrées
- `axe3_rd_esperance_vie` — combiné : R&D pharma (barres) vs espérance de vie (courbes), par zone, 2000-2023.
- `axe3_origine_molecules` — origine géographique des nouvelles molécules (2024).
- `axe3_pm25_air` — exposition aux PM2.5, 1990-2020 (complément désindustrialisation).

*Sources primaires : OCDE (ANBERD) ; Banque mondiale (WDI) ; EFPIA, The Pharmaceutical Industry in Figures 2025 ; OMS.*
