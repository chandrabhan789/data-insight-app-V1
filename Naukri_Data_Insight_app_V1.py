import streamlit as st
import pandas as pd
from io import StringIO

# Page Config
st.set_page_config(page_title="Data Insight Generator", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
            color: #000000;
        }
        .summary-box {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            line-height: 1.6;
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

# --- Header Images ---
st.markdown("""
    <div class='image-container'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Infoedgelogo.png/500px-Infoedgelogo.png' alt='Info Edge'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/f/fc/Naukri.png?20240329063224' alt='Naukri'>
    </div>
""", unsafe_allow_html=True)

# --- App Title & Text Input ---
st.title("AI-Powered Data Insight Generator")
st.markdown("Paste your tabular data below (CSV-style) and click 'Generate Insights'.")

user_input = st.text_area("Paste Data Here", height=200, placeholder="e.g. Student Name,Math Mark,Science Mark,Biology Mark\nStudent-1,59,95,21")

# --- Insight Functions ---

# Primary insights
def generate_summary(df):
    summaries = []
    for col in df.select_dtypes(include='number').columns:
        max_val = df[col].max()
        min_val = df[col].min()
        mean_val = df[col].mean()
        max_row = df[df[col] == max_val].iloc[0]
        min_row = df[df[col] == min_val].iloc[0]
        summaries.append(f"🔹 In **{col}**, the highest score is **{max_val}** by **{max_row[0]}**, and the lowest is **{min_val}** by **{min_row[0]}**. Average score is **{mean_val:.2f}**.")
    return "\n".join(summaries)

# Second level of insights
def generate_secondary_insight(df):
    insights = []
    df_numeric = df.select_dtypes(include='number')

    # Subject with highest average
    avg_scores = df_numeric.mean()
    top_subject = avg_scores.idxmax()
    insights.append(f"📊 **{top_subject}** has the highest overall average score: **{avg_scores[top_subject]:.2f}**.")

    # Consistency in student scores (standard deviation)
    row_std = df_numeric.std(axis=1)
    most_consistent_index = row_std.idxmin()
    most_consistent_student = df.iloc[most_consistent_index, 0]
    insights.append(f"🔍 **{most_consistent_student}** is the most consistent performer across subjects.")

    # Most varied subject
    score_ranges = df_numeric.max() - df_numeric.min()
    most_varied_subject = score_ranges.idxmax()
    insights.append(f"📈 **{most_varied_subject}** shows the widest score range among all subjects.")

    return "\n".join(insights)

# Final Output Display
def display_insights(df):
    st.subheader("📄 Primary Insight Summary")
    st.markdown(f"<div class='summary-box'>{generate_summary(df)}</div>", unsafe_allow_html=True)

    st.subheader("🧠 Alternative Insight Perspective")
    st.markdown(f"<div class='summary-box'>{generate_secondary_insight(df)}</div>", unsafe_allow_html=True)

# --- Generate Insights ---
if st.button("Generate Insights"):
    try:
        if user_input:
            df = pd.read_csv(StringIO(user_input), sep=",|\t", engine="python")
            display_insights(df)
        else:
            st.warning("⚠️ Please paste some data first.")
    except Exception as e:
        st.error(f"❌ Error processing data: {e}")
