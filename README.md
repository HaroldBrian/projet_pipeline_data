# Projet pipeline data — Mobilité urbaine

Petit pipeline ETL en Python : lecture d'un fichier CSV de trajets, contrôle et nettoyage des données, calcul d'indicateurs, graphiques, puis export CSV et chargement dans une base SQLite.

## Organisation

| Fichier | Rôle |
|---|---|
| `mobilite.csv` | Données brutes |
| `traitement.py` | Import, contrôle qualité et nettoyage |
| `analyse.py` | Calcul des indicateurs (Pandas + NumPy) |
| `graphiques.py` | Graphiques Matplotlib (`.png`) |
| `chargement_bdd.py` | Export `resultats.csv` et chargement dans `mobilite.db` |
| `main.py` | Exécute le pipeline complet |

## Lancer le projet

```bash
pip install -r requirements.txt
python main.py
```

## Nettoyage effectué

- suppression des doublons sur `id` ;
- normalisation du texte (`BUS` → `Bus`, espaces) ;
- durée manquante remplacée par la médiane des durées positives ;
- suppression des durées/distances négatives ou nulles ;
- conversion des types (`id` et `duree` en entier, `date_trajet` en date).
