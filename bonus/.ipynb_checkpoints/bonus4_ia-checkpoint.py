#Bonus 4 : commentaire automatique des résultats avec l'IA (Google Gemini)

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Accès au dossier parent pour réutiliser le pipeline et le fichier .env
DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DOSSIER_PROJET)

from traitement import importer_donnees, controller_et_nettoyer, DOSSIER_FICHIERS
from analyse import calculer_indicateurs

MODELE = "gemini-3.8-flash"

def commentaire_sans_ia(indicateurs):
    # Commentaire de secours si l'IA n'est pas disponible 
    return (f"Sur {indicateurs['nb_trajets']} trajets analysés, le moyen de transport le plus utilisé "
            f"est : {indicateurs['transport_top']}. La distance totale parcourue est de "
            f"{indicateurs['distance_totale']:.1f} km pour une durée moyenne de "
            f"{indicateurs['duree_moyenne']:.1f} min. Le trajet le plus fréquent est "
            f"{indicateurs['trajet_top']}.")

def generer_commentaire_ia(indicateurs):
    print("=== BONUS 4. COMMENTAIRE AUTOMATIQUE PAR L'IA ===")

    load_dotenv(os.path.join(DOSSIER_PROJET, ".env"))
    cle_api = os.getenv("GOOGLE_API_KEY")
    if not cle_api:
        print("-Clé GOOGLE_API_KEY absente du fichier .env : commentaire généré sans IA.\n")
        return commentaire_sans_ia(indicateurs)

    prompt = f"""Tu es un analyste de données. Rédige en français un court commentaire
(4 à 5 phrases, sans liste ni titre) sur les déplacements urbains à partir de ces indicateurs :
- Nombre total de trajets : {indicateurs['nb_trajets']}
- Distance totale : {indicateurs['distance_totale']:.2f} km
- Durée moyenne : {indicateurs['duree_moyenne']:.2f} min
- Durée minimale : {indicateurs['duree_min']} min, maximale : {indicateurs['duree_max']} min
- Moyen de transport le plus utilisé : {indicateurs['transport_top']}
- Station de départ la plus fréquentée : {indicateurs['station_depart_top']}
- Trajet le plus fréquent : {indicateurs['trajet_top']}
- Médiane de la distance : {indicateurs['mediane_distance']:.2f} km
- Écart-type de la distance : {indicateurs['ecart_type_distance']:.2f} km
N'invente aucun chiffre qui ne figure pas dans cette liste."""

    try:
        genai.configure(api_key=cle_api, transport="rest")
        reponse = genai.GenerativeModel(MODELE).generate_content(
            prompt, request_options={"timeout": 90}) 
        return reponse.text.strip()
    except Exception as erreur:
        print(f"-L'IA n'a pas pu répondre ({erreur}) : commentaire généré sans IA.\n")
        return commentaire_sans_ia(indicateurs)

if __name__ == "__main__":
    df_brut = importer_donnees(os.path.join(DOSSIER_PROJET, "mobilite.csv"))
    df_propre = controller_et_nettoyer(df_brut)
    indicateurs = calculer_indicateurs(df_propre)

    commentaire = generer_commentaire_ia(indicateurs)
    print(commentaire)

    with open(os.path.join(DOSSIER_FICHIERS, "commentaire_ia.txt"),
              "w", encoding="utf-8") as f:
        f.write(commentaire)
