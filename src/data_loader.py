import numpy as np
import pandas as pd

def make_dummy_data():
    np.random.seed(42)
    n = 50

    df = pd.DataFrame({
        "song_id": range(1000, 1000+n),
        "growth": np.random.normal(0.05, 0.02, n),
        "retention": np.random.uniform(0, 1, n),
        "reactivity": np.random.uniform(0, 1, n),
        "xgb_prob": np.random.uniform(0, 1, n)
    })
    return df
