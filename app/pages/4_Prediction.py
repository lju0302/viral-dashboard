import streamlit as st
from utils import make_dummy_data

df = make_dummy_data()

st.title("🔎 Explore (전곡 검증용)")

song = st.selectbox("곡 선택", df["song_id"])

row = df[df["song_id"] == song].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Retention", round(row["retention"], 2))
col2.metric("Reactivity", round(row["reactivity"], 2))
col3.metric("XGB Prob", round(row["xgb_prob"], 2))
