import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Data Insight Generator", layout="centered")

st.title("AI-Powered Data Insight Generator")
st.markdown("Paste your tabular data (CSV-style text) in the box below and get instant insights.")

user_input = st.text_area("Paste Data Here", height=200, placeholder="e.g. Student Name,Math Mark,Science Mark, Biology Mark\nStudent-1,59,95,21")

if st.button("Generate Insights"):
    if user_input:
        try:
            # Read the text input as a DataFrame
            df = pd.read_csv(StringIO(user_input), sep=",|\t", engine="python")

            st.subheader("Data Preview")
            st.dataframe(df.head())

            st.subheader("Summary Statistics")
            st.dataframe(df.describe(include='all'))

            st.subheader("Column-wise Insights")
            for col in df.select_dtypes(include='number').columns:
                st.markdown(f"**{col}**")
                st.write(f"- Mean: {df[col].mean():.2f}")
                st.write(f"- Median: {df[col].median():.2f}")
                st.write(f"- Max: {df[col].max()}")
                st.write(f"- Min: {df[col].min()}")
                st.write(f"- Std Deviation: {df[col].std():.2f}")

        except Exception as e:
            st.error(f"Error processing data: {e}")
    else:
        st.warning("Please paste some data first.")
