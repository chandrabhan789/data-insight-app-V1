import streamlit as st
import pandas as pd
from io import StringIO

# Set up page config first
st.set_page_config(page_title="Data Insight Generator", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
            color: #000000;
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
            margin-bottom: 20px;
        }
        .image-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .image-container img {
            width: 20%;
        }
    </style>
""", unsafe_allow_html=True)

# Header with 2 logos
st.markdown("""
    <div class='image-container'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Infoedgelogo.png/500px-Infoedgelogo.png' alt='Info Edge'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/f/fc/Naukri.png?20240329063224' alt='Naukri'>
    </div>
""", unsafe_allow_html=True)

# App title and input
st.title("AI-Powered Data Insight Generator")
st.markdown("Paste your tabular data below (CSV-style) and click 'Generate Insights'.")

user_input = st.text_area("Paste Data Here", height=200, placeholder="e.g. Student Name,Math Mark,Science Mark,Biology Mark\nStudent-1,59,95,21")

# --- Insight Functions ---

# Primary insight block
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

# Alternative insight block
def generate_secondary_insight(df):
    messages = []

    # Subject with highest average
    subject_avgs = df.select_dtypes(include='number').mean()
    top_subject = subject_avgs.idxmax()
    top_avg = subject_avgs.max()
    messages.append(f"📊 The subject with the highest overall average is **{top_subject}** with {top_avg:.2f} marks.")

    # Most consistent student (lowest std dev in row)
    df_numeric = df.select_dtypes(include='number')
    df_numeric['variation'] = df_numeric.std(axis=1)
    consistent_index = df_numeric['variation'].idxmin()
    consistent_student = df.iloc[consistent_index, 0]
    messages.append(f"🔍 The most consistent performer is **{consistent_student}**, with the least score variation across subjects.")

    # Most varied subject
    ranges = df_numeric.drop(columns='variation').max() - df_numeric.drop(columns='variation').min()
    varied_subject = ranges.idxmax()
    messages.append(f"📈 **{varied_subject}** has the widest score range, showing the most inconsistent performance across students.")

    return "\n".join(messages)

# Main display logic
def display_insights(df):
    st.subheader("Natural Language Summary")
    st.markdown(f"<div class='summary-box'>{generate_summary(df)}</div>", unsafe_allow_html=True)

    st.subheader("Alternative Insight Perspective")
    st.markdown(f"<div class='summary-box'>{generate_secondary_insight(df)}</div>", unsafe_allow_html=True)

# Process input
if st.button("Generate Insights"):
    try:
        if user_input:
            df = pd.read_csv(StringIO(user_input), sep=",|\t", engine="python")
            display_insights(df)
        else:
            st.warning("⚠️ Please paste some data to analyze.")
    except Exception as e:
        st.error(f"❌ Error processing data: {e}")
