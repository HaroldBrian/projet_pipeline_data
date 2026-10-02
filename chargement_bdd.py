import sqlite3
import pandas as pd
from traitement import importer_donnees, controller_et_nettoyer

def exporter_csv(df, nom_fichier="resultats.csv"):
    #Exportation des données nettoyées au format CSV
    df.to_csv(nom_fichier, index=False)
    print("=== 6. EXPORT CSV ===")
    print(f"-Fichier généré avec succès : '{nom_fichier}'\n")

def charger_dans_bdd(df, nom_bdd="mobilite.db"):
    #Chargement des données nettoyées dans la table trajets
    print("=== 7. CHARGEMENT EN BASE DE DONNÉES (SQLite Externe) ===")
    
    # 1. Connexion au fichier SQLite existant
    conn = sqlite3.connect(nom_bdd)
    cursor = conn.cursor()

    # 2. Vider la table avant insertion pour éviter les erreurs de clé primaire 'id' en cas de réexécution)
    cursor.execute("DELETE FROM trajets")
    conn.commit()

    # 3. Insertion des données nettoyées dans la table déjà créée
    df.to_sql("trajets", conn, if_exists="append", index=False)
    
    # 4. Vérification de l'insertion
    cursor.execute("SELECT COUNT(*) FROM trajets")
    total_bdd = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    print(f"-Données insérées avec succès dans '{nom_bdd}' ({total_bdd} lignes dans la table 'trajets').\n")

if __name__ == "__main__":
    df_brut = importer_donnees()
    df_propre = controller_et_nettoyer(df_brut)
    exporter_csv(df_propre)
    charger_dans_bdd(df_propre)