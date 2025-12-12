import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("2️⃣ 반사실(Counterfactual)")

song_id = st.session_state.get("selected_song", None)

x = np.arange(30)
actual = np.cumsum(np.random.normal(1.2, 0.3, 30))
cf = np.cumsum(np.random.normal(0.5, 0.2, 30))

fig, ax = plt.subplots()
ax.plot(x, actual, label="Actual")
ax.plot(x, cf, label="Counterfactual (TikTok=0)")
ax.legend()

st.pyplot(fig)

if song_id:
    st.info(f"현재 선택된 곡 ID: {song_id}")
