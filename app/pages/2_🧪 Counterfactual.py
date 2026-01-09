# 2_Counterfactual
# 

import streamlit as st

st.set_page_config(page_title="Counterfactual", layout="wide")

st.title("🧪 Counterfactual")
st.caption("K-SARIMAX 소개 / 반사실 예시")

# 상단: 모델 소개 + 선정 이유
st.header("1) 모델 소개 및 선정 이유 (K-SARIMAX)")
with st.container(border=True):
    left, right = st.columns([1, 1])
    with left:
        st.subheader("모델 개요")
        st.subheader("👌직관으로 설명하는 ARIMA")
        st.markdown("""
        우리는 어제 들은 음악을 오늘도 듣고, 내일도 들을 것입니다.
        또한, 출근과 쉬는 날 등의 행동 패턴에 따라서 청취 패턴이 유사하게 반복되기도 합니다.
        이를테면, 출근하는 시간 마다 특정 플레이리스트를 듣는 식이죠. 
        이런 식으로, 음악 청취는 시간에 따라 누적되는 패턴과 변화 추세를 보입니다.
        이러한 패턴과 추세를 포착하는 데에 적합한 모델이 바로 **ARIMA** 모델입니다.
                    """)
        st.markdown("### 🧠 Model Overview")

        st.markdown("""
        **ARIMA 모델**은 과거의 흐름을 바탕으로 미래를 예측하는 **시계열 모델**로,  
        시간에 따라 누적되는 **패턴**과 **변화 추세**를 포착하는 데 적합합니다.

        본 연구에서는 음악 스트리밍의 특성을 보다 잘 반영하기 위해,     
        ARIMA를 확장한 **K-SARIMAX 모델**을 사용하였습니다.  
        이 모델은 유사한 성장 패턴을 가진 곡들을 그룹화(K)하고,  
        주기적 반복 패턴(S)과 외부 영향 요인(X)을 함께 고려하는 것이 특징입니다.
        """, unsafe_allow_html=False)

    with right:
        st.markdown("### 🔍 Key Characteristics of K-SARIMAX")
        st.markdown("""
        #### 📅 **계절성 반영 (Seasonality)**
        음악 스트리밍 데이터는 **요일 단위의 반복적인 소비 패턴**을 보입니다.  
        실제 분석 결과, **7일 주기 계절성**을 포함했을 때 예측 오차(**RMSE**)가 가장 크게 감소하여,  
        **주간 단위 반복 구조**를 모델에 명시적으로 반영하였습니다.

        #### 🌐 **외생 변수 통합 (Exogenous Variables)**
        단순한 과거 스트리밍 수치뿐만 아니라,  
        **TikTok 바이럴 노출**과 같은 **SNS 활동**,  
        그리고 **곡·아티스트·기획사 메타데이터**를 외부 변수로 포함하여  
        스트리밍 변화의 **원인**을 보다 직접적으로 설명합니다.

        #### 🧩 **그룹별 맞춤형 모델링 (Cluster-based Modeling)**
        모든 곡을 하나의 모델로 설명하는 대신,  
        **성장 곡선이 유사한 곡들**을 **클러스터(K)**로 묶어  
        각 그룹에 **최적화된 SARIMAX 모델**을 개별적으로 적합시켰습니다.  
        이를 통해 바이럴 반응의 **이질성(Heterogeneity)**을 보다 정밀하게 포착할 수 있습니다.
        """)
st.divider()

# 반사실 예시(특정 곡)
st.header("2) 반사실 추정 예시 (실제 vs 반사실)")
# with st.container(border=True):
#     c1, c2 = st.columns([1.1, 0.9])
#     with c1:
#         st.subheader("곡 선택")
#         st.selectbox("곡 선택", options=["(예시) song A", "(예시) song B"], index=0)
#         st.info("선택 곡 메타 정보 카드 영역")
#     with c2:
#         st.subheader("설정")
#         st.slider("윈도우/기간", 0, 100, 50)
#         st.checkbox("onset 표시", value=True)
#         st.checkbox("신뢰구간 표시", value=False)

# st.write("")
# with st.container(border=True):
#     st.subheader("라인플롯: Observed vs Counterfactual")
#     st.info("여기에 실제/반사실 라인플롯 배치")

# st.divider()

# app/pages/2_🧪 Counterfactual.py

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

# =========================
# 파일 경로
# =========================
DATA_PATH = Path("src/ksarimax_counterfactual_predictions_sample.csv")

# =========================
# 데이터 로딩
# =========================
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    # 컬럼명 자동 대응 (필요 최소한만)
    rename_map = {}
    if "y_true" in df.columns:
        rename_map["y_true"] = "observed"
    if "y_cf" in df.columns:
        rename_map["y_cf"] = "counterfactual"

    df = df.rename(columns=rename_map)

    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data(DATA_PATH)

song_ids = df["song_id"].drop_duplicates().tolist()
song_map = {
    f"샘플 곡 {i+1}": sid
    for i, sid in enumerate(song_ids[1:])
}

# =========================
# 곡 선택
# =========================

selected_label = st.selectbox(
"예시 곡 선택",
list(song_map.keys())
)

selected_song = song_map[selected_label]
df_all = df[df["song_id"] == selected_song].sort_values("date")


# =========================
# 컬럼 설정(슬라이더, 결과 요약)
# =========================
# =========================
# 탭 구성
#   1) 실제 vs 반사실
#   2) 누적효과
# =========================
tab1, tab2 = st.tabs(["1) 실제 vs 반사실", "2) 누적효과"])

# -------------------------
# TAB 1: 실제 vs 반사실 (그래프 옆에 결과 요약만)
# -------------------------
with tab1:
    # 기간 슬라이더는 탭 내부로
    max_days = min(100, len(df_all))
    window_days = st.slider(
        "관측 기간 (일)",
        min_value=7,
        max_value=max_days,
        value=min(30, max_days),
        step=1,
        help="슬라이더를 움직이며 관측 기간에 따른 변화를 확인해 보세요",
        key="window_days_tab1",
    )

    df_s = df_all.head(window_days).copy()

    # 그래프/요약 병렬
    gcol, scol = st.columns([1.25, 0.75], gap="large")

    with gcol:
        st.subheader("실제 스트리밍 vs 반사실 시나리오")
        st.caption("일별 스트리밍 흐름을 비교합니다.")

        fig1 = go.Figure()

        fig1.add_trace(
            go.Scatter(
                x=df_s["date"],
                y=df_s["observed"],
                mode="lines",
                name="Observed",
                line=dict(width=3),
            )
        )

        if "counterfactual" in df_s.columns:
            fig1.add_trace(
                go.Scatter(
                    x=df_s["date"],
                    y=df_s["counterfactual"],
                    mode="lines",
                    name="Counterfactual",
                    line=dict(dash="dash"),
                )
            )

        # treat_date 표시 (윈도우 안에 들어올 때만)
        treat_date = None
        if "treat_date" in df_all.columns and df_all["treat_date"].notna().any():
            treat_date = pd.to_datetime(df_all["treat_date"].dropna().iloc[0])
        if treat_date is not None and (df_s["date"].min() <= treat_date <= df_s["date"].max()):
            fig1.add_vline(
                x=treat_date,
                line_width=2,
                line_dash="dot",
                annotation_text="Viral onset",
                annotation_position="top left",
            )

        fig1.update_layout(
            height=450,
            xaxis_title="Date",
            yaxis_title="Streaming",
            template="plotly_white",
            legend_title="Series",
        )

        st.plotly_chart(fig1, use_container_width=True)

    with scol:
        st.subheader("결과 요약")
        with st.container(border=True):
            observed_sum = float(df_s["observed"].sum())
            if "counterfactual" in df_s.columns:
                cf_sum = float(df_s["counterfactual"].sum())
            else:
                cf_sum = None

            st.metric("🗓️ 관측 기간 (days)", int(window_days))
            st.metric("🎶 실제 스트리밍 누적", f"{int(observed_sum):,}")

            if cf_sum is not None:
                st.metric("❓ 반사실 누적", f"{int(cf_sum):,}")
                st.caption("반사실: 틱톡 바이럴이 없었다면 예상되는 스트리밍 누적치")

# -------------------------
# TAB 2: 누적효과 (그래프 옆에 ‘틱톡 증가효과(몇회)’ 요약)
# -------------------------
with tab2:
    max_days = min(100, len(df_all))
    window_days2 = st.slider(
        "관측 기간 (일)",
        min_value=7,
        max_value=max_days,
        value=min(30, max_days),
        step=1,
        help="누적 효과를 계산할 기간을 선택하세요",
        key="window_days_tab2",
    )

    df_s2 = df_all.head(window_days2).copy()

    gcol2, scol2 = st.columns([1.25, 0.75], gap="large")

    with gcol2:
        st.subheader("누적 효과 (Cumulative lift)")
        st.caption("틱톡 바이럴이 스트리밍에 미친 누적 효과를 나타냅니다.")

        if "counterfactual" not in df_s2.columns:
            st.info("Counterfactual 결과가 없어 누적 효과를 계산할 수 없습니다.")
        else:
            df_s2["effect"] = df_s2["observed"] - df_s2["counterfactual"]
            df_s2["cum_effect"] = df_s2["effect"].cumsum()

            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=df_s2["date"],
                    y=df_s2["cum_effect"],
                    mode="lines",
                    name="Cumulative lift",
                    line=dict(width=3),
                )
            )

            # treat_date 표시 (윈도우 안에 들어올 때만)
            treat_date2 = None
            if "treat_date" in df_all.columns and df_all["treat_date"].notna().any():
                treat_date2 = pd.to_datetime(df_all["treat_date"].dropna().iloc[0])
            if treat_date2 is not None and (df_s2["date"].min() <= treat_date2 <= df_s2["date"].max()):
                fig2.add_vline(
                    x=treat_date2,
                    line_width=2,
                    line_dash="dot",
                    annotation_text="Viral onset",
                    annotation_position="top left",
                )

            fig2.update_layout(
                height=450,
                xaxis_title="Date",
                yaxis_title="Cumulative lift",
                template="plotly_white",
            )

            st.plotly_chart(fig2, use_container_width=True)

    with scol2:
        st.subheader("결과 요약")
        with st.container(border=True):
            st.metric("🗓️ 관측 기간 (days)", int(window_days2))

            if "counterfactual" in df_s2.columns:
                inc_effect = float((df_s2["observed"] - df_s2["counterfactual"]).sum())
                st.metric("🚀 틱톡이 가져다 준 증가효과 (몇 회 증가했는지)", f"{int(inc_effect):,}")
                st.caption("정의: (실제 스트리밍) − (틱톡이 없었을 때의 반사실)의 기간 누적 합")
            else:
                st.metric("🚀 틱톡 증가효과", "N/A")
                st.caption("Counterfactual 컬럼이 없어 계산 불가")


# 상위그룹 ATE
# st.header("3) 상위 그룹의 ATE")
# with st.container(border=True):
#     left, right = st.columns([1, 1])
#     with left:
#         st.subheader("ATE 요약")
#         st.metric("Top group ATE", "—")
#         st.metric("Cumulative lift", "—")
#     with right:
#         st.subheader("분포/비교")
#         st.info("그룹별 ATE bar/box/violin 등 배치 영역")

# with st.expander("상세 테이블 보기", expanded=False):
#     st.info("상위 그룹 ATE 테이블(정렬/필터) 영역")
