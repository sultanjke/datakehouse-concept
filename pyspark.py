import pyspark
from pyspark.sql import SparkSession
import os
 
NESSIE_URI = os.environ.get("NESSIE_URI")
WAREHOUSE = os.environ.get("WAREHOUSE")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_S3_ENDPOINT = os.environ.get("AWS_S3_ENDPOINT")

print("MINIO ENDPOINT:", AWS_S3_ENDPOINT) # .env файл
print("NESSIE URI:", NESSIE_URI)
print("WAREHOUSE:", WAREHOUSE) 

conf = (
    pyspark.SparkConf()
        .setAppName('ParquetToIceberg')
        .set('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.1,'
                                     'org.projectnessie.nessie-integrations:nessie-spark-extensions-3.3_2.12:0.67.0,'
                                     'software.amazon.awssdk:bundle:2.17.178,'
                                     'software.amazon.awssdk:url-connection-client:2.17.178')
        .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions,'
                                     'org.projectnessie.spark.extensions.NessieSparkSessionExtensions')
        .set('spark.sql.catalog.nessie', 'org.apache.iceberg.spark.SparkCatalog')
        .set('spark.sql.catalog.nessie.uri', NESSIE_URI)
        .set('spark.sql.catalog.nessie.ref', 'main')
        .set('spark.sql.catalog.nessie.authentication.type', 'NONE')
        .set('spark.sql.catalog.nessie.catalog-impl', 'org.apache.iceberg.nessie.NessieCatalog')
        .set('spark.sql.catalog.nessie.s3.endpoint', AWS_S3_ENDPOINT)
        .set('spark.sql.catalog.nessie.warehouse', WAREHOUSE)
        .set('spark.sql.catalog.nessie.io-impl', 'org.apache.iceberg.aws.s3.S3FileIO')
        .set('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY)
        .set('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_KEY)
)
 
spark = SparkSession.builder.config(conf=conf).getOrCreate()
 
parquet_path = "userdata.parquet"
df = spark.read.parquet(parquet_path)
df.printSchema()
df.show(5)
 
df.writeTo("nessie.userdata").using("iceberg").createOrReplace()
 
spark.sql("SELECT * FROM nessie.userdata LIMIT 10").show()