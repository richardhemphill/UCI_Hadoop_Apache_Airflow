"""Streamlit dashboard for raw sales and dbt sales summary."""

import os
import pandas as pd
import psycopg2
import streamlit as st


st.set_page_config(page_title="Kafka + dbt Sales Dashboard", layout="wide")
st.title("Kafka + dbt Sales Dashboard")

connection = psycopg2.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME", "airflow"),
    user=os.getenv("DB_USER", "airflow"),
    password=os.getenv("DB_PASSWORD", "airflow"),
)

raw_df = pd.read_sql("select * from raw_sales order by user_id", connection)
summary_df = pd.read_sql("select * from sales_summary order by event", connection)

st.header("Raw Sales Events")
st.dataframe(raw_df, use_container_width=True)

st.header("Sales Summary")
st.dataframe(summary_df, use_container_width=True)

if not summary_df.empty:
    st.bar_chart(summary_df.set_index("event")["total_events"])

connection.close()
