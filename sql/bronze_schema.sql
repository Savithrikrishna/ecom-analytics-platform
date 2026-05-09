CREATE OR REPLACE TABLE `<project-id>.poc_daily_csv_ingest.orders_bronze`
(
  order_id STRING,
  order_date STRING,        -- Stored as string to handle various date formats from source
  customer_email STRING,
  product_name STRING,
  category STRING,
  quantity STRING,          -- Stored as string to prevent errors if source sends non-numeric data
  price STRING,             -- Stored as string to handle currency symbols like '$' if present
  store_name STRING,
  ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(_PARTITIONTIME)
OPTIONS(
  description="Raw landing table for daily CSV ingestions from email."
);
