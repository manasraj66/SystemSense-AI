import numpy as np
from sklearn.ensemble import RandomForestRegressor
def train(values):
    y = np.asarray(values, dtype=float)
    return RandomForestRegressor(n_estimators=150, random_state=42).fit(np.arange(len(y)).reshape(-1,1), y)
