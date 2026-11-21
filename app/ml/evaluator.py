import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
def regression_metrics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    return {"mae": float(mean_absolute_error(y_true, y_pred)), "mse": float(mse),
            "rmse": float(np.sqrt(mse)), "r2": float(r2_score(y_true, y_pred))}
def classification_metrics(y_true, y_pred):
    from sklearn.metrics import precision_score, recall_score, f1_score
    return {"precision": float(precision_score(y_true,y_pred,zero_division=0)),
            "recall": float(recall_score(y_true,y_pred,zero_division=0)),
            "f1": float(f1_score(y_true,y_pred,zero_division=0))}
