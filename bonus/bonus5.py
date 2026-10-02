import os
import sys

DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(DOSSIER_PROJET)

from analyse import calculer_indicateurs
from chargement_bdd import charger_dans_bdd, exporter_csv
from graphiques import generer_graphiques
from traitement import controller_et_nettoyer, importer_donnees

def choisir_fichier():
    #Demande à l'utilisateur de saisir un fichier CSV valide
    fichier_par_defaut = "mobilite.csv"

    while True:
        saisie = input(
            f"\nEntrer le nom du fichier CSV à traiter (Appuyez sur Entrée pour '{fichier_par_defaut}' ou 'EXIT' pour quitter) : "
        ).strip()

        # Option de sortie
        if saisie.upper() == "EXIT":
            print("Arrêt du programme demandé par l'utilisateur.")
            return None

        # Fichier par défaut
        if not saisie:
            saisie = fichier_par_defaut

        # Construction du chemin complet vers la racine du projet
        chemin_complet = os.path.join(DOSSIER_PROJET, saisie)

        # Vérification de l'existence avec le chemin absolu
        if os.path.exists(chemin_complet):
            print(f"-> Fichier '{saisie}' validé pour le traitement.")
            return chemin_complet
        else:
            print(
                f"[ERREUR] Le fichier '{saisie}' est introuvable à la racine du projet ({DOSSIER_PROJET}). Veuillez réessayer."
            )

def executer_pipeline_bonus5():
    print("===LANCEMENT DU PIPELINE ETL - BONUS 5 ===")

    # 1. Choix du fichier via la boucle interactive
    fichier_csv = choisir_fichier()

    # Si l'utilisateur a saisi EXIT
    if fichier_csv is None:
        return

    print(f" \n  DÉBUT DU TRAITEMENT SUR : {fichier_csv}")
 
    try:
        # 2. Extraction & Nettoyage
        df_brut = importer_donnees(fichier_csv)
        df_propre = controller_et_nettoyer(df_brut)

        # 3. Analyse
        calculate_indicators = calculer_indicateurs(df_propre)

        # 4. Graphiques
        generer_graphiques(df_propre)

        # 5. Exports (CSV & BDD)
        exporter_csv(df_propre, "resultats.csv")
        charger_dans_bdd(df_propre, "mobilite.db")

        
        print(" BONUS 5 EXÉCUTÉ AVEC SUCCÈS !")
     

    except Exception as e:
        print(f"\n[ERREUR INATTENDUE] : {e}")


if __name__ == "__main__":
    executer_pipeline_bonus5()