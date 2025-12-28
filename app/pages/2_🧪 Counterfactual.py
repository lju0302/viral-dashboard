# 2_Counterfactual
# 

import streamlit as st

st.set_page_config(page_title="Counterfactual", layout="wide")

st.title("🧪 Counterfactual")
st.caption("K-SARIMAX 소개 / 반사실 예시 / 상위그룹 ATE")

# 상단: 모델 소개 + 선정 이유
st.header("1) 모델 소개 및 선정 이유 (K-SARIMAX)")
with st.container(border=True):
    left, right = st.columns([1, 1])
    with left:
        st.subheader("모델 개요")
        st.write("K-SARIMAX 구조/아이디어 요약 영역")
    with right:
        st.subheader("선정 이유")
        st.write("선정 이유 bullet/근거 영역")

st.divider()

# 반사실 예시(특정 곡)
st.header("2) 반사실 추정 예시 (실제 vs 반사실)")
with st.container(border=True):
    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        st.subheader("곡 선택")
        st.selectbox("곡 선택", options=["(예시) song A", "(예시) song B"], index=0)
        st.info("선택 곡 메타 정보 카드 영역")
    with c2:
        st.subheader("설정")
        st.slider("윈도우/기간", 0, 100, 50)
        st.checkbox("onset 표시", value=True)
        st.checkbox("신뢰구간 표시", value=False)

st.write("")
with st.container(border=True):
    st.subheader("라인플롯: Observed vs Counterfactual")
    st.info("여기에 실제/반사실 라인플롯 배치")

st.divider()

# 상위그룹 ATE
st.header("3) 상위 그룹의 ATE")
with st.container(border=True):
    left, right = st.columns([1, 1])
    with left:
        st.subheader("ATE 요약")
        st.metric("Top group ATE", "—")
        st.metric("Cumulative lift", "—")
    with right:
        st.subheader("분포/비교")
        st.info("그룹별 ATE bar/box/violin 등 배치 영역")

with st.expander("상세 테이블 보기", expanded=False):
    st.info("상위 그룹 ATE 테이블(정렬/필터) 영역")
