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
