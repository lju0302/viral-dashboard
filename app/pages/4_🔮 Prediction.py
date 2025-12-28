import streamlit as st

st.set_page_config(page_title="Prediction", layout="wide")

st.title("🔮 Prediction")
st.caption("사후 데이터 기반 강조 / 메타데이터로 사전 예측 / 분류 결과 / 입력 폼 + XGBoost")

# 1) 포지셔닝(사후 → 사전 예측)
st.header("1) 포지셔닝: 사후 결과 기반 → 사전 예측")
with st.container(border=True):
    st.write("앞선 Typology/Counterfactual이 사후 데이터 기반임을 강조하는 설명 영역")
    st.write("사전 예측을 위해 메타데이터 활용했다는 설명 영역")

st.divider()

# 2) 실제 분류 결과(포스터와 동일)
st.header("2) 분류 결과 (Poster와 동일)")
with st.container(border=True):
    left, right = st.columns([1.2, 0.8])
    with left:
        st.subheader("결과 시각화")
        st.info("포스터와 동일한 confusion matrix / ROC / 분포 등 배치 영역")
    with right:
        st.subheader("요약 지표")
        st.metric("Accuracy", "—")
        st.metric("Macro F1", "—")
        st.metric("Q1 Recall", "—")

st.divider()

# 3) 예측 입력 공간 (XGBoost 탑재 예정)
st.header("3) 사전 예측 입력")
with st.container(border=True):
    form_col, out_col = st.columns([1, 1])
    with form_col:
        st.subheader("입력 (Metadata)")
        with st.form("predict_form", border=False):
            st.text_input("곡명", placeholder="예: Bubble")
            st.text_input("아티스트", placeholder="예: STAYC")
            st.number_input("Danceability", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
            st.number_input("Energy", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
            st.number_input("Speechiness", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
            submitted = st.form_submit_button("예측 실행")
    with out_col:
        st.subheader("예측 결과")
        if "submitted_dummy" not in st.session_state:
            st.session_state.submitted_dummy = False
        st.info("여기에 사분면 확률/클래스 결과/설명(importance) 출력 영역")

st.caption("※ 실제 XGBoost 모델 탑재 시 위 입력값과 모델 피처 매핑만 연결하면 됨.")
