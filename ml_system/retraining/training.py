from datetime import datetime
import numpy as np
import pandas as pd
import joblib
import json
import os
from sklearn.base import clone

def preprocess_data(X_train, X_val, y_train, model_v):
    BASE_DIR = get_base_dir()

    MODEL_PATH = os.path.join(BASE_DIR, "model", "model_v1.pkl")
    PREPROCESSOR_PATH = os.path.join(BASE_DIR, "model", "preprocessor.pkl")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    if not os.path.exists(PREPROCESSOR_PATH):
        raise FileNotFoundError(f"Preprocessor not found at {PREPROCESSOR_PATH}")

    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    
    X_train_processed= preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_val)
    model.fit(X_train_processed, y_train)
    
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'num_support_tickets']
    cat_cols = ['PaymentMethod', 'InternetService', 'Contract']
    
    training_stats = {}

    for col in num_cols:
        training_stats[col] = {
            "mean": float(X_train[col].mean()),
            "std": float(X_train[col].std()),
            "min": float(X_train[col].min()),
            "max": float(X_train[col].max()),
            "p25": float(X_train[col].quantile(0.25)),
            "p50": float(X_train[col].quantile(0.50)),
            "p75": float(X_train[col].quantile(0.75))
        }
    training_stats[col] = {
        k: float(v)
        for k, v in X_train[col].value_counts(normalize=True).items()
    }
    model_version = "v" + str(model_v)
    prev_version = model_v
    save_name = "training_stats" + "_" + model_version + ".json"
    with open(f"{save_name}", "w") as f:
        json.dump(training_stats, f, indent=4)
        
    
    message = "trained successfully!"
    return message
  
def get_base_dir():
    """
    Finds project root by locating the 'model' directory.
    """
    current = os.getcwd()

    while True:
        if os.path.isdir(os.path.join(current, "model")):
            return current

        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Could not find project root containing 'model/'")
        current = parent
        
        
def full_data_generator(df_train, df_val):
    df = pd.read_csv("C:/Users/Sahil.s.Vernekar/OneDrive/Documents/ML/Churn/Dataset/train.csv")
    df["num_support_tickets"] = np.random.poisson(lam=1.2, size=len(df))
    custom_map ={
        'yes' : 1,
        'no' : 0
    }
    df['churn'] = df['Churn'].apply(lambda x:1 if x=='Yes' else 0)
    df.drop(columns =['Churn'], inplace = True)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    cols_to_drop = [cols for cols in df.columns if cols not in ['tenure', 'MonthlyCharges', 'TotalCharges', 'PaymentMethod', 'InternetService', 'Contract', 'num_support_tickets', 'churn']]
    df.drop(columns= cols_to_drop, inplace= True)
    full_data = pd.concat([df, df_train, df_val], axis=0)
    return full_data
  
  
def retrain_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    base_model_path: str,
    preprocessor_path: str,
    new_model_path: str
):
    base_model = joblib.load(base_model_path)
    preprocessor = joblib.load(preprocessor_path)

    model = clone(base_model)

    X_train_processed = preprocessor.transform(X_train)
    model.fit(X_train_processed, y_train)

    joblib.dump(model, new_model_path)

    return {
        "trained_at": datetime.utcnow().isoformat(),
        "samples_used": len(X_train)
    }
    
def generate_training_stats(df: pd.DataFrame) -> dict:
    stats = {
        "samples": len(df),
        "label_distribution": df["churn"].value_counts(normalize=True).to_dict()
    }

    for col in df.columns:
        if col != "churn" and df[col].dtype != "object":
            stats[col] = {
                "mean": float(df[col].mean()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max())
            }

    return stats
