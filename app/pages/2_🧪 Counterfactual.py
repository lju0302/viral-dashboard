# 2_Counterfactual
# 

import streamlit as st

st.set_page_config(page_title="Counterfactual", layout="wide")

st.title("🧪 Counterfactual")
st.caption("K-SARIMAX 소개 / 반사실 예시")

# 스타일 지정
def highlight_box(title: str, body: str, icon: str = "💡"):
    st.markdown(
        f"""
<div style="
    background: linear-gradient(135deg, #f8fafc, #eef2ff);
    border: 1px solid #dbeafe;
    border-left: 8px solid #3b82f6;
    border-radius: 16px;
    padding: 10px 16px;
    margin: 10px 0;
    box-shadow: 0 6px 18px rgba(0,0,0,0.04);
">
<div style="
    font-size: 1.3rem;
    font-weight: 800;
    margin-bottom: 14px;
    color: #1e3a8a;
">
    {icon} {title}
</div>
<div style="
    font-size: 1.2rem;
    line-height: 1.7;
    color: #0f172a;
    white-space: pre-wrap;
">
    {body}
</div>
</div>
""",
unsafe_allow_html=True,
    )



# 상단: 모델 소개 + 선정 이유
st.header("1) 모델 소개 및 선정 이유 (K-SARIMAX)")
t1, t2 = st.tabs(["ARIMA에 대해", "K-SARIMAX 모델의 특징"])

with t1:
    arima_text = """
우리는 어제 들은 음악을 오늘도 듣고, 내일도 들을 것입니다. \n또한, 출근과 쉬는 날 등의 행동 패턴에 따라서 청취 패턴이 유사하게 반복되기도 합니다. \n이를테면, 출근하는 시간마다 특정 플레이리스트를 듣는 식이죠. 
이런 식으로 음악 청취는 시간에 따라 누적되는 패턴과 변화 추세를 보입니다.\n이러한 패턴과 추세를 포착하는 데에 적합한 모델이 바로 **ARIMA** 모델입니다.
"""

    highlight_box(
        title="직관으로 이해하는 ARIMA",
        body=arima_text,
        icon="👌"
    )
    toggle = st.toggle('더 자세한 설명 보기')
    if toggle:
        with st.container(border = True):
            st.markdown("""### ARIMA를 구성하는 세 가지 요소
                        - AR(Autoregressive, 자기회귀) : 현재 시점의 값이 자신의 과거 관측값(과거 데이터 포인트)들에 대한 선형 결합으로 설명됩니다. 'p'개의 과거 값을 사용하며, 데이터의 추세(Trend)를 모델링하는 데 도움을 줍니다.
    - I(Integrated, 적분/차분) : 시계열 데이터가 정상성(Stationarity)을 갖도록 만들기 위해 데이터를 차분(difference)하는 과정입니다. 정상성을 만족하지 않는(비정상) 시계열 데이터를 정상 시계열로 변환하며, 'd'번 차분합니다.
    - MA(Moving Average, 이동평균) : 개념: 현재 시점의 값이 과거 예측 오차들의 선형 결합으로 설명됩니다. 'q'개의 과거 오차 항을 사용하여 시계열의 불규칙한 패턴이나 노이즈를 모델링합니다.
                """)

with t2:
    st.markdown("### 🔍 Key Characteristics of K-SARIMAX")
    c_1, c_2, c_3 = st.columns(3, gap="large")
    with c_1:
        st.markdown("""
        #### 📅 **계절성 반영 (S)**""")
        st.metric("계절성 반영으로 감소한 RMSE", "94.2%")
        st.caption(""" 변화: 0.00479 (ARIMAX) → 0.00028 (SARIMAX) """)
        st.info("""
        음악 스트리밍 데이터는 **요일 단위의 반복적인 소비 패턴**을 보입니다. 실제 분석 결과, **7일 주기 계절성**을 포함했을 때 예측 오차(**RMSE**)가 가장 크게 감소하였고, 이러한 **주간 단위 반복 구조**를 모델에 명시적으로 반영하였습니다.""")
        

    with c_2:
        st.markdown("""
        #### 💥 **외생 변수 결합 (X)**""")
        st.metric("결합한 외생 변수 수", "6개")
        st.caption("tiktok views/likes, 뮤직비디오 존재 여부/반응 지표, 뉴스기사 노출")
        st.info("""
        단순한 과거 스트리밍 수치뿐만 아니라, **TikTok 노출**, 그리고 **외부 노출량**을 외부 변수로 포함하여  스트리밍 변화의 **원인**을 보다 직접적으로 설명합니다.""")


    with c_3:
        st.markdown("""
        #### 📦 **그룹별 맞춤형 모델링 (K)**""")
        st.metric("칼만 필터 적용으로 얻은 RMSE 감소", '35.7%')
        st.caption("• SARIMAX : RMSE 0.00028 → KSARIMAX : RMSE 0.00018")
        st.info("""
        모든 곡을 하나의 모델로 설명하는 대신, **성장 곡선이 유사한 곡들**을 묶어 각 그룹에 **최적화된 SARIMAX 모델**을 개별적으로 적합시켰습니다. 이를 통해 바이럴 반응의 **이질성(Heterogeneity)**을 보다 정밀하게 포착할 수 있습니다.""")
    
    st.caption("언급된 오차는 로그 차분(일일 증가율 차이) 기준으로 측정되었습니다.")
st.divider()

# 반사실 예시(특정 곡)
st.header("2) 반사실 추정 예시 (실제 vs 반사실)")

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
        st.caption("일별 스트리밍 누적의 흐름을 비교합니다.")

        fig1 = go.Figure()

        fig1.add_trace(
            go.Scatter(
                x=df_s["date"],
                y=df_s["observed"],
                mode="lines",
                name="Observed",
                fill = 'tozeroy',
                fillcolor = 'rgba(135, 206, 250, 0.2)',
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
                    fill = 'tozeroy',
                    fillcolor = 'rgba(255, 182, 193, 0.5)',
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

            # ✅ 누적 퍼센트 증가(기간 누적 기준)
            base = df_s2["counterfactual"].sum()
            lift = df_s2["effect"].sum()  # = df_s2["cum_effect"].iloc[-1]
            pct_increase = (lift / base) * 100 if base != 0 else None

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
                st.metric("누적 증가율", f"{pct_increase:.1f}%")
                st.caption("정의: (실제 스트리밍) − (틱톡이 없었을 때의 반사실)의 기간 누적 합")
            else:
                st.metric("🚀 틱톡 증가효과", "N/A")
                st.caption("Counterfactual 컬럼이 없어 계산 불가")

