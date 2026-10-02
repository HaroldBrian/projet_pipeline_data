import matplotlib.pyplot as plt
import pandas as pd
from traitement import controller_et_nettoyer, importer_donnees


def generer_graphiques(df):
 
    print("=== 5. CRÉATION DES GRAPHIQUES ===")

    # Configuration du style
    plt.style.use('ggplot')

    # Graphique 1 : Nombre de trajets par moyen de transport (Diagramme en barres)
    plt.figure(figsize=(8, 5))
    counts_transport = df['transport'].value_counts()
    counts_transport.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Nombre de trajets par moyen de transport')
    plt.xlabel('Moyen de transport')
    plt.ylabel('Nombre de trajets')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('trajets_par_transport.png')
    plt.close()
    print("-Graphique 1 sauvegardé : 'trajets_par_transport.png'")

    # Graphique 2 : Distance totale par moyen de transport (Camembert)
    plt.figure(figsize=(7, 7))
    distance_transport = df.groupby('transport')['distance'].sum()
    distance_transport.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title('Répartition de la distance totale par moyen de transport')
    plt.ylabel('')  # pour supprimer le libellé d'axe automatique
    plt.tight_layout()
    plt.savefig('distance_par_transport.png')
    plt.close()
    print("-Graphique 2 sauvegardé : 'distance_par_transport.png'\n")

if __name__ == "__main__":
    df_brut = importer_donnees()
    df_propre = controller_et_nettoyer(df_brut)
    generer_graphiques(df_propre)