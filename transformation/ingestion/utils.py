"""
Author : Arjun P
"""

from pathlib import Path
from typing import List
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import pandas as pd
import re

def traverse_folder(dir:str) -> List:
    
    return [f"{dir}/{f.name}" for f in Path(dir).iterdir() if f.is_file()]

def standardize_file_name(filename:str) -> str:
    new_filename = filename.strip().lower()
    new_filename = new_filename.replace(" ", "_")
    new_filename = re.sub(r'[^a-z0-9_]', '', new_filename)
    return new_filename

def ingest_spark(
        files: List
) -> None:
    builder = (
        SparkSession.builder
        .appName("PySparkWithStandaloneMetastore")
        .master("spark://spark-server:7077")
        .config("spark.sql.warehouse.dir", "file:///spark-warehouse")
        .config("spark.sql.catalogImplementation", "hive")
        .config("hive.metastore.uris", "thrift://metastore-db:9083")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("delta.columnMapping.mode", "name")
        .enableHiveSupport()
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    # Spark expects schemas to be present before writing to it
    schema_name = "raw"
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {schema_name}")

    for file in [f for f in files if f.endswith('.csv')]:

        try:
            df = spark.read.csv(file, 
                                header=True, 
                                inferSchema=True
                                )

            file_name = file.split('/')[-1].split('.')[0]
            file_name = standardize_file_name(file_name)
            table_name = f"{schema_name}.{file_name}"

            df.write.format("delta").mode("overwrite").saveAsTable(table_name)

            print(f"{table_name} table created in delta lake!")

        except Exception as e:
            print(e)
