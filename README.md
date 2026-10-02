# Pipeline de données — Mobilité urbaine

Projet de synthèse Python : un pipeline **ETL** qui lit des données de trajets urbains, les nettoie, les analyse, puis les enregistre dans une base de données.

## Structure

```
projet_pipeline_data/
├── mobilite.csv        # Données brutes
├── main.py             # Lance le pipeline complet
├── traitement.py       # Import, contrôle et nettoyage
├── analyse.py          # Indicateurs (Pandas + NumPy)
├── graphiques.py       # Graphiques Matplotlib
├── chargement_bdd.py   # Export CSV + base SQLite
├── bonus/              # Bonus 1 (MongoDB), 3 (PySpark), 4 (IA)
└── files/              # Fichiers générés (CSV, base, graphiques, JSON...)
```

## Installation

```bash
# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate

# Puis, dans les deux cas
pip install -r requirements.txt
```

## Lancer le pipeline

```bash
python main.py
```

Chaque étape s'affiche dans le terminal, et les résultats sont enregistrés dans `files/`.

**Nettoyage effectué :** suppression des doublons, normalisation du texte (`BUS` → `Bus`), durée manquante remplacée par la médiane, suppression des durées négatives et conversion des types.

**Résultat :** 14 trajets conservés sur 16. Distance totale : 75,90 km. Durée moyenne : 21,57 min. Transport le plus utilisé : le vélo.

## Bonus

Les bonus se lancent depuis la racine du projet.

### Bonus 1 — MongoDB

Les données nettoyées sont exportées en JSON, puis chargées dans la base `mobilite`, collection `trajets`.

**1. Démarrer un serveur MongoDB** (sur `localhost:27017`) :

- **Windows :** téléchargez _MongoDB Community Server_ sur [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community). Pendant l'installation, cochez **« Install MongoD as a Service »** : le serveur démarrera alors automatiquement. MongoDB Compass est proposé dans le même installateur.
- **Mac :**
  ```bash
  brew tap mongodb/brew
  brew install mongodb-community
  brew services start mongodb-community
  ```
- **Avec Docker (Windows, Mac ou Linux) :**
  ```bash
  docker run -d --name mongodb -p 27017:27017 mongo
  ```

**2. Lancer le bonus :**

```bash
python bonus/bonus1_mongodb.py
```

Pour voir les données dans **MongoDB Compass**, connectez-vous à `mongodb://localhost:27017`, puis ouvrez `mobilite` > `trajets`.

> `main.py` lance aussi ce bonus. Si MongoDB n'est pas démarré, un message s'affiche et le pipeline continue.

### Bonus 3 — PySpark

Le script refait le nettoyage et l'analyse avec PySpark, et retrouve les mêmes résultats que Pandas. **Java 17 ou plus récent** doit être installé.

```bash
python bonus/bonus3_pyspark.py
```

### Bonus 4 — IA (Google Gemini)

Gemini rédige un commentaire des résultats, enregistré dans `files/commentaire_ia.txt`.

1. Créez une clé API sur [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
2. À la racine du projet, créez un fichier `.env` contenant :
   ```
   GOOGLE_API_KEY=votre_clé_ici
   ```
3. Lancez :
   ```bash
   python bonus/bonus4_ia.py
   ```

> Si l'IA ne répond pas, le script affiche un commentaire de secours, sans IA. Le fichier `.env` n'est pas envoyé sur Git.
