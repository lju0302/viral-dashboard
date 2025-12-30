import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# 데이터 불러오기
# @st.cache_data
# def load_data():

# 기본 세팅
st.set_page_config(
    page_title="All That Beats Is Not The Hit 📢",
    layout="wide"
)

# 0. 표지 영역
## 0-1. 제목
st.title("All That Beats Is Not The Hit 📢")
st.markdown("**Inside Virality: Retention, Reactivity and Conterfactual Estimation of Streaming**")

## 0-2. Research question
# st.markdown("""
#             <aside style ="background-color: #f0f4f8; padding: 12px 16px; border-left: 6px solid #3b82f6; margin-bottom: 20px;"> 
#             📌 본 분석에서 다룰 질문들 \n
#             1. 틱톡이 스트리밍에 순수한 인과적 효과는? \n
#             2. 바이럴의 유형과 특성은?
#             </aside>""", unsafe_allow_html=True)
# st.text("\n")

st.markdown("""
<div style="
    background-color:#f5f9ff;
    padding:16px 18px;
    border-left:5px solid #3b82f6;
    border-radius:6px;
    margin-bottom:20px;
">
  <div style="font-weight:600; font-size:16px; margin-bottom:8px;">
    📌 연구 질문
  </div>
  <ul style="margin:0; padding-left:18px;">
    <li>틱톡 노출이 음악 스트리밍에 기여하는 <b>인과적 효과</b>는 얼마나 되는가?</li>
    <li>바이럴은 어떤 <b>유형</b>으로 구분되며, 각 유형의 <b>특성</b>은 무엇인가?</li>
  </ul>
</div>
""", unsafe_allow_html=True)


# 1. KPI 카드 영역
st.subheader("핵심 KPI 요약")

# KPI 컬럼 스타일 지정
st.markdown("""
<style>
.kpi-card {
    background-color: #f9fafb;
    border-radius: 14px;
    padding: 14px 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

.kpi-label {
    font-size: 0.95rem;          /* 기존보다 크게 */
    font-weight: 700;            /* 굵게 */
    color: #374151;              /* 더 진한 회색 */
    letter-spacing: 0.01em;      /* 과한 spacing 제거 */
    text-transform: none;        /* 대문자 제거 → 가독성 향상 */
}

.kpi-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #111827;
    margin-top: 6px;
}

.kpi-sub {
    font-size: 0.82rem;
    color: #6b7280;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
##############################################
# 더미 데이터 임시 사용중, 데이터 로드 후 코드 교체 필요 ☣️☠️‼️
##############################################
n_songs = "-" #songs.shape[0]
date_min = "-"  #streaming["date"].min().date()
date_max = "-" #streaming["date"].max().date()
avg_ate = "-" #songs["ate_stream"].mean() * 100
n_clusters = "-" #songs["cluster"].nunique()

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">총 곡 수</div>
        <div class="kpi-value">{n_songs}</div>
        <div class="kpi-sub">분석 대상 트랙 개수</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">데이터 기간</div>
        <div class="kpi-value">{date_min} ~ {date_max}</div>
        <div class="kpi-sub">Spotify 일별 스트리밍 기준</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">바이럴 유형의 수 (K)</div>
        <div class="kpi-value">{n_clusters}</div>
        <div class="kpi-sub">K-SARIMAX 기반 그룹</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">상위그룹 ATE (TikTok → Streaming)</div>
        <div class="kpi-value">{avg_ate}</div>
        <div class="kpi-sub"> 성장패턴 상위 그룹(k = 3,4) 증분 추정치</div>
    </div>
    """, unsafe_allow_html=True)

st.text("\n")

## 0-3. 섹션 안내
## Explanatory -> Counterfact -> Viral Typology -> Prediction (-> Strategy) 워크플로우 이미지(Mermaid)

st.subheader("Sections")

cards = [
    ("Explanatory", "Patterns & heterogeneity signals", "onset patterns, distributions, segments", "pages/1_📈 Explanatory.py", "📈"),
    ("Counterfactual", "What-if baseline & causal lift", "observed vs counterfactual, ATE/cumulative lift", "pages/2_🧪 Counterfactual.py", "🧪"),
    ("Viral Typology", "Retention × Reactivity quadrants", "Q1–Q4 mix, representative cases", "pages/3_🧭 Viral_Typology.py", "🧭"),
    ("Prediction", "Early signals & probabilities", "quadrant probabilities, feature importance", "pages/4_🔮 Prediction.py", "🔮"),
    ("Strategy", "Playbook & KPIs", "actions by type, monitoring metrics", "pages/5_🎯 Strategy.py", "🎯"),
]

# 3열 그리드(원하면 2열로 바꿔도 됨)
cols = st.columns(3)
for i, (title, subtitle, examples, target, icon) in enumerate(cards):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"### {icon} {title}")
            st.caption(subtitle)
            st.markdown(f"- {examples}")
            st.page_link(target, label="Go!", icon="➡️")



