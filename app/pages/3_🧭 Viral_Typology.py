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
