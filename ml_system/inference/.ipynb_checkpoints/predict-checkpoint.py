# inference/predict.py
import sys
import os

sys.path.append(os.path.abspath(".."))


import joblib
import datetime
from ml_logging.prediction_logger import log_prediction

MODEL_VERSION = "v1"

model = joblib.load("model/model_v1.pkl")
preprocessor = joblib.load("model/preprocessor.pkl")

def predict(input_features: dict):
    """
    input_features: raw input (same schema as training)
    """

    # 1. Convert to DataFrame
    import pandas as pd
    X = pd.DataFrame([input_features])

    # 2. Apply preprocessing
    X_transformed = preprocessor.transform(X)

    # 3. Predict
    y_pred = model.predict(X_transformed)[0]

    # 4. Log prediction (non-negotiable)
    log_prediction(
        model_version=MODEL_VERSION,
        features=input_features,
        prediction=float(y_pred)
    )

    return float(y_pred)
