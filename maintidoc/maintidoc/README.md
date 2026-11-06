# MaintiDoc — Livrable 1 : cadrage, corpus et architecture

Module **IA générative multimodale**, EMSI 2026 — Enseignante : Prof. Mariam Cherrabi

**Équipe AHMITO-JOURAAI**

| Membre | Rôle principal |
|---|---|
| Douaa Ahmito | Corpus et inventaire, ingestion et recherche, reranker, vérificateur de citations, évaluation, interface |
| Mohamed Nacer Jouraai | API et contrôle d'accès, orchestrateur LangGraph, serveur MCP et tickets, sécurité, déploiement |

## Objectif du projet

MaintiDoc est un assistant documentaire multimodal et agentique pour la maintenance biomédicale (pompes à perfusion InfuPro, moniteurs patients VitaScan, tous fictifs). À partir d'une question et d'une photo, il retrouve les passages et figures autorisés, répond en citant le document, la page et l'élément, consulte l'historique d'un équipement par un outil MCP et prépare un brouillon de ticket, créé seulement après approbation humaine.
C'est une aide documentaire : il ne pilote aucun équipement, ne garantit aucun diagnostic et ne donne aucune indication clinique.

## Contenu du ZIP

| Élément | Contenu |
|---|---|
| `L1_MaintiDoc_AHMITO-JOURAAI_Rapport.pdf` | Rapport complet : cadrage, corpus, architecture, flux de données et accès, risques, planning (14 pages hors annexes) |
| `L1_MaintiDoc_AHMITO-JOURAAI_LienGitHub.txt` | URL du dépôt GitHub de l'équipe |
| `README.md` | Ce fichier |
| `L1_MaintiDoc_AHMITO-JOURAAI_Corpus/` | 40 documents synthétiques (20 par famille), `inventaire.csv`, `prompts_corpus.md` |

## Structure du dépôt

```
maintidoc/
├── README.md
├── .gitignore
├── docs/
│   └── diagrammes/        sources des six figures du rapport (SVG)
└── corpus/
    ├── inventaire.csv     registre : une ligne par document, 20 colonnes
    ├── prompts_corpus.md  prompts P01 à P14, outil et date
    ├── documents/
    │   ├── famille_1/     pompes à perfusion (PDF)
    │   └── famille_2/     moniteurs patients (PDF)
    └── images/            photos de panneaux, voyants et écrans
```

## Le corpus en bref

- 40 documents en français, tous synthétiques (provenance et licence : `synthetique`), générés à partir d'une fiche maître unique (équipements, 20 codes d'alarme, 19 interventions).
- 33 documents avec éléments visuels, 2 scannés, 2 contradictoires (calibration v1 et v2), 1 piégé (injection de prompt), 3 ambigus.
- Les 32 PDF sont générés par script à partir de la fiche maître ; les 8 images sont rendues par code et les 2 scans sont simulés (voir `remarques` dans l'inventaire). `check_corpus.py` vérifie pagination, codes, identifiants et tickets (0 erreur).
- Groupes d'accès fictifs : `techniciens_perfusion`, `techniciens_monitorage`, `responsables`.
- Chaque document est relié à son prompt dans la colonne `outil_ia` de l'inventaire.

Aucun secret (clé d'API, mot de passe) n'est présent dans le ZIP ni dans le dépôt.
