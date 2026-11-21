from sklearn.ensemble import IsolationForest
from app.ml.preprocessing import clean_features
def train(rows):
    return IsolationForest(n_estimators=150, contamination=0.05, random_state=42).fit(clean_features(rows))
