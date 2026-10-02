#Bonus 1 : CSV -> Pandas -> nettoyage -> JSON -> MongoDB

import os
import sys
import json
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Accès au dossier parent pour réutiliser traitement.py et mobilite.csv
DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DOSSIER_PROJET)

from traitement import importer_donnees, controller_et_nettoyer, DOSSIER_FICHIERS

def exporter_json(df, nom_fichier=os.path.join(DOSSIER_FICHIERS, "resultats.json")):
    print("=== BONUS 1. EXPORT JSON ===")
    df = df.copy()
    df['date_trajet'] = df['date_trajet'].astype(str)  # date au format "AAAA-MM-JJ"
    df.to_json(nom_fichier, orient="records", indent=2, force_ascii=False)
    print(f"-Fichier généré avec succès : '{os.path.relpath(nom_fichier)}'\n")

def charger_dans_mongodb(nom_fichier=os.path.join(DOSSIER_FICHIERS, "resultats.json"), url="mongodb://localhost:27017/",
                         nom_bdd="mobilite", nom_collection="trajets"):
    print("=== BONUS 1. CHARGEMENT DANS MONGODB ===")

    with open(nom_fichier, encoding="utf-8") as f:
        trajets = json.load(f)

    # Attente de 3 secondes maximum si le serveur ne répond pas
    client = MongoClient(url, serverSelectionTimeoutMS=3000)
    try:
        collection = client[nom_bdd][nom_collection]

        # Vider la collection pour pouvoir relancer le script sans doublons
        collection.delete_many({})

        collection.insert_many(trajets)
        total = collection.count_documents({})
        print(f"-Données insérées avec succès dans '{nom_bdd}.{nom_collection}' ({total} documents).\n")
    except ServerSelectionTimeoutError:
        print(f"-Impossible de se connecter à MongoDB ({url}). Le serveur est-il démarré ?\n")
    finally:
        client.close()

if __name__ == "__main__":
    df_brut = importer_donnees(os.path.join(DOSSIER_PROJET, "mobilite.csv"))
    df_propre = controller_et_nettoyer(df_brut)
    exporter_json(df_propre)
    charger_dans_mongodb()
