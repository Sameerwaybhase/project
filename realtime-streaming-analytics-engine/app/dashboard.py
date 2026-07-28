import streamlit as st
import pandas as pd
import boto3
import os

st.set_page_config(page_title="Real-Time Analytics Dashboard", layout="wide")

st.title("⚡ Real-Time Streaming & Analytics Engine Dashboard")

REGION = "us-east-1"
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "LiveOrdersTable")

@st.cache_data(ttl=5)
def fetch_live_orders():
    try:
        dynamodb = boto3.resource("dynamodb", region_name=REGION)
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan()
        items = response.get("Items", [])
        if items:
            df = pd.DataFrame(items)
            df["amount"] = df["amount"].astype(float)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()

df = fetch_live_orders()

if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders Processed", len(df))
    col2.metric("Total Revenue", f"${df['amount'].sum():,.2f}")
    col3.metric("Avg Order Value", f"${df['amount'].mean():,.2f}")

    st.subheader("Live Streamed Orders Data")
    st.dataframe(df.sort_values(by="timestamp", ascending=False), use_container_width=True)
else:
    st.info("No streaming data available. Please start the producer script.")
