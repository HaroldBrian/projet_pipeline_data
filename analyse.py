import numpy as np
import pandas as pd
from traitement import controller_et_nettoyer, importer_donnees


def calculer_indicateurs(df):
    #Calcul et affichage les indicateurs statistiques demandés
    print("=== 4. ANALYSE ET TRAITEMENTS DE DONNÉES ===")

    # 1. Calculs de base 
    nb_total_trajets = len(df)
    distance_totale = df['distance'].sum()
    duree_moyenne = df['duree'].mean()
    duree_min = df['duree'].min()
    duree_max = df['duree'].max()

    # 2. Modes et frequences
    transport_top = df['transport'].mode()[0]
    station_depart_top = df['station_depart'].mode()[0]

    # Trajet le plus frequent (Départ -> Arrivée)
    df['trajet_couple'] = df['station_depart'] + ' -> ' + df['station_arrivee']
    trajet_top = df['trajet_couple'].mode()[0]

    # 3. Calcul statistique avec NumPy
    ecart_type_distance = np.std(df['distance'].to_numpy())
    médiane_distance = np.median(df['distance'].to_numpy())

    # Affichage des résultats
    print(f"-Nombre total de trajets : {nb_total_trajets}")
    print(f"-Distance totale parcourue : {distance_totale:.2f} km")
    print(f"-Durée moyenne d'un trajet : {duree_moyenne:.2f} min")
    print(f"-Durée minimale : {duree_min:.1f} min | Durée maximale : {duree_max:.1f} min")
    print(f"-Moyen de transport le plus utilisé : {transport_top}")
    print(f"-Station de départ la plus fréquentée : {station_depart_top}")
    print(f"-Trajet le plus fréquent : {trajet_top}")
    print(f"-Écart-type de la distance : {ecart_type_distance:.2f} km")
    print(f"-Médiane de la distance : {médiane_distance:.2f} km\n")

    return {
        'nb_trajets': nb_total_trajets,
        'distance_totale': distance_totale,
        'duree_moyenne': duree_moyenne,
        'transport_top': transport_top
    }

if __name__ == "__main__":
    df_brut = importer_donnees()
    df_propre = controller_et_nettoyer(df_brut)
    indicateurs = calculer_indicateurs(df_propre)