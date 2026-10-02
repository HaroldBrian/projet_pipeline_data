#Execution du pipeline complet

from traitement import importer_donnees, controller_et_nettoyer
from analyse import calculer_indicateurs
from graphiques import generer_graphiques
from chargement_bdd import exporter_csv, charger_dans_bdd
from bonus.bonus1_mongodb import exporter_json, charger_dans_mongodb


def executer_pipeline():
    
    print("   LANCEMENT DU PIPELINE DE TRAITEMENT DE DONNÉES  ")

    # 1, 2 & 3. Import, contrôle et nettoyage
    df_brut = importer_donnees("mobilite.csv")
    df_propre = controller_et_nettoyer(df_brut)

    # 4. Analyse & Transformation
    indicateurs = calculer_indicateurs(df_propre)

    # 5. Visualisation
    generer_graphiques(df_propre)

    # 6 & 7. Exportation CSV et chargement en BDD
    exporter_csv(df_propre)
    charger_dans_bdd(df_propre)

    # Bonus 1. Exportation JSON et chargement dans MongoDB
    exporter_json(df_propre)
    charger_dans_mongodb()

    
    print("===PIPELINE EXÉCUTÉ AVEC SUCCÈS !===")
    


if __name__ == "__main__":
    executer_pipeline()