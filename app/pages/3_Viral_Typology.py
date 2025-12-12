import streamlit as st
from utils import make_dummy_data

df = make_dummy_data()

st.title("3️⃣ Viral Typology")

st.markdown("""
성장 곡선 형태에 따라 바이럴 유형을 구분합니다.
""")

st.dataframe(
    df[["song_id", "retention", "reactivity"]]
        .assign(type=lambda x:
            ["High-High" if r>0.5 and t>0.5 else "Other"
             for r, t in zip(x.retention, x.reactivity)]
        )
)
