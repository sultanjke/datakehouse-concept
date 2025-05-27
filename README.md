# Local Data Lakehouse with Apache Iceberg, MinIO, Project Nessie & Dremio

This project provides a complete local deployment of a modern **Data Lakehouse** architecture using Docker Compose. It integrates key open-source technologies for data storage, metadata management, processing, and analysis.

---

## Architecture Overview

![Frame 1](https://github.com/user-attachments/assets/99f9c0bb-434c-449c-902d-310f22397cd8)

---

## Components

| Service         | Description                                                                 | Reference                                  |
|-----------------|-----------------------------------------------------------------------------|--------------------------------------------|
| **MinIO**       | S3-compatible object storage. Stores raw and processed datasets.           | https://min.io/                             |
| **Apache Iceberg** | Table format that brings ACID transactions and versioning to data lakes. | https://iceberg.apache.org/                |
| **Project Nessie** | Central catalog for managing Iceberg table metadata.                    | https://projectnessie.org/                  |
| **Spark**       | Distributed compute engine used for batch ETL and data transformation.     | https://spark.apache.org/                   |
| **Dremio**      | SQL engine and BI layer for querying Iceberg tables and visualizing data.  | https://www.dremio.com/                     |

---

# Getting Started
To obtain a local copy of the repository and set it up, please follow these steps:

### Software Dependencies
* Install [Python 3.8+](https://www.python.org/)
* Install [Visual Studio Code](https://code.visualstudio.com/)

### Prerequisites

- [Docker Compose](https://docs.docker.com/compose/)

### Clone the Repository

```
git clone https://github.com/sultanjke/datalakehouse-concept.git
cd datalakehouse-concept
```

> Please, make sure creating each terminal for every component to not messing up.

### Run the MinIO Component in VS Code's Terminal

```
docker-compose up minioserver
```

Head over to localhost:9001 in your browser and log in with credentials minioadmin/minioadmin. Once you're logged in, do the following:

* create a bucket called "warehouse"
* create an access key and copy the access key and secret key to your .env file

### Running up the Project Nessie Component in VS Code's Terminal

```
docker-compose up nessie
```

### Running up Jupyter Notebook environment with Apache Spark in VS Code's Terminal

```
docker-compose up spark_notebook
```
* In the logs, when this container opens in Docker Software, look for output that looks like the following and copy and paste the URL into your browser:
  ```
  notebook  |  or http://127.0.0.1:8888/?token=9db2c8a4459b4aae3132dfabdf9bf4396393c608816743a9
  ```
* Upload a dataset model from dataset/userdata.parquet to the notebook from the project repository.
* Create a new Python3 file and execute the following script, which is also stored in the repository as a /datalakehouse-concept/pyspark.py:
  
     ```
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
     ```

### Running up the Dremio Component in VS Code's Terminal
```
docker-compose up dremio
```

### Querying the Data in Dremio

Now that the data has been created, catalogs like Nessie for your Apache Iceberg tables offer easy visibility of your tables from tool to tool. We open Dremio and see we can immediately query the data we have in our Nessie catalog.

* head over to localhost:9047 where Dremio web application resides
* create your admin user account
* once on the dashboard click on "add source" in the bottom left
* select "nessie"

Fill out the tabs as shown in the images below:

![image](https://github.com/user-attachments/assets/3947ffb8-ff8d-4546-b6ae-c43dafb04f2a)
=========================================================================================
![image](https://github.com/user-attachments/assets/675ca1bf-a793-465d-a229-ea805fc016e0)

Now you can see our names table on the Dremio dashboard under our new connected source:

![image 11](https://github.com/user-attachments/assets/ac09f7c4-040a-4969-8b79-3d6c8377b9da)

### Power BI Integration (Live Data via DirectQuery)

Dremio supports ODBC/JDBC connections (31010:31010, 32010:32010 ports), enabling seamless integration with Power BI for live dashboards using DirectQuery. This ensures that data in your Iceberg tables (stored in MinIO) is 
queried in real time without requiring dataset imports. Here's the two instructions:

* ODBC Connection:
  
    i. In Power BI Desktop, choose: Get Data -> ODBC
  
    ii. Select Dremio Connector (set up a DSN for it in ODBC Data Sources 64-bit)

  ![image](https://github.com/user-attachments/assets/eb226f74-6db0-4555-b221-93503cb86787)
  ![image](https://github.com/user-attachments/assets/4e793de2-ba53-4d79-9e98-3265fc14f7e7)
  
    iii. Fill out the connection details (Server: localhost or dremio, port: 31010)
  
    iv. Verify the authentication credentials: usually, your credentials you fill out the first time you're joined to the GUI system of Dremio.

* Direct Power BI Connection, searching up Dremio Software in Get Data Tab

  ![image](https://github.com/user-attachments/assets/2f18f13b-64b6-493c-b08a-7115647c62a9)

  > Make sure encryption is disabled, creds are localhost or dremio:31010, and auth creds are the same as in log-in creds for Dremio GUI.

## Result

So now you get the performance of Dremio and Apache Iceberg along with the git-like capabilities that the Nessie catalog brings, allowing you to isolate ingestion on branches, create zero-clones for experimentation, and rollback your catalog for disaster recovery all on your data lakehouse.

![image](https://github.com/user-attachments/assets/3b38236b-085d-4f83-b1e6-92c9b2fa62a5)

