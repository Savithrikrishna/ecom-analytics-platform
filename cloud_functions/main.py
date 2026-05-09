import functions_framework
from google.cloud import bigquery
import os

@functions_framework.cloud_event
def process_csv_trigger(cloud_event):
    # Get file info from the trigger
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]
    
    PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    DATASET_ID = os.environ.get("BQ_DATASET")
    
    # Tables
    BRONZE_TABLE = f"{PROJECT_ID}.{DATASET_ID}.{os.environ.get('BRONZE_TABLE')}"
    SILVER_TABLE = f"{PROJECT_ID}.{DATASET_ID}.{os.environ.get('SILVER_TABLE')}"
    
    client = bigquery.Client()

    # LOAD DATA INTO BRONZE (RAW)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_APPEND",
    )

    uri = f"gs://{bucket_name}/{file_name}"
    print(f"Starting Ingestion: Loading {file_name} into {BRONZE_TABLE}...")
    
    load_job = client.load_table_from_uri(uri, BRONZE_TABLE, job_config=job_config)
    load_job.result()  # Wait for ingestion to finish
    
    print(f"Ingestion Complete. Starting Transformation to {SILVER_TABLE}...")

    # TRANSFORM DATA INTO SILVER (CLEAN)
    sql_query = f"""
    CREATE OR REPLACE TABLE `{SILVER_TABLE}` AS
    WITH raw_data AS (
      SELECT 
        *,
        CASE 
          WHEN product_name IN ('Foldable Chair', 'Folding Chair') THEN 'Folding Chair'
          ELSE product_name 
        END AS clean_product_name
      FROM `{BRONZE_TABLE}`
    )
    SELECT 
        order_id,
        ANY_VALUE(CAST(order_date AS DATE)) AS order_date,
        ANY_VALUE(customer_email) AS customer_email,
        ANY_VALUE(clean_product_name) AS product_name,
        ANY_VALUE(category) AS category,
        SUM(CAST(quantity AS INT64)) AS total_quantity,
        MAX(CAST(price AS FLOAT64)) AS unit_price,
        SUM(CAST(quantity AS INT64) * CAST(price AS FLOAT64)) AS total_revenue,
        ANY_VALUE(store_name) AS store_name
    FROM raw_data
    WHERE order_id IS NOT NULL 
      AND order_date IS NOT NULL
    GROUP BY order_id;
    """
    
    # Run the SQL Query
    query_job = client.query(sql_query)
    query_job.result()
    
    print(f"Pipeline Complete! Data is now clean in {SILVER_TABLE}.")
