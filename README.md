# 🏗️ Local Data Lakehouse with Apache Iceberg, MinIO, Hive Metastore & Dremio

This project provides a complete local deployment of a modern **Data Lakehouse** architecture using Docker Compose. It integrates key open-source technologies for data storage, metadata management, processing, and analysis.

---

## 📸 Architecture Overview

![Frame 1](https://github.com/user-attachments/assets/5dec6683-8fd8-4f90-86b9-4fe944a12eb2)

---

## 🧩 Components

| Service         | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| **MinIO**       | S3-compatible object storage. Stores raw and processed datasets.           |
| **Apache Iceberg** | Table format that brings ACID transactions and versioning to data lakes. |
| **Hive Metastore** | Central catalog for managing Iceberg table metadata.                    |
| **Spark**       | Distributed compute engine used for batch ETL and data transformation.     |
| **Dremio**      | SQL engine and BI layer for querying Iceberg tables and visualizing data.  |

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Clone the Repository

```bash
git clone https://github.com/sultanjke/datalakehouse-concept.git
cd datalakehouse-concept
