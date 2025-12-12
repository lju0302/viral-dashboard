import streamlit as st
import matplotlib.pyplot as plt
from utils import make_dummy_data

df = make_dummy_data()

st.title("1️⃣ 이질성(Heterogeneity)")

st.markdown("""
같은 바이럴이라도 **곡마다 반응과 지속성이 다릅니다**.
""")

fig, ax = plt.subplots()
ax.scatter(df["reactivity"], df["retention"])
ax.set_xlabel("Reactivity")
ax.set_ylabel("Retention")

st.pyplot(fig)
