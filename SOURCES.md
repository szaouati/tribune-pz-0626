# Documentation des sources — Tribune PZ-0626
### Toutes les séries, leurs sources primaires, codes et dates d'extraction

**Date d'extraction unique : 06/06/2026.** Collecte programmatique via API officielles (reproductible).
Le détail figure aussi dans la feuille « Métadonnées » de chaque classeur Excel et dans
`data/raw/registre_sources_propre.csv`.

## Banque mondiale — World Development Indicators (API `api.worldbank.org/v2`)
| Série | Indicateur | Axe |
|---|---|---|
| Score de bonheur (relais OWID) | — | 1 |
| PIB/hab PPA (\$ intl courants) | `NY.GDP.PCAP.PP.CD` | 1, 2 |
| Population totale | `SP.POP.TOTL` | 1 |
| PIB réel/hab (\$ const. 2015) | `NY.GDP.PCAP.KD` | 1 |
| PIB courant (\$US) par zone | `NY.GDP.MKTP.CD` | 2 |
| Espérance de vie à la naissance | `SP.DYN.LE00.IN` | 3 |
| Dépenses publiques de santé (% PIB) | `SH.XPD.GHED.GD.ZS` | 3 |
| Exposition PM2.5 (µg/m³) | `EN.ATM.PM25.MC.M3` | 3 |
| Industrie manufacturière (% PIB) | `NV.IND.MANF.ZS` | 3 |
| Taux de fécondité | `SP.DYN.TFRT.IN` | 4 |
| FBCF / investissement (% PIB) | `NE.GDI.FTOT.ZS` | 4 |
| Dépenses militaires (% PIB, source SIPRI) | `MS.MIL.XPND.GD.ZS` | 4 |

→ `https://data.worldbank.org/indicator/<CODE>`

## FMI — World Economic Outlook (DataMapper API)
| Série | Indicateur | Axe |
|---|---|---|
| Dette publique brute (% PIB) | `GGXWDG_NGDP` | 4 |
| Solde primaire (% PIB) | `pb` | 4 |

→ `https://www.imf.org/external/datamapper/<CODE>`  ·  *millésime : dernier disponible au 06/2026.*

## OCDE
| Série | Source / dataflow | Axe |
|---|---|---|
| Better Life Index (scores 0-10, 4 dimensions) | SDMX archive `OECD,DF_BLI` (édition 2020) | 2 |
| R&D pharmaceutique des entreprises (industrie C21) | ANBERD `DSD_ANBERD@DF_ANBERDi4` (USD PPA) | 3 |
| Heures travaillées annuelles | via OWID (`annual-working-hours-per-worker`) | 2 |

→ `https://data-explorer.oecd.org` · `https://sdmx.oecd.org`

## Eurostat — API dissemination (JSON-stat) · axe 5 (France / Allemagne / Pays-Bas)
| Série | Dataset / clé | Axe |
|---|---|---|
| Dépense publique par fonction (COFOG) : total, éducation (`GF09`), ordre & sécurité (`GF03`) | `gov_10a_exp` (S13, na_item `TE`, unités `PC_GDP` + `MIO_EUR`) | 5 |
| Densité de population par région NUTS3 | `demo_r_d3dens` | 5 |
| Population au 1ᵉʳ janvier (nationale / NUTS3) | `demo_pjan` / `demo_r_pjanaggr3` | 5 |
| Effectifs de police (pour 100 000 hab) | `crim_just_job` (CITP-08 `OC5412`, unité `P_HTHAB`) | 5 |
| Parités de pouvoir d'achat du PIB (→ SPA/hab) | `prc_ppp_ind` (`na_item=PPP_EU27_2020`, `ppp_cat=GDP`) | 5 |
| Élèves inscrits en primaire (CITE 1, harmonisé) | `educ_uoe_enra01` (`isced11=ED1`) | 5 |

→ `https://ec.europa.eu/eurostat/databrowser/product/page/<DATASET>`

## Open data France — test de causalité interne (axe 5, par département)
| Série | Source / accès | Axe |
|---|---|---|
| Équipements publics par département (écoles `C107/C108/C109`, collège `C201`, lycées `C301/C302/C303`, police `A101`, gendarmerie `A104`) | **INSEE — Base permanente des équipements (BPE) 2024**, API Mélodi `DS_BPE` | 5 |
| Dépense communale par habitant, par département | **OFGL** (`data.ofgl.fr`, Opendatasoft v2.1, `ofgl-base-communes`, 2023) | 5 |
| Superficie des départements (densité) | **geo.api.gouv.fr** (communes, champ `surface`, agrégé) | 5 |

→ INSEE Mélodi : `https://api.insee.fr/melodi` · OFGL : `https://data.ofgl.fr` · `https://geo.api.gouv.fr`

## Our World in Data (relais de séries primaires)
| Série | Grapher | Source amont | Axe |
|---|---|---|---|
| Échelle de Cantril (bonheur) | `happiness-cantril-ladder` | World Happiness Report / Gallup | 1 |
| Heures travaillées | `annual-working-hours-per-worker` | OCDE / PWT | 2 |

→ `https://ourworldindata.org/grapher/<slug>.csv`

## Sources spécialisées
| Série | Source | Détail | Axe |
|---|---|---|---|
| Bonheur déclaré US « very happy » (1972-2024) | **General Social Survey**, NORC (Univ. Chicago) | Microdonnées GSS7224 R3, var. `HAPPY`, pondération `WTSSPS` — % calculé par nos soins | 1 |
| Origine des nouvelles substances actives (2024) | **EFPIA**, *The Pharmaceutical Industry in Figures 2025* | Comptage par nationalité de la société mère | 3 |
| Nombre de communes (unités administratives locales) | **INSEE** (FR, 34 935 / 2024), **Destatis** (DE, 10 753), **CBS** (NL, 342) | Compilation — pas d'API unique comparable | 5 |
| Nombre d'écoles du 1ᵉʳ degré | **DEPP** (FR), **Destatis** (DE, Grundschulen), **CBS/DUO** (NL, basisscholen) | Périmètres non strictement comparables (maternelle FR incluse) | 5 |

→ GSS : `https://gss.norc.org` · EFPIA : `https://www.efpia.eu` · INSEE/Destatis/CBS/DEPP : instituts nationaux de statistique

## Notes de traçabilité
- Les fichiers bruts (réponses API, PDF EFPIA, microdonnées GSS) sont conservés dans `data/raw/`.
- Chaque série computée par nos soins (GSS %, scores BLI normalisés, parts de PIB, agrégats R&D par
  zone) est **entièrement reproductible** via les scripts du dossier `scripts/`.
- Périmètres particuliers documentés dans les notes : agrégat « UE-27 » (composition actuelle
  rétropolée), « Europe » R&D (UE+AELE, hors Royaume-Uni non couvert par ANBERD), dette japonaise
  (brute, dernier millésime FMI).
