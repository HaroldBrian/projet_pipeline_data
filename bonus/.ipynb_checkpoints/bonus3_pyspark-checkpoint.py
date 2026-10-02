#Bonus 3 : reproduction du nettoyage et de l'analyse avec PySpark

import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def creer_session():
    spark = SparkSession.builder.appName("pipeline_mobilite").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")  # masquer les logs techniques de Spark
    return spark

def importer_donnees(spark, chemin_fichier=os.path.join(DOSSIER_PROJET, "mobilite.csv")):
    print("=== BONUS 3. IMPORT AVEC PYSPARK ===")
    df = spark.read.csv(chemin_fichier, header=True, inferSchema=True)
    print(f"Nombre de lignes : {df.count()}, colonnes : {len(df.columns)}")
    df.printSchema()
    return df

def nettoyer_donnees(df):
    print("=== BONUS 3. NETTOYAGE AVEC PYSPARK ===")

    df = df.dropDuplicates(["id"])

    df = df.withColumn("transport", F.initcap(F.trim(F.col("transport"))))
    df = df.withColumn("station_depart", F.trim(F.col("station_depart")))
    df = df.withColumn("station_arrivee", F.trim(F.col("station_arrivee")))

    # Imputation avant le filtre, sinon les durées manquantes seraient supprimées
    mediane_duree = df.filter(F.col("duree") > 0).approxQuantile("duree", [0.5], 0)[0]
    df = df.fillna({"duree": mediane_duree})
    print(f"-Durées manquantes imputées par la médiane : {mediane_duree} min")

    df = df.filter((F.col("duree") > 0) & (F.col("distance") > 0))

    df = df.withColumn("duree", F.col("duree").cast("int"))
    df = df.withColumn("date_trajet", F.to_date(F.col("date_trajet")))

    print(f"-Lignes conservées : {df.count()}")
    df.orderBy("id").show()
    return df

def calculer_indicateurs(df):
    print("=== BONUS 3. INDICATEURS AVEC PYSPARK ===")

    stats = df.agg(
        F.count("*").alias("nb_trajets"),
        F.sum("distance").alias("distance_totale"),
        F.avg("duree").alias("duree_moyenne"),
        F.min("duree").alias("duree_min"),
        F.max("duree").alias("duree_max")
    ).first()

    # Valeur la plus fréquente d'une colonne (équivalent de mode() en Pandas)
    def plus_frequent(colonne):
        return df.groupBy(colonne).count().orderBy(F.desc("count"), colonne).first()[0]

    df = df.withColumn("trajet", F.concat_ws(" -> ", "station_depart", "station_arrivee"))

    print(f"-Nombre total de trajets : {stats['nb_trajets']}")
    print(f"-Distance totale parcourue : {stats['distance_totale']:.2f} km")
    print(f"-Durée moyenne d'un trajet : {stats['duree_moyenne']:.2f} min")
    print(f"-Durée minimale : {stats['duree_min']} min | Durée maximale : {stats['duree_max']} min")
    print(f"-Moyen de transport le plus utilisé : {plus_frequent('transport')}")
    print(f"-Station de départ la plus fréquentée : {plus_frequent('station_depart')}")
    print(f"-Trajet le plus fréquent : {plus_frequent('trajet')}\n")

    print("Nombre de trajets et distance totale par moyen de transport :")
    df.groupBy("transport").agg(
        F.count("*").alias("nb_trajets"),
        F.round(F.sum("distance"), 2).alias("distance_totale")
    ).orderBy(F.desc("nb_trajets")).show()

if __name__ == "__main__":
    spark = creer_session()
    df_brut = importer_donnees(spark)
    df_propre = nettoyer_donnees(df_brut)
    calculer_indicateurs(df_propre)
    spark.stop()
