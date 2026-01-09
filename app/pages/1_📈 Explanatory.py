# 1_Explanatory.py
# 데이터 탐색과 개괄을 위한 페이지 구성
# 

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# st.set_page_config(page_title="Explanatory", layout="wide")

# st.title("📈 Explanatory")
# st.caption("플랫폼 이질성 / ATE 개념 / 스토리 / 데이터 소개 / 성장곡선 K-Means")

# 상단 요약 박스
# with st.container(border=True):
#     st.subheader("요약")
#     c1, c2, c3 = st.columns(3)
#     with c1:
#         st.metric("TikTok–Streaming 상관", "—")
#     with c2:
#         st.metric("Insta–Streaming 상관", "—")
#     with c3:
#         st.metric("분석 대상 곡 수", "—")

# st.divider()

#=============================================================
# 내용 구성 후보 1번입니다.

import plotly.express as px

st.set_page_config(page_title="Explanatory", layout="wide")

st.title("📈 Explanatory")
st.caption("플랫폼 이질성 / 인과추론 & ATE 개념 / 데이터 소개")

# --- Section 1: 플랫폼 이질성 (The "Why") ---
st.header("1️⃣ 왜 TikTok인가? (플랫폼 이질성)")
col1, col2 = st.columns([1.2, 1])

with col1:
    # 실제 데이터가 있다면 px.bar 등으로 교체
    st.subheader("Platform-Streaming Correlation")
    st.image('src/image/platform_diff.jpeg')
    st.caption("그래프 설명: 틱톡(TikTok)은 인스타그램 대비 스트리밍 상승과 더 강력한 시차 상관관계를 보임")

with col2:
    st.write("### 핵심 발견")
    st.success("틱톡의 노출은 약 n일의 시차를 두고 스포티파이 재생수 증가와 강한 양의 상관관계를 가집니다.")
    st.info("이 결과에 따라, 본 연구는 '틱톡 바이럴'을 핵심 처치(Treatment)로 설정하여 인과 분석을 수행합니다.")

st.divider()

# --- Section 2: 인과관계와 ATE (The "How") ---
st.header("2️⃣ 상관관계를 넘어 인과관계로")
c1, c2 = st.columns(2)

with c1:
    st.subheader("⚠️ 상관관계의 함정")
    st.write("단순히 '바이럴 이후 재생수가 올랐다'는 사실만으로는 바이럴의 순수 효과를 알 수 없습니다. 자연적인 차트인이나 다른 마케팅 효과가 섞여 있기 때문입니다.")

with c2:
    st.subheader("🎯 ATE (Average Treatment Effect)")
    st.write("**반사실(Counterfactual) 추정:** '바이럴이 없었을 때의 가상 시나리오'를 생성하여, 실제 데이터와의 차이만큼을 바이럴의 '순수 기여도'로 정의합니다.")
    show_formula = st.toggle("📐 ATE 수식으로 확인하기", value=False)

    if show_formula:
        st.markdown("""
    **(1) 전처리 단계** - 노이즈 제거

    - 3일 이동평균:  
    $\\tilde{Y}_{i,t} = \\dfrac{Y_{i,t} + Y_{i,t-1} + Y_{i,t-2}}{3}$

    - 로그 변환:  
    $Z_{i,t} = \\log(\\tilde{Y}_{i,t} + 1)$

    - 로그 차분:  
    $\\Delta Z_{i,t} = Z_{i,t} - Z_{i,t-1}$

    &nbsp;

    **(2) 곡 단위 누적 효과 (Counterfactual Lift)**

    - 전처리된 시계열 기준 증가량:  
    $\\Delta_{i,t} = \\Delta Z_{i,t}^{\\text{obs}} - \\Delta Z_{i,t}^{\\text{cf}}$

    - 곡 $i$의 누적 효과:  
    $\\Delta_i = \\sum_{t=1}^{T} \\left( \\Delta Z_{i,t}^{\\text{obs}} - \\Delta Z_{i,t}^{\\text{cf}} \\right)$

    &nbsp;

    **(3) 클러스터 $k$ 내 평균 처리 효과 (ATE)**

    - 클러스터 평균 처리 효과:  
    $\\text{ATE}_k = \\dfrac{1}{N_k} \\sum_{i \\in \\mathcal{I}_k} \\sum_{t=1}^{T} \\left( \\Delta Z_{i,t}^{\\text{obs}} - \\Delta Z_{i,t}^{\\text{cf}} \\right)$
    """)

        st.caption(
            "※ $+1$은 스트리밍 값이 0인 구간에서도 로그 변환이 가능하도록 하기 위한 안정화 처리이며, "
            "ATE는 전처리된 로그 차분 시계열 기준의 평균 누적 증가 효과를 의미합니다."
        )



st.divider()

# --- Section 3: 데이터 파이프라인 (The "Tech Stack") ---
st.header("3️⃣ 데이터 수집 및 관리")

# 단계별 컬럼 구성
step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("### **Step 1. 데이터 수집n**")
    st.info("""
    - **Music Meta**: Tunebat, Kworb, Spotify API (피쳐, 차트)
    - **Performance**: Chartmetric (일별 스트리밍, 인기도)
    - **Social**: Songstats (SNS 노출량)
    - **Tool**: Python(Selenium, statsmodels and more...), PostgreSQL
    """)

with step2:
    st.markdown("### **Step 2. 데이터 적재 (DB)**")
    # Supabase 로고나 아이콘 강조
    st.write("### 🌩️ **Supabase** (PostgreSQL)")
    st.write("수집된 1,158곡의 시계열 데이터를 클라우드 DB에 적재하여 데이터 무결성을 확보하고, 곡/아티스트/소속사별 id를 부여해 데이터 간 연결성을 확보했습니다.")
    st.write("🎨 데이터베이스 ERD : ")
    st.image('src/image/erd.png')


with step3:
    st.markdown("### **Step 3. 데이터 미리보기**")
    st.caption("실제 분석에 사용된 데이터 구조와 예시를 확인할 수 있습니다.")

    tab_song, tab_stream, tab_social = st.tabs(
        ["🎵 Song / Artist", "📈 Streaming", "📱 Tiktok"]
    )

    # -------------------------
    # Tab 1: Song / Artist
    # -------------------------
    with tab_song:
        song_df = pd.read_csv("src/data_preview/song_meta_sample.csv")
        st.dataframe(song_df, use_container_width=True)
        st.markdown(
            "<div style='font-size:12px; color:gray;'>"
            "*곡 ID, 곡명, 아티스트, 발매연도, 소속사 등 메타 정보*"
            "</div>",
            unsafe_allow_html=True
        )

    # -------------------------
    # Tab 2: Streaming
    # -------------------------
    with tab_stream:
        streaming_df = pd.read_csv("src/data_preview/streaming_sample.csv")
        st.dataframe(streaming_df, use_container_width=True)
        st.markdown(
            "<div style='font-size:12px; color:gray;'>"
            "*1,158곡의 일별 Spotify 스트리밍 데이터 (2023–2024)*"
            "</div>",
            unsafe_allow_html=True
        )

    # -------------------------
    # Tab 3: Tiktok
    # -------------------------
    with tab_social:
        sns_df = pd.read_csv("src/data_preview/tiktok_sample.csv")
        st.dataframe(sns_df, use_container_width=True)
        st.markdown(
            "<div style='font-size:12px; color:gray;'>"
            "*TikTok 일별 조회수·좋아요*"
            "</div>",
            unsafe_allow_html=True
        )

