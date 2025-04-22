import streamlit as st
import pandas as pd
from io import StringIO

# Must be the first Streamlit command
st.set_page_config(page_title="Data Insight Generator", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
        }
        .reportview-container .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .summary-box {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .image-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .image-container img {
            width: 48%;
        }
    </style>
""", unsafe_allow_html=True)

# Header Images
st.markdown("""
    <div class='image-container'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Infoedgelogo.png/500px-Infoedgelogo.png' alt='Image 1'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/f/fc/Naukri.png?20240329063224' alt='Image 2'>
    </div>
""", unsafe_allow_html=True)

# App title
st.title("AI-Powered Data Insight Generator")
st.markdown("Upload a CSV file or paste your tabular data below to generate insights.")

# CSV Upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

# Text Input
st.markdown("---")
st.markdown("### OR Paste Data Below")
user_input = st.text_area("Paste Data Here (CSV-style text)", height=200, placeholder="e.g. Student Name,Math Mark,Science Mark, Biology Mark\nStudent-1,59,95,21")

# Function to generate simple natural language summary
def generate_summary(df):
    summaries = []
    for col in df.select_dtypes(include='number').columns:
        max_val = df[col].max()
        min_val = df[col].min()
        mean_val = df[col].mean()

        max_row = df[df[col] == max_val].iloc[0]
        min_row = df[df[col] == min_val].iloc[0]

        summaries.append(f"In '{col}', the highest value is {max_val} by {max_row[0]}, and the lowest is {min_val} by {min_row[0]}. The average is {mean_val:.2f}.")

    return "\n".join(summaries)

# Function to process and display insights
def display_insights(df):
    st.subheader("Natural Language Summary")
    st.markdown(f"<div class='summary-box'>{generate_summary(df)}</div>", unsafe_allow_html=True)

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
