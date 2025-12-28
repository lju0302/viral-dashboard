# 1_Explanatory.py
# 데이터 탐색과 개괄을 위한 페이지 구성
# 

import streamlit as st

st.set_page_config(page_title="Explanatory", layout="wide")

st.title("📈 Explanatory")
st.caption("플랫폼 이질성 / ATE 개념 / 스토리 / 데이터 소개 / 성장곡선 K-Means")

# 상단 요약 박스
with st.container(border=True):
    st.subheader("요약")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("TikTok–Streaming 상관", "—")
    with c2:
        st.metric("Insta–Streaming 상관", "—")
    with c3:
        st.metric("분석 대상 곡 수", "—")

st.divider()

#=============================================================

# 1) 플랫폼 차이
st.header("1) 플랫폼 차이: TikTok vs Instagram")
left, right = st.columns([1.2, 1])
with left:
    with st.container(border=True):
        st.subheader("비교 시각화")
        st.info("여기에 플랫폼별 상관/산점도/요약 차트 배치")
with right:
    with st.container(border=True):
        st.subheader("핵심 메시지")
        st.write("여기에 한 줄 요약/해석 텍스트")
        st.write("여기에 보조 설명 텍스트")

st.divider()

#=============================================================

# 2) ATE란?
st.header("2) ATE란?")
with st.container(border=True):
    colA, colB = st.columns([1, 1])
    with colA:
        st.subheader("개념 설명")
        st.write("ATE 정의/직관/단위 설명 영역")
    with colB:
        st.subheader("수식/예시")
        st.info("ATE 수식 또는 아주 짧은 예시를 넣는 영역")

st.divider()

#=============================================================

# 3) 보고서 스토리/향후 연구방안
st.header("3) 보고서 스토리 & 향후 연구방안")
with st.container(border=True):
    st.subheader("스토리라인")
    st.write("Explanatory → Counterfactual → Typology → Prediction 흐름 설명 영역")
    st.subheader("향후 연구방안")
    st.write("향후 연구방안 bullet 영역")

st.divider()

#=============================================================

# 4) 사용 데이터 소개
st.header("4) 사용 데이터 소개")
with st.container(border=True):
    a, b = st.columns([1, 1])
    with a:
        st.subheader("수집/정의")
        st.write("수집방안 및 데이터 구성 설명 영역")
    with b:
        st.subheader("예시 데이터셋")
        st.info("예시 테이블/스키마/샘플 dataframe 표시 영역")

st.divider()

#=============================================================

# 5) 성장곡선 유형분류 (K-Means)
st.header("5) 성장곡선 유형분류 (K-Means)")
with st.container(border=True):
    t1, t2 = st.tabs(["클러스터 요약", "대표 곡/패턴"])
    with t1:
        st.info("클러스터 분포/센트로이드/요약 차트 영역")
    with t2:
        left2, right2 = st.columns([1, 1])
        with left2:
            st.info("대표 곡 선택/리스트 영역")
        with right2:
            st.info("선택 곡의 성장곡선(라인플롯) 영역")

#=============================================================
