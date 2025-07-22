from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load('model/churn_model.pkl')

expected_columns = [
    'SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
    'gender_Female', 'gender_Male', 'Partner_No', 'Partner_Yes',
    'Dependents_No', 'Dependents_Yes', 'PhoneService_No', 'PhoneService_Yes',
    'MultipleLines_No', 'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_DSL', 'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No', 'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No', 'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No', 'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No', 'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No', 'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No', 'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_Month-to-month', 'Contract_One year', 'Contract_Two year',
    'PaperlessBilling_No', 'PaperlessBilling_Yes',
    'PaymentMethod_Bank transfer (automatic)', 'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check'
]

class EncodedInput(BaseModel):
    features: list[float]

app = FastAPI()

@app.post("/predict")
def predict(data: EncodedInput):

    print(data)

    input_array = np.array([data.features])

    print(input_array.shape, "shape")

    if input_array.shape[1] != len(expected_columns):
        return {"error": f"Expected {len(expected_columns)} features, got {input_array.shape[1]}"}

    pred = model.predict(input_array)[0]
    prob = model.predict_proba(input_array)[0][1]

    return {
        "churn_prediction": int(pred),
        "churn_probability": round(float(prob), 4)
    }