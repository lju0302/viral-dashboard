import streamlit as st

st.set_page_config(page_title="Viral Typology", layout="wide")

st.title("🧭 Viral Typology")
st.caption("retention/reactivity 소개 / 4유형 / 스캐터플롯")

# 1) 핵심 지표 소개
st.header("1) 핵심 지표 소개 (Retention, Reactivity)")
with st.container(border=True):
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Retention")
        st.write("정의/직관/단위 설명 영역")
    with right:
        st.subheader("Reactivity")
        st.write("정의/직관/단위 설명 영역")

st.divider()

# 2) 4유형 소개
st.header("2) 바이럴 4유형 소개")
with st.container(border=True):
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        with st.container(border=True):
            st.markdown("**Q1**")
            st.caption("설명 영역")
    with q2:
        with st.container(border=True):
            st.markdown("**Q2**")
            st.caption("설명 영역")
    with q3:
        with st.container(border=True):
            st.markdown("**Q3**")
            st.caption("설명 영역")
    with q4:
        with st.container(border=True):
            st.markdown("**Q4**")
            st.caption("설명 영역")

st.divider()

# 3) 실제 데이터 포인트 확인 스캐터플롯
st.header("3) 실제 데이터 포인트 확인 (Interactive Scatter)")
with st.container(border=True):
    left, right = st.columns([1.2, 0.8])
    with left:
        st.subheader("Scatter Plot")
        st.info("retention(축) × reactivity(축) 인터랙티브 스캐터 영역")
    with right:
        st.subheader("필터")
        st.selectbox("클러스터", ["전체", "C0", "C1", "C2"])
        st.selectbox("사분면", ["전체", "Q1", "Q2", "Q3", "Q4"])
        st.slider("peak_tiktok 범위", 0, 100, (10, 80))
        st.checkbox("기준선 표시", value=True)

with st.expander("선택 포인트 상세", expanded=False):
    st.info("포인트 클릭/선택 시 상세 정보 패널 영역")




# streamlit_app/pages/3_viral_typology.py (예시)
# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.set_page_config(page_title="Viral Typology", layout="wide")

# @st.cache_data
# def load_data(path: str):
#     df = pd.read_csv(path)
#     # 불필요한 인덱스 컬럼 제거
#     df = df.drop(columns=[c for c in df.columns if c.lower().startswith("unnamed")], errors="ignore")
#     return df

# # ✅ 너 파일 경로에 맞게 수정
# DATA_PATH = "/Users/starboy/Desktop/data_analysis/Causal Inference/project/viral-dashboard/src/viral_index.csv"  # 또는 "./viral_index.csv"
# df = load_data(DATA_PATH)

# # --- 컬럼 매핑 (가정) ---
# # reactivity = beta, retention = retention
# df = df.rename(columns={"beta": "reactivity"})

# st.title("Retention × Reactivity (Viral Typology)")

# # --- Sidebar filters ---
# with st.sidebar:
#     st.header("Filters")

#     # peak_tiktok 로그/범위 필터
#     min_peak = float(df["peak_tiktok"].min())
#     max_peak = float(df["peak_tiktok"].max())
#     peak_range = st.slider("peak_tiktok range", min_value=min_peak, max_value=max_peak,
#                            value=(min_peak, max_peak))

#     # retention / reactivity 범위 필터
#     rmin, rmax = float(df["retention"].min()), float(df["retention"].max())
#     bmin, bmax = float(df["reactivity"].min()), float(df["reactivity"].max())

#     retention_range = st.slider("retention range", min_value=rmin, max_value=rmax, value=(rmin, rmax))
#     reactivity_range = st.slider("reactivity range", min_value=bmin, max_value=bmax, value=(bmin, bmax))

#     log_x = st.checkbox("log scale (reactivity)", value=False)
#     log_size = st.checkbox("size by peak_tiktok (log)", value=True)

#     # 사분면 기준 (너가 쓰던 기본값 가정)
#     st.subheader("Quadrant thresholds")
#     thr_retention = st.number_input("retention threshold", value=1.0, step=0.1)
#     thr_reactivity = st.number_input("reactivity threshold", value=0.0, step=0.1)

# # --- Apply filters ---
# dff = df[
#     (df["peak_tiktok"].between(*peak_range)) &
#     (df["retention"].between(*retention_range)) &
#     (df["reactivity"].between(*reactivity_range))
# ].copy()

# # --- Quadrant label ---
# def quadrant(row, r_thr, b_thr):
#     r, b = row["retention"], row["reactivity"]
#     if (r >= r_thr) and (b >= b_thr): return "Q1: High react, High retain"
#     if (r >= r_thr) and (b <  b_thr): return "Q2: Low react, High retain"
#     if (r <  r_thr) and (b <  b_thr): return "Q3: Low react, Low retain"
#     return "Q4: High react, Low retain"

# dff["quadrant"] = dff.apply(quadrant, axis=1, args=(thr_retention, thr_reactivity))

# # --- Plotly scatter ---
# size_col = "peak_tiktok"
# if log_size:
#     # size가 너무 튀는 것 방지용 (log1p)
#     dff["_size"] = (dff["peak_tiktok"]).clip(lower=0).apply(lambda x: __import__("math").log1p(x))
#     size_col = "_size"

# fig = px.scatter(
#     dff,
#     x="reactivity",
#     y="retention",
#     color="quadrant",
#     size=size_col,
#     hover_data={
#         "song_id": True,
#         "reactivity": ":.4f",
#         "retention": ":.4f",
#         "peak_tiktok": True,
#         "quadrant": True,
#     },
#     height=720,
# )

# # 기준선 (사분면)
# fig.add_vline(x=thr_reactivity, line_width=1)
# fig.add_hline(y=thr_retention, line_width=1)

# # 축 스케일
# if log_x:
#     fig.update_xaxes(type="log")

# fig.update_layout(
#     margin=dict(l=20, r=20, t=40, b=20),
#     legend_title_text="Quadrant",
# )

# st.plotly_chart(fig, use_container_width=True)

# st.caption(f"Rows: {len(dff):,} / {len(df):,}")
