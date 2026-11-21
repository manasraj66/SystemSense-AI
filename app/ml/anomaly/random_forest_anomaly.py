from sklearn.ensemble import RandomForestClassifier
from app.ml.preprocessing import clean_features
def train(rows):
    x = clean_features(rows)
    y = ((x[:,0] > 80) | (x[:,1] > 85) | (x[:,2] > 90)).astype(int)
    return RandomForestClassifier(n_estimators=120, random_state=42, class_weight="balanced").fit(x, y)
