# 대시보드 홈 페이지입니다.

import streamlit as st
from utils import make_dummy_data  # 위 코드 복붙해도 됨

st.set_page_config(page_title="Viral Story Dashboard", layout="wide")

df = make_dummy_data()

st.title("🎵 Viral Dynamics Story Dashboard")
st.markdown("""
이 대시보드는  
**이질성 → 순수 효과 → 바이럴 유형 → 전략적 시사점**  
을 스토리 형태로 보여줍니다.
""")

# session_state 초기화
if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

st.subheader("📌 대표 사례")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("모범 사례"):
        st.session_state.selected_song = df.iloc[0]["song_id"]

with col2:
    if st.button("역전 사례"):
        st.session_state.selected_song = df.iloc[10]["song_id"]

with col3:
    if st.button("실패 사례"):
        st.session_state.selected_song = df.iloc[20]["song_id"]

if st.session_state.selected_song:
    st.success(f"선택된 곡 ID: {st.session_state.selected_song}")
