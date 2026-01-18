
import joblib
import pandas as pd
from datetime import datetime
from ml_logging.prediction_logger import log_prediction


def load_artifacts(model_path: str, preprocessor_path: str):
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    return model, preprocessor


def predict(
    input_features: dict,
    model_version: str,
    model_path: str,
    preprocessor_path: str
) -> float:

    model, preprocessor = load_artifacts(model_path, preprocessor_path)

    X = pd.DataFrame([input_features])
    X_processed = preprocessor.transform(X)

    y_pred = model.predict(X_processed)[0]

    # If classifier supports probability, log it
    proba = None
    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(X_processed)[0][1])

    log_prediction(
        model_version=model_version,
        features=input_features,
        prediction=float(y_pred),
        prediction_percentage=proba
    )

    return float(y_pred), float(proba), model_version
