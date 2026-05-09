# AI-Powered ECOM BI Sales Platform (GCP POC)

An end-to-end, serverless data pipeline that automates the ingestion of daily sales CSVs from email into **BigQuery**, cleanses the data using a **Medallion Architecture**, and provides an **AI Chatbot** interface for natural language business intelligence.

---

## Architecture Overview

The system follows a serverless, event-driven design on **Google Cloud Platform**:

1.  **Ingestion**: A Google Apps Script monitors Gmail for daily CSV attachments and streams them to **Google Cloud Storage (GCS)**.
2.  **Processing**: An **Eventarc** trigger detects new files and launches a **2nd Gen Cloud Function**.
3.  **Transformation**: The Cloud Function loads raw data into the **Bronze Layer** and executes SQL logic to deduplicate and standardize data into the **Silver Layer**.
4.  **Analytics**: A **Streamlit** web app utilizes **LangChain** and **Gemini 2.5 Flash** to translate English questions into SQL queries against the Silver Layer.

---

## 📂 Project Structure

```text
ecom-analytics-platform/
├── automation/               # Apps Script code for Gmail polling
├── chatbot/                  # Streamlit UI & LangChain Agent logic
├── cloud_functions/          # Python 3.11 Cloud Function (ETL)
├── sql/                      # DDL and Transformation scripts
├── .env.example              # Template for environment variables
├── .gitignore                # Ensures security by hiding credentials
└── README.md                 # Project documentation

```

## Tech Stack
Languages: Python 3.11, SQL, Google Apps Script
AI/LLM: Gemini 2.5 Flash, LangChain
Google Cloud: BigQuery, Cloud Functions (2nd Gen), GCS, Eventarc
Frontend: Streamlit


## Setup & Installation
1. Environment Configuration
Create a .env file in the root directory based on the following template:

```
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
BQ_DATASET=your_dataset_name
BRONZE_TABLE=orders_bronze
SILVER_TABLE=orders_silver
```

2. Authentication
Ensure you have the Google Cloud SDK installed and authenticated on your local machine:

```
gcloud auth application-default login
```

3. Running the Chatbot Locally

# Navigate to the chatbot directory
```cd chatbot```

# Install dependencies
```pip install -r requirements.txt```

# Start Streamlit
```python3 -m streamlit run chatbot.py --server.enableCORS=false --server.enableXsrfProtection=false```


## Data Strategy: Medallion Architecture
To satisfy business requirements for "trustworthy data," this project implements two distinct layers:

Bronze (Raw): Captures every row from the CSV exactly as received. This ensures auditability and a "source of truth."

Silver (Cleaned):

Deduplication: Uses QUALIFY ROW_NUMBER() to ensure each order_id is unique.
Data Correction: Standardizes product names (e.g., merging "Folding Chair" variations).
Type Casting: Converts string-based prices and quantities into numeric types (INT64, FLOAT64) for accurate BI calculations.


## Future Improvements (Production Grade)

CI/CD: Implement GitHub Actions or Cloud Build to deploy Cloud Functions automatically on code commit.
Data Validation: Integrate Great Expectations to catch malformed data (negative prices, invalid emails) before it reaches the Silver layer.
Monitoring & Alerting: Set up Cloud Monitoring dashboards and Slack/Email alerts for pipeline failures.
