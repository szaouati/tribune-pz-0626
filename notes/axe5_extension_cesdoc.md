# Axe 5 — Étendre le test causal : liste de données (CESDOC / OCDE) + note client

## Objectif

Le test de causalité « densité → maillage/dépense » est aujourd'hui établi **pour la seule France**
(96 départements, corrélations −0,74 écoles / −0,69 sécurité). Pour le rendre robuste, deux chantiers :

1. **Répliquer le gradient pour l'Allemagne et les Pays-Bas** → démonstration sur 3 pays, pas un seul.
2. **Adosser le mécanisme à la littérature** (« coûts de la dispersion ») → passer de « forte corrélation »
   à « mécanisme documenté ».

Par région (Kreis allemand, gemeente/COROP néerlandais), il faut le même triptyque que pour la France :
**densité × nombre d'équipements publics/hab × dépense publique locale/hab (idéalement par fonction).**

---

## 1. Données à récupérer

### ⚑ Ce que la sonde open data a déjà montré (07/06/2026)

- **OCDE — dépense infranationale par fonction (COFOG) : EN ACCÈS LIBRE**, via `sdmx.oecd.org`
  (Data Explorer, dataflow `OECD.CFE.RDG,DSD_DASHBOARD@COFOG`). FR/DE/NL présents, fonctions GF01–GF10,
  secteurs *local* (`S1313`) et *régional/État* (`S1312`), en % du PIB et en % de la dépense.
  **→ pas besoin de CESDOC pour cette brique.** *Mais* c'est un agrégat **national par niveau de
  gouvernement**, **pas par région** → il ne donne pas le gradient interne ; et il est **faussé par la
  structure de décentralisation** : ex. dépense d'éducation des administrations *locales* (% PIB, 2022)
  FR 1,6 / DE 1,5 / **NL 3,9** — parce qu'en Allemagne l'école est financée par les *Länder* (+3,3 pts),
  aux Pays-Bas par les communes. (Ordre & sécurité ≈ 0,34 % partout.)
- 🇩🇪 **Allemagne — GENESIS (regionalstatistik.de) fermé sans compte** (API → 404 / inscription requise).
  Or c'est *le* bon terrain de réplication (Kreise de 36 à 4 800 hab/km²). → inscription gratuite GENESIS,
  ou repli OCDE/littérature.
- 🇳🇱 **Pays-Bas — CBS StatLine ouvert** (OData, table `70072ned` : densité + écoles par région), mais
  NL n'a quasi aucune région peu dense (COROP ≥ 142 hab/km²) → gradient interne **peu informatif** : NL
  joue le rôle de « témoin » (pas de problème de dispersion à mesurer).

**Conséquence pour le plan CESDOC** : l'apport résiduel se resserre sur **(1) la littérature** (le
principal) et **(2) la réplication du gradient en Allemagne** (données régionales par Kreis). La
comparaison harmonisée des dépenses par fonction, elle, est déjà faisable en open data.

### A. À tenter d'abord en OPEN DATA (sans CESDOC)

| Pays | Source ouverte | Contenu | Accès |
|---|---|---|---|
| **Allemagne** | **Regionaldatenbank Deutschland** (regionalstatistik.de) | « Rechnungsergebnisse der kommunalen Haushalte » (dépenses communales/Kreis par fonction) ; nombre d'écoles par Kreis (Schulstatistik) | API GENESIS REST/JSON ; CSV/XLSX |
| **Pays-Bas** | **CBS StatLine** | « Gemeentefinanciën / Gemeenterekeningen » (dépenses par commune et par *taakveld*/fonction) ; écoles par commune | API OData (`opendata.cbs.nl`) |
| **Les 3** | **Eurostat** `demo_r_d3dens` | densité par région NUTS3 | déjà branché dans le pipeline |

> Le gradient DE/NL est **techniquement faisable en open data**, mais (a) laborieux et en langue locale,
> (b) trois cadres comptables non directement comparables. D'où l'intérêt de l'OCDE ci-dessous.

### B. CESDOC → OCDE iLibrary : la **comparabilité harmonisée** (valeur ajoutée réelle)

| Base (OCDE iLibrary) | Ce qu'on y prend | Pourquoi CESDOC |
|---|---|---|
| **OECD Fiscal Decentralisation Database** | Dépense des administrations **infranationales par fonction COFOG**, par niveau de gouvernement, 1995-2022, FR/DE/NL | ⚑ **Déjà OPEN** via OECD Data Explorer (`OECD.CFE.RDG,DSD_DASHBOARD@COFOG`) — *testé, OK sans compte*. CESDOC n'ajoute ici que la doc/confort. **Limite** : agrégat national par niveau de gouvernement, pas par région → inutile pour le gradient interne. |
| **OECD Regional Statistics — « Subnational government structure and finance »** | Dépense/investissement infranational, structure des collectivités, par pays (TL2/TL3 pour certains) | Situer FR/DE/NL ; vérifier la granularité régionale disponible |
| **OECD Regions & Cities (TL3)** | Population, densité, PIB régional, parfois investissement public régional | Variables de contrôle régionales harmonisées |

### C. CESDOC → littérature (étayer le mécanisme causal)

Bases : **Econlit**, **OpenAlex** (ouvert), **Academic Search Premier**, **OCDE iLibrary** (working papers),
**ProQuest**, **Cairn** (si dispo). Requêtes à lancer :
- *« cost of (low) population density / sparsity » + « local public services / public provision »*
- *« economies of scale in local government » / « optimal municipality (jurisdiction) size »*
- *« fragmentation communale » / « millefeuille territorial » + « coût »*
- Rapports : **Cour des comptes**, **France Stratégie**, **CAE**, **OCDE** sur le coût du maillage communal.

Objectif : 2-3 références solides établissant « faible densité → surcoût unitaire des services publics locaux ».

### D. Limites résiduelles à garder en tête
- **Comparabilité des fonctions** : compétences décentralisées différentes (social au département en FR, aux
  Länder/Kreise en DE…). Le COFOG OCDE atténue mais ne supprime pas le biais.
- **Granularité** : l'OCDE est souvent au niveau infranational *agrégé national*, pas par région fine ; pour
  le **gradient interne** DE/NL, ce sera surtout regionalstatistik.de (DE) et CBS StatLine (NL).

---

## 2. Note pour le client (à recopier / adapter)

> **Objet : suite « coût du territoire » — ce que je ferai avec l'accès aux bases Paris 1**
>
> Bonjour,
>
> Un point sur la piste « gestion du territoire ». La base est faite (France / Allemagne / Pays-Bas), avec
> un résultat solide : la France a le maillage public le plus dense — communes, écoles, gendarmeries par
> habitant — et la dépense publique la plus lourde rapportée au PIB. J'ai même pu **démontrer le mécanisme
> à l'intérieur de la France** : plus un département est peu peuplé, plus il porte d'équipements publics par
> habitant (corrélation très nette sur les 96 départements).
>
> Il reste une limite que je veux lever avant publication : cette démonstration « de cause à effet » n'est
> faite que pour la France. Avec l'accès aux bases de Paris 1 (notamment l'OCDE), je vais :
>
> 1. **répliquer le test en Allemagne** — le pays le plus comparable, et qui présente comme la France de
>    vraies zones très peu denses —, à partir de ses statistiques régionales par arrondissement ;
> 2. **adosser le mécanisme à deux ou trois références académiques** sur les « coûts de la dispersion », pour
>    que la tribune ne repose pas que sur nos propres corrélations.
>
> J'ai déjà vérifié la disponibilité des données : l'essentiel est en accès ouvert (j'ai même pu récupérer les
> dépenses publiques régionales comparées de l'OCDE, qui montrent que l'organisation des compétences diffère
> beaucoup d'un pays à l'autre). L'accès aux bases de Paris 1 servira surtout à **sourcer la littérature** et à
> compléter le cas allemand. Je reviens vers toi avec la version consolidée dès que possible.
>
> Bien à toi,
> Sacha
