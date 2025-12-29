import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. Database & Page Configuration
engine = create_engine('postgresql://airflow:airflow@postgres:5432/airflow')
st.set_page_config(page_title="Davut Cano - MLOps Dashboard", layout="wide")

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_sql("SELECT * FROM movie_reviews WHERE model_prediction IS NOT NULL", engine)
    if not df.empty:
        df['ingested_at'] = pd.to_datetime(df['ingested_at'])
        df = df.sort_values('ingested_at')
    return df

df = load_data()

# --- SIDEBAR (SYSTEM STATUS) ---
st.sidebar.title("🛠️ System Control")
st.sidebar.success("Pipeline: ACTIVE")
if not df.empty:
    st.sidebar.write(f"**Total Records:** {len(df)}")
    st.sidebar.write(f"**Last Sync:** {df['ingested_at'].max().strftime('%H:%M:%S')}")

st.title("🛡️ Spoiler Detection MLOps Command Center")
st.markdown("---")

if df.empty:
    st.warning("Database is empty. Please trigger the Airflow pipeline to generate predictions.")
    st.stop()

# --- TOP PANEL: GAUGE CHARTS (KPIs) ---
c1, c2, c3 = st.columns(3)
accuracy = (df['spoiler_tag'] == df['model_prediction']).mean()
spoiler_ratio = (df['model_prediction'] == 1).mean()

with c1:
    fig_acc = go.Figure(go.Indicator(
        mode = "gauge+number", value = accuracy * 100,
        title = {'text': "Model Accuracy (%)"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
    ))
    fig_acc.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_acc, use_container_width=True)

with c2:
    fig_ratio = go.Figure(go.Indicator(
        mode = "gauge+number", value = spoiler_ratio * 100,
        title = {'text': "Spoiler Density (%)"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "red"}}
    ))
    fig_ratio.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_ratio, use_container_width=True)

with c3:
    # Cumulative Data Ingestion Chart
    df['cumulative_count'] = range(1, len(df) + 1)
    fig_growth = px.area(df, x='ingested_at', y='cumulative_count', title="Data Ingestion Rate")
    fig_growth.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_growth, use_container_width=True)

# --- MAIN TABS ---
t1, t2, t3, t4 = st.tabs(["🏠 Overview", "📉 Performance & Drift", "📊 Content Analysis", "🧪 Live Test"])

with t1:
    st.subheader("Spoiler Distribution by Movie")
    st.plotly_chart(px.histogram(df, x="movie", color="model_prediction", barmode="group", 
                                 title="Review Classifications per Movie",
                                 labels={'model_prediction': 'Prediction (1:Spoiler)'}), use_container_width=True)
    st.subheader("Recent Activity Log")
    st.dataframe(df[['movie', 'review_detail', 'model_prediction']].tail(10), use_container_width=True)

with t2:
    st.subheader("Model Drift Analysis (Accuracy over Time)")
    df['match'] = (df['spoiler_tag'] == df['model_prediction']).astype(int)
    drift_df = df.resample('5min', on='ingested_at')['match'].mean().ffill().reset_index()
    st.plotly_chart(px.line(drift_df, x='ingested_at', y='match', title="System Accuracy Stability", markers=True), use_container_width=True)
    
    st.divider()
    st.subheader("Confusion Matrix (Error Breakdown)")
    z = pd.crosstab(df['spoiler_tag'], df['model_prediction'])
    # Fix potential missing classes
    for i in [0, 1]: 
        if i not in z.columns: z[i] = 0
        if i not in z.index: z.loc[i] = 0
    z = z.sort_index(axis=0).sort_index(axis=1)
    fig_cm = ff.create_annotated_heatmap(z.values, x=['Pred: Clean', 'Pred: Spoiler'], y=['Actual: Clean', 'Actual: Spoiler'], colorscale='Blues')
    st.plotly_chart(fig_cm, use_container_width=True)

with t3:
    col_x, col_y = st.columns(2)
    with col_x:
        st.subheader("Hierarchical Breakdown")
        fig_sun = px.sunburst(df, path=['movie', 'model_prediction'], title="Movie -> Prediction Hierarchy")
        st.plotly_chart(fig_sun, use_container_width=True)
        

    with col_y:
        st.subheader("Top Spoiler Keywords")
        spoiler_df = df[df['model_prediction'] == 1]
        if not spoiler_df.empty:
            words = " ".join(spoiler_df['review_detail']).lower().split()
            filtered = [w for w in words if len(w) > 3]
            w_counts = pd.Series(filtered).value_counts().head(10).reset_index()
            w_counts.columns = ['Keyword', 'Frequency']
            fig_bar = px.bar(w_counts, x='Frequency', y='Keyword', orientation='h', 
                             color='Frequency', color_continuous_scale='Reds')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Insufficient data for keyword analysis.")

with t4:
    st.subheader("Real-Time Inference")
    input_text = st.text_area("Enter a movie review to analyze:")
    if st.button("Run AI Analysis"):
        with st.spinner('Model is processing...'):
            tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            model = AutoModelForSequenceClassification.from_pretrained("/opt/airflow/models")
            inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                pred = torch.argmax(model(**inputs).logits, dim=-1).item()
            if pred == 1: st.error("🚨 SPOILER ALERT: This comment contains spoilers!")
            else: st.success("✅ SAFE: No spoilers detected in this comment.")

st.sidebar.markdown("---")
if st.sidebar.button("💾 Clear Cache & Refresh"):
    st.cache_data.clear()