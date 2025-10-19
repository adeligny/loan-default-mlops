from flask import Flask, render_template, request
import joblib
import pandas as pd
import os, json

MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/best_model.joblib")
THRESHOLD_PATH = "artifacts/threshold.json"
DEFAULT_THRESHOLD = 0.5

# Options des listes déroulantes
OPTIONS = {
    "Education": ["High School", "Bachelor's", "Master's", "PhD", "Other"],
    "EmploymentType": ["Full-time", "Part-time", "Self-employed", "Unemployed", "Contractor", "Other"],
    "MaritalStatus": ["Single", "Married", "Divorced", "Widowed", "Other"],
    "HasMortgage": ["No", "Yes"],
    "HasDependents": ["No", "Yes"],
    "LoanPurpose": ["Personal", "Home", "Auto", "Business", "Education", "Other"],
    "HasCoSigner": ["No", "Yes"],
}

# Valeurs par défaut
DEFAULTS = {
    "Age": 35,
    "Income": 42000,
    "LoanAmount": 12000,
    "CreditScore": 680,
    "MonthsEmployed": 48,
    "NumCreditLines": 5,
    "InterestRate": 7.5,
    "LoanTerm": 36,
    "DTIRatio": 0.28,  # ratio entre 0 et 1
    "Education": "Bachelor's",
    "EmploymentType": "Full-time",
    "MaritalStatus": "Single",
    "HasMortgage": "No",
    "HasDependents": "No",
    "LoanPurpose": "Personal",
    "HasCoSigner": "No",
}

FEATURES = [
    'Age','Income','LoanAmount','CreditScore','MonthsEmployed','NumCreditLines',
    'InterestRate','LoanTerm','DTIRatio','Education','EmploymentType','MaritalStatus',
    'HasMortgage','HasDependents','LoanPurpose','HasCoSigner'
]

app = Flask(__name__)
model = joblib.load(MODEL_PATH)

# Charge le seuil s’il existe
thr = DEFAULT_THRESHOLD
if os.path.exists(THRESHOLD_PATH):
    try:
        with open(THRESHOLD_PATH, "r") as f:
            thr = json.load(f).get("threshold", DEFAULT_THRESHOLD)
    except Exception:
        thr = DEFAULT_THRESHOLD


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", options=OPTIONS, defaults=DEFAULTS, threshold=thr)


@app.route("/predict", methods=["POST"])
def predict():
    payload = {}

    for f in FEATURES:
        val = request.form.get(f, DEFAULTS.get(f))

        if f in OPTIONS:  # variables catégorielles
            if val not in OPTIONS[f]:
                val = OPTIONS[f][0]
            payload[f] = val
        else:
            # variables numériques
            try:
                if isinstance(val, str):
                    val = val.replace(",", ".")  # accepte virgule ou point

                payload[f] = float(val)

                # cast entier pour certains champs
                if f in ["Age", "MonthsEmployed", "NumCreditLines", "LoanTerm"]:
                    payload[f] = int(round(payload[f]))

                # conversion pourcentage -> ratio
                if f == "DTIRatio" and payload[f] > 1:
                    payload[f] = payload[f] / 100.0

                # bornes raisonnables
                if f == "DTIRatio":
                    payload[f] = max(0.0, min(1.0, payload[f]))

            except Exception:
                payload[f] = DEFAULTS[f]

    X = pd.DataFrame([payload])
    proba = float(model.predict_proba(X)[0, 1])
    pred = int(proba >= thr)
    msg = f"Probabilité de défaut: {proba:.3f} — Seuil: {thr:.2f} — Prédiction: {'Défaut' if pred==1 else 'Pas de défaut'}"

    return render_template("index.html", options=OPTIONS, defaults=payload, threshold=thr, prediction_text=msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
