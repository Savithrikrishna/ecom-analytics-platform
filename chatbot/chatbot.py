import streamlit as st
from langchain_google_vertexai import ChatVertexAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION")
DATASET = os.getenv("BQ_DATASET")

# Setup Gemini 2.5 Flash
llm = ChatVertexAI(
    model_name="gemini-2.5-flash",
    project=PROJECT_ID,
    location=LOCATION,
    temperature=0,
)

# Connect to BigQuery
db_uri = f"bigquery://{PROJECT_ID}/{DATASET}"
db = SQLDatabase.from_uri(db_uri)

# Create a tool-calling SQL agent
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True,
    handle_parsing_errors=True,
    prefix="""You are a BigQuery expert assistant for an e-commerce BI use case.

Given an input question:
1. Use the available SQL tools to inspect the schema and run queries against BigQuery.
2. Always run the query before answering.
3. After getting the result, respond with a clear, human-friendly English sentence summarizing the answer.
4. Do NOT include the raw SQL in your final answer. Only state the result in plain English.
5. If a count is returned, phrase it naturally (e.g., "There were 775 orders in November 2024.").
""",
)

# Streamlit UI
st.set_page_config(page_title="E-commerce BI Assistant", page_icon="🛍️")
st.title("📊 BI Sales Chatbot")
st.markdown("""
    This assistant queries the **Silver Layer** (cleaned data) in BigQuery.
    Ask me about revenue, products, or store performance.
""")

st.sidebar.header("Try these questions:")
st.sidebar.markdown("- What was the total revenue?")
st.sidebar.markdown("- Which store is performing best?")
st.sidebar.markdown("- What is the top selling product category?")
st.sidebar.markdown("- How many orders in November 2024?")

user_query = st.text_input("Ask a business question in plain English:")

if user_query:
    with st.spinner("Analyzing data..."):
        try:
            response = agent_executor.invoke({"input": user_query})

            output = response.get("output", [])

            final_answer = ""
            if isinstance(output, list):
                for part in output:
                    if hasattr(part, 'text'):
                        final_answer = part.text
                    elif isinstance(part, dict) and 'text' in part:
                        final_answer = part['text']
            else:
                final_answer = str(output)

            st.success("### Answer")
            st.write(final_answer)
        except Exception as e:
            st.error(f"Error: {e}")
