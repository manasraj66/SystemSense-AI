import numpy as np
from sklearn.tree import DecisionTreeRegressor
def train(values):
    y = np.asarray(values, dtype=float)
    return DecisionTreeRegressor(max_depth=5, random_state=42).fit(np.arange(len(y)).reshape(-1,1), y)
