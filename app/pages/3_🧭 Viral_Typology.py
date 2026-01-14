import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Viral Typology", layout="wide")

st.title("🧭 Viral Typology")
st.caption("retention/reactivity 소개 / 4유형 / 스캐터플롯")

with st.container(border=True):
    st.markdown("### 왜 바이럴 유형학(Viral Typology)이 필요한가?")

    st.markdown("""
숏폼 바이럴은 단순히 “떴다 / 안 떴다"로 끝나지 않습니다.  
같은 바이럴이라도 스트리밍 성과의 전개는 크게 달라집니다.

- **반응은 큰데 금방 꺼지는 바이럴** (단기 버스트)
- **반응은 느리지만 오래 가는 바이럴** (지속형)
- **반응도 지속도 거의 없는 경우** (무반응)
        """)

st.divider()

# 1) retention / reactivity 개념
st.header("1) 바이럴의 두 축 : Retention & Reactivity")
a, b = st.columns(2, gap="large")

with a:
        st.markdown("#### ⚡ Reactivity (반응성)")
        st.markdown("""
바이럴 발생 직후, 스트리밍/관심이 **얼마나 빠르고 크게 반응하는가**를 나타냅니다.  
- 빠른 확산, 급격한 증가가 특징  
- 단기 버스트형 바이럴을 포착하는 데 유리
        """)
        st.caption("예: 챌린지/밈 확산으로 며칠 내 급등")

        detail_rea = st.checkbox("반응성 추가 설명 보기", value=False)
        if detail_rea:
            st.markdown("""
- **정의**: 틱톡 노출이 1단위 증가할 때 스트리밍이 몇 단위 증가하는가 (회귀계수 β)
- **해석**: β가 클수록 틱톡 노출에 민감하게 반응하여 스트리밍이 급증
- **측정 방법**: K-SARIMAX 모델의 외생변수(틱톡 노출) 회귀계수 활용
            """)

with b:
    st.markdown("#### 🕒 Retention (지속성)")
    st.markdown("""
바이럴 반응이 **얼마나 오래 유지되는가**를 나타냅니다.  
- 반복 소비, 플레이리스트 정착, 장기 성장과 연결  
- ‘지속 가능한 바이럴’ 여부 판단에 유리
    """)
    st.caption("예: 초반 급등은 약해도 장기 우상향")

    detail_ret = st.checkbox("지속성 추가 설명 보기", value=False)
    if detail_ret:
        st.markdown("""
- **정의**: 바이럴 종료 후 스트리밍 수준이 바이럴 이전 대비 몇 배로 유지되는가 (지속 비율)
- **해석**: 1보다 클수록 바이럴 종료 후에도 스트리밍이 이전 수준보다 높게 유지 
- **측정 방법**: K-SARIMAX 모델의 바이럴 종료 전후 예측치 비교 """)
st.divider()

@st.cache_data
def load_viral_index():
    base_dir = Path(__file__).resolve().parents[2]
        # parents[0] = pages
        # parents[1] = app
        # parents[2] = viral-dashboard (root)
    data_path = base_dir / "src" / "viral_index.csv"
    return pd.read_csv(data_path)

df = load_viral_index()


# 2) 4유형 소개
st.header("2) 바이럴 4유형 소개")
st.caption("Retention과 Reactivity의 조합에 따른 4가지 유형 - 3)의 그래프 실제 위치와 대응됩니다")
with st.container(border=True):
    q_c1, q_c2 = st.columns(2)
    with q_c1:
        with st.container(border=True):
            st.markdown("#### **Q2** : 반짝형 (🧨)")
            st.caption("지속력은 낮지만 반응성은 높은 유형으로, 빠른 확산 후 급격한 하락이 특징인 콘텐츠입니다.")
            st.markdown("**Q2의 특징**")
            st.write("틱톡에서의 높은 노출이 즉각적인 스트리밍 상승으로 이어지지만, 바이럴이 종료된 이후에는 급격한 하락세를 보입니다. 이러한 유형은 주로 챌린지나 밈과 같은 단기적인 유행에 의해 촉발되며, 지속적인 음원 소비로 이어지지 못하는 경우가 많습니다.")
        with st.container(border=True):
            st.markdown("#### **Q3 : 무반응형 (😵)**")
            st.caption("반응성과 지속성이 모두 낮은 유형으로, 바이럴이 발생했지만 효과가 거의 없는 콘텐츠입니다.")
            st.markdown("**Q3의 특징**")
            st.write("틱톡에서의 노출이 스트리밍 증가로 이어지지 않으며, 바이럴이 종료된 이후에도 스트리밍 수준이 크게 변하지 않는 유형입니다. 이는 주로 틱톡 내에서의 노출이 충분하지 않거나, 노출된 콘텐츠가 청취자들의 관심을 끌지 못하는 경우에 발생합니다.")
    with q_c2:
        with st.container(border=True):
            st.markdown("#### **Q1** : 이상적 바이럴 (⭐️)")
            st.caption("반응성과 지속성 모두 높은 유형으로, 높은 확산과 지속적인 인기를 누리는 콘텐츠입니다.")
            st.markdown("**Q1의 특징**")
            st.write("틱톡에서의 노출이 즉각적인 스트리밍 상승으로 이어질 뿐만 아니라, 바이럴이 종료된 이후에도 높은 스트리밍 수준이 지속되는 가장 성공적인 형태입니다. 단순한 유행을 넘어 실제 음원 소비층의 확장과 장기적인 흥행으로 전이된 사례입니다.")
        with st.container(border=True):
            st.markdown("#### **Q4** : 팬덤형 (🌱)")
            st.caption("반응성은 상대적으로 낮지만, 고정 소비층에 의해 지속적인 스트리밍이 유지되는 유형입니다.")
            st.markdown("**Q4의 특징**")
            st.write("틱톡에서의 노출이 스트리밍 증가로 이어지긴 하지만, 그 반응 속도는 다소 느린 편입니다. 그러나 바이럴이 종료된 이후에도 일정 수준의 스트리밍이 지속되며, 이는 주로 충성도 높은 팬덤에 의해 뒷받침됩니다. 이러한 유형은 특정 아티스트나 장르에 대한 고정 팬층이 존재하는 경우에 나타납니다.")
            

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
