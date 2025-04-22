import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Data Insight Generator", layout="centered")

st.title("AI-Powered Data Insight Generator")
st.markdown("Upload a CSV file or paste your tabular data below to generate insights.")

# CSV Upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# Text Input
st.markdown("---")
st.markdown("### OR Paste Data Below")
user_input = st.text_area("Paste Data Here (CSV-style text)", height=200, placeholder="e.g. Student Name,Math Mark,Science Mark, Biology Mark\nStudent-1,59,95,21")

# Function to process and display insights
def display_insights(df):
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

# Logic to read input and display results
if st.button("Generate Insights"):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            display_insights(df)

        elif user_input:
            df = pd.read_csv(StringIO(user_input), sep=",|\t", engine="python")
            display_insights(df)

        else:
            st.warning("Please upload a file or paste some data.")

    except Exception as e:
        st.error(f"Error processing data: {e}")
