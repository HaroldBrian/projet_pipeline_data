import pandas as pd

# Format du fichier CSV 
csv_format = {
    "sep": ",",         
    "encoding": "utf-8",  
    "decimal": ".",       
    "champs": [           
        "id",
        "date_trajet",
        "station_depart",
        "station_arrivee",
        "duree",
        "distance",
        "transport"
    ]
}

def importer_donnees(chemin_fichier="mobilite.csv", format_csv=csv_format):
    #Lecture du fichier CSV et obtention du DataFrame initial
    try:
        df = pd.read_csv(chemin_fichier, sep=format_csv["sep"],
                         encoding=format_csv["encoding"], decimal=format_csv["decimal"])
    except FileNotFoundError:
        print(f"Erreur : le fichier '{chemin_fichier}' est introuvable.")
        raise

    # Vérification que tous les champs attendus sont présents
    champs_manquants = [c for c in format_csv["champs"] if c not in df.columns]
    if champs_manquants:
        raise ValueError(f"Champs manquants dans '{chemin_fichier}' : {champs_manquants}")

    print("=== 1. DONNÉES BRUTES IMPORTÉES ===")
    print(f"Nombre de lignes : {len(df)}, colonnes : {len(df.columns)}")
    print(f"Noms des colonnes : {list(df.columns)}")
    print("\nTypes de données :")
    print(df.dtypes)
    print("\nPremières lignes :")
    print(df.head(), "\n")
    return df

def controler_donnees(df):
    #Detection et affichage des lignes problematiques (sans modifier les donnees)
    print("=== 2. CONTRÔLE DE LA QUALITÉ DES DONNÉES ===")

    # a. Valeurs manquantes
    print("Valeurs manquantes par colonne :")
    print(df.isna().sum())
    print("Lignes concernées :")
    print(df[df.isna().any(axis=1)], "\n")

    # b. Doublons sur 'id'
    doublons = df[df.duplicated(subset=['id'], keep=False)]
    print(f"Doublons sur 'id' : {df.duplicated(subset=['id']).sum()}")
    print(doublons, "\n")

    # c. Valeurs incoherentes (duree ou distance <= 0)
    incoherences = df[(df['duree'] <= 0) | (df['distance'] <= 0)]
    print(f"Trajets avec durée/distance négative ou nulle : {len(incoherences)}")
    print(incoherences, "\n")

def nettoyer_donnees(df):
    #Correction ou suppression des anomalies detectees
    print("=== 3. NETTOYAGE DES DONNÉES ===")

    # a. Suppression des doublons
    df = df.drop_duplicates(subset=['id']).copy()

    # b. Normalisation du texte (transport, stations)
    df['transport'] = df['transport'].str.strip().str.capitalize()
    df['station_depart'] = df['station_depart'].str.strip()
    df['station_arrivee'] = df['station_arrivee'].str.strip()

    # c. Traitement des valeurs manquantes (avant le filtre, sinon les NaN seraient supprimés)
    #    La médiane est calculée uniquement sur les durées positives
    nb_nan_duree = df['duree'].isna().sum()
    if nb_nan_duree > 0:
        mediane_duree = df.loc[df['duree'] > 0, 'duree'].median()
        df['duree'] = df['duree'].fillna(mediane_duree)
        print(f"-Durées manquantes imputées par la médiane ({mediane_duree} min) : {nb_nan_duree}")

    # d. Suppression des valeurs incoherentes (duree ou distance <= 0)
    df = df[(df['duree'] > 0) & (df['distance'] > 0)].copy()

    # e. Conversion des types de donnees
    df['id'] = df['id'].astype(int)
    df['duree'] = df['duree'].round().astype(int)
    df['distance'] = df['distance'].astype(float)
    df['date_trajet'] = pd.to_datetime(df['date_trajet']).dt.date

    print(f"\n=== FIN DU NETTOYAGE : {len(df)} LIGNES CONSERVÉES ===")
    df.info()
    print("\nAperçu des données nettoyées :")
    print(df.head(), "\n")

    return df

def controller_et_nettoyer(df):
    #Enchainement du controle puis du nettoyage
    controler_donnees(df)
    return nettoyer_donnees(df)

if __name__ == "__main__":
    df_brut = importer_donnees()
    df_propre = controller_et_nettoyer(df_brut)
