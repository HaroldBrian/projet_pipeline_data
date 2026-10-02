import pandas as pd
import numpy as np

def importer_donnees(chemin_fichier="mobilite.csv"):
    #Lecture du fichier CSV et obtention du DataFrame initial
    df = pd.read_csv(chemin_fichier)
    print("=== 1. DONNÉES BRUTES IMPORTÉES ===")
    print(f"Nombre de lignes : {len(df)}, colonnes : {len(df.columns)}\n")
    return df

def controller_et_nettoyer(df):

    #Detection et correction des anomalies de qualite
    
    print("=== 2. CONTRÔLE ET NETTOYAGE DES DONNÉES ===")
    
    # a. Suppression des doublons 
    nb_doublons = df.duplicated(subset=['id']).sum()
    print(f"Doublons sur 'id' détectés : {nb_doublons}")
    df = df.drop_duplicates(subset=['id']).copy()
    
    # b. Normalisation du texte (transport, stations)
    df['transport'] = df['transport'].str.strip().str.capitalize()
    df['station_depart'] = df['station_depart'].str.strip()
    df['station_arrivee'] = df['station_arrivee'].str.strip()
    
    # c. Nettoyage des valeurs incoherentes (duree ou distance <= 0)
    anomalies_valeurs = df[(df['duree'] <= 0) | (df['distance'] <= 0)]
    print(f"Trajets avec durée/distance négative ou nulle : {len(anomalies_valeurs)}")
    df = df[(df['duree'] > 0) & (df['distance'] > 0)].copy()
    
    # d. Traitement des valeurs manquantes (remplacement de la duree manquante par la médiane)
    nb_nan_duree = df['duree'].isna().sum()
    if nb_nan_duree > 0:
        mediane_duree = df['duree'].median()
        df['duree'] = df['duree'].fillna(mediane_duree)
        print(f"-> Durées manquantes imputées par la médiane ({mediane_duree} min) : {nb_nan_duree}")
        
    # e. Conversion des types de donnees
    df['date_trajet'] = pd.to_datetime(df['date_trajet'])
    df['id'] = df['id'].astype(int)
    
    print(f"\n=== FIN DU NETTOYAGE : {len(df)} LIGNES CONSERVÉES ===")
    print(df.info())
    print("\nAperçu des données nettoyées :")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df_brut = importer_donnees()
    df_propre = controller_et_nettoyer(df_brut)