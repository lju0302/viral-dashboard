import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


base_dir = Path(__file__).resolve().parents[2]
EXPECTED_COLS = joblib.load(base_dir / "src" / "model_feature_columns.joblib")


## 예시 데이터와 컬럼 설정
data = [ 
    ["Drama", 87, 64, 38, 16, 0, 36, 4, -2, "big3", 4, 2023, 1], 
    ["Bubble", 77, 77, 72, 3, 0, 7, 6, -3, "mid", 4, 2023, 1], 
    ["뛰어(Jump!)", 93, 71, 52, 0, 0, 10, 7, -6, 'big3', 10, 2025, 1],
    ["Spaghetti", 82, 90, 87, 8, 0, 29, 7, -5, 'big3', 4, 2025, 1]

    ]
cols = ["title","energy","danceability","happiness","acousticness", "instrumentalness","liveness","speechiness","loudness", "class","career_years","release_year","existence"]

st.set_page_config(page_title="Prediction", layout="wide")

st.title("🔮 Prediction")
st.caption("사후 데이터 기반 강조 / 메타데이터로 사전 예측 / 분류 결과 / 입력 폼 + XGBoost")

# 1) 포지셔닝(사후 → 사전 예측)
st.header("1) 포지셔닝: 사후 결과 기반 → 사전 예측")
with st.container(border=True):
    # st.write("앞선 Typology/Counterfactual이 사후 데이터 기반임을 강조하는 설명 영역")
    # st.write("사전 예측을 위해 메타데이터 활용했다는 설명 영역")
    st.write(" ")
    st.write(
        "앞선 반사실 추정과 바이럴 유형 분류는 **곡이 발매된 이후**, "
        "**충분한 관측 기간**이 지난 뒤에야 평가할 수 있는 분석입니다."
    )

    st.write(
        "이에 본 연구는 이러한 바이럴 유형을 "
        "**곡 발매 이전 단계**에서도 사전에 예측할 수 있을지에 주목하였습니다."
    )

    st.write(
        "**곡이 발매되기 전에도 확인 가능**한 메타데이터만을 활용하여, "
        "해당 곡이 향후 **'이상적 바이럴'** 유형에 속할 가능성을 "
        "**사전에 분류**하는 예측 모델을 구축하였습니다."
    )
    st.write(" ")

# 2) 분류 모델 개요와 정확도, 피쳐 임포턴스
st.header("2) 분류 모델 설명")
with st.container(border=True):
    left, right = st.columns([1.2 , 0.8])
    with left:
        st.subheader("피쳐 중요도", help = "'이상적 바이럴' 분류에 어떤 변수가 중요하게 작용했는지를 보여줍니다.")
        fi_df = pd.read_csv("./src/xgb_feature_importance.csv")
        fi_df = fi_df.drop(columns = 'Unnamed: 0')
        # fi_df = fi_df.sort_values(by = 'importance)
        # 추가 컬럼 : 피쳐 설명 <- 피쳐 임포턴스 다시 집어넣은 후에 다시 쓰기
        descr = ['뮤직비디오 존재 여부', '소속사 분류 : 대형', '소속사 분류 : 중형', '발매연도', '활동 연차', '해당 트랙에 보컬이 포함되어 있지 않을 가능성 정도', '소속사 분류 : 소형', '해당 트랙이 춤추기에 얼마나 적합한지를 나타내는 지표', '해당 트랙의 분위기가 얼마나 행복한지를 나타내는 지표', '볼륨 레벨', '전자 장비를 사용하지 않은, 자연 그대로의 소리를 내는 정도', '해당 트랙의 분위기기 얼마나 에너제틱한지 나타내는 지표', '보컬 트랙이 얼마나 노래보다는 말이나 랩에 가까운지를 측정하는 지표',  '해당 트랙이 라이브음원 같은지를 나타내는 지표']
        fi_df['피쳐 설명'] = descr
        st.dataframe(data = fi_df)
        
    with right:
        st.subheader("결과 지표")
        st.metric("ROC-AUC Score", "0.83", help = "")
        st.metric("Accuracy Score", "0.80", help = "")

st.divider()

# 모델 탑재
import streamlit as st
from pathlib import Path
import joblib

@st.cache_resource
def load_model():
    base_dir = Path(__file__).resolve().parents[2]
    model_path = base_dir / "src" / "xgb_model.joblib"
    return joblib.load(model_path)

xgb_model = load_model()

#st.success("XGBoost model loaded successfully")
#st.write(xgb_model)




# 3) 예측 입력 공간 (XGBoost 탑재 예정)
st.header("3) 사전 예측 입력")
# st.write("차후 메타데이터 자동 연결 예정")

with st.container(border=True):
    form_col, out_col = st.columns([1, 1], gap="large")

    with form_col:
        st.subheader("입력 (Model Features)")

        # (선택) 샘플 선택해서 자동 채우기
        sample_titles = [row[0] for row in data]
        selected_sample = st.selectbox("샘플 불러오기(선택)", ["직접 입력"] + sample_titles)

        # 기본값
        defaults = {
            "title": "",
            "energy": 70,
            "danceability": 70,
            "happiness": 70,
            "acousticness": 20,
            "instrumentalness": 0,
            "liveness": 20,
            "speechiness": 5,
            "loudness": -6,
            "class": "mid",
            "career_years": 2,
            "release_year": 2023,
            "existence": 1,
        }

        # 샘플 선택 시 defaults 덮어쓰기
        if selected_sample != "직접 입력":
            idx = sample_titles.index(selected_sample)
            row = data[idx]
            defaults = dict(zip(cols, row))

        with st.form("predict_form", border=False):
            title = st.text_input("title", value=str(defaults["title"]), placeholder="예: Bubble")

            c1, c2 = st.columns(2)
            with c1:
                energy = st.number_input("energy (0~100)", min_value=0, max_value=100, value=int(defaults["energy"]))
                danceability = st.number_input("danceability (0~100)", min_value=0, max_value=100, value=int(defaults["danceability"]))
                happiness = st.number_input("happiness (0~100)", min_value=0, max_value=100, value=int(defaults["happiness"]))
                acousticness = st.number_input("acousticness (0~100)", min_value=0, max_value=100, value=int(defaults["acousticness"]))
                release_year = st.number_input("release_year", min_value=1990, max_value=2035, value=int(defaults["release_year"]))                
            with c2:
                liveness = st.number_input("liveness (0~100)", min_value=0, max_value=100, value=int(defaults["liveness"]))
                speechiness = st.number_input("speechiness (0~100)", min_value=0, max_value=100, value=int(defaults["speechiness"]))
                loudness = st.number_input("loudness (예: -12 ~ 0)", min_value=-60, max_value=10, value=int(defaults["loudness"]))
                instrumentalness = st.number_input("instrumentalness (0~100)", min_value=0, max_value=100, value=int(defaults["instrumentalness"]))
                career_years = st.number_input("career_years", min_value=0, max_value=60, value=int(defaults["career_years"]))

            # 범주/이진 변수
            company_class = st.selectbox(
                "class (company size)",
                options=["big3", "mid", "small"],
                index=["big3", "mid", "small"].index(str(defaults["class"])) if str(defaults["class"]) in ["big3","mid","small"] else 2,
                help = "기획사 규모 분류"
            )

            existence = st.checkbox(
                "existence (binary)",
                value=bool(int(defaults["existence"])),
                help="공식 뮤직비디오 존재 여부"
            )

            submitted = st.form_submit_button("예측 실행")

    with out_col:
        st.subheader("예측 결과")

        # 제출되면 입력을 df로 만들기 (모델 연결 전에도 확인 가능)
        if submitted:
            input_row = {
                "title": title,
                "energy": int(energy),
                "danceability": int(danceability),
                "happiness": int(happiness),
                "acousticness": int(acousticness),
                "instrumentalness": int(instrumentalness),
                "liveness": int(liveness),
                "speechiness": int(speechiness),
                "loudness": float(loudness),
                "class": company_class,
                "career_years": int(career_years),
                "release_year": int(release_year),
                "existence": int(existence),
            }

            class_map = {
                            "small": 0.0,
                            "mid": 1.0,
                            "big3": 2.0,
                        }
            
            input_row["class"] = float(class_map[company_class])  # <- 여기서 class 먼저 처리

            class_code = class_map.get(company_class)

            if class_code is None:
                class_code = 0
        
            

            st.success("입력값이 준비됐음!")
            st.write("Model input (single-row):")
            st.dataframe(pd.DataFrame([input_row]), use_container_width=True, hide_index=True)

            # st.info("여기에 사분면 확률/클래스 결과/설명(importance) 출력 영역")

            import numpy as np

            # 1) dict -> DF
            df = pd.DataFrame([input_row]).drop(columns=["title"], errors="ignore")

            # 2) 학습과 동일하게 원-핫 (drop_first=True)
            df = pd.get_dummies(df, columns=["class"], drop_first=True)

            # 3) 학습 컬럼/순서로 강제 맞춤 (이게 핵심)
            df = df.reindex(columns=EXPECTED_COLS, fill_value=0)

            X = df.values

            try:
                # 1) 예측 라벨
                y_pred = xgb_model.predict(X)[0]

                # 2) 확률(가능한 경우만)
                proba = None
                if hasattr(xgb_model, "predict_proba"):
                    proba = xgb_model.predict_proba(X)[0]

                st.success("✅ 모델 예측 완료")
                st.write("Predicted class:", y_pred)

                if proba is not None:
                    st.metric("이상적 바이럴 가능성", f"{proba[1]*100:.1f}%", help = "50% 이상이면 이상적 바이럴로 판단합니다.")
                    st.write("Probabilities:")
                    st.dataframe(
                        pd.DataFrame([proba]),
                        use_container_width=True,
                        hide_index=True
                    )


            except Exception as e:
                st.error("❌ 예측 실패 (모델 로딩/피처 불일치/전처리 문제 가능)")
                st.code(str(e))

        else:
            st.caption("왼쪽에서 값을 입력하고 '예측 실행'을 누르면 입력 행이 생성됨.")


# st.caption("※ 실제 XGBoost 모델 탑재 시 위 입력값과 모델 피처 매핑만 연결하면 됨.")
