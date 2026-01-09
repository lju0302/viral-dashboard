import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Viral Typology", layout="wide")

st.title("🧭 Viral Typology")
st.caption("retention/reactivity 소개 / 4유형 / 스캐터플롯")


@st.cache_data
def load_viral_index():
    base_dir = Path(__file__).resolve().parents[2]
        # parents[0] = pages
        # parents[1] = app
        # parents[2] = viral-dashboard (root)
    data_path = base_dir / "src" / "viral_index.csv"
    return pd.read_csv(data_path)

df = load_viral_index()

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

import plotly.express as px

st.header("3) 실제 데이터 포인트 확인 (Interactive Scatter)")

with st.container(border=True):
    left, right = st.columns([1.2, 0.8])

    with left:
        st.subheader("Scatter Plot")

        fig = px.scatter(
            df,
            x="retention",
            y="beta",                     # 실제 컬럼은 beta
            hover_data=["song_id"],
            labels={
                "retention": "Retention",
                "beta": "Reactivity"      # 👈 표시 이름만 변경
            },
            title="Viral Typology Scatter Plot"
        )

        # ✅ 기준선 추가
        fig.add_vline(
            x=1.0,
            line_width=2,
            line_dash="dot",
            line_color="light blue"
        )
        fig.add_hline(
            y=0.0,
            line_width=2,
            line_dash="dot",
            line_color="light blue"
        )

        # ✅ 정사각형 비율 유지 (핵심)
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1
        )

        # (선택) 축 범위 자동 + 여백 최소화
        fig.update_layout(
            margin=dict(l=30, r=30, t=30, b=30),
            legend_title_text="",
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("필터")
        st.selectbox("클러스터", ["전체", "C0", "C1", "C2"])
        st.selectbox("사분면", ["전체", "Q1", "Q2", "Q3", "Q4"])
        st.slider("peak_tiktok 범위", 0, 100, (10, 80))
        st.checkbox("기준선 표시", value=True)

with st.expander("선택 포인트 상세", expanded=False):
    st.info("포인트 클릭/선택 시 상세 정보 패널 영역")
