import numpy as np
from sklearn.linear_model import LinearRegression
def train(values):
    y = np.asarray(values, dtype=float)
    return LinearRegression().fit(np.arange(len(y)).reshape(-1,1), y)
