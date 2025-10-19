import streamlit as st
import pandas as pd
import joblib
import os, json

# --- Configuration des chemins ---
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/best_model.joblib")
THRESHOLD_PATH = "artifacts/threshold.json"
DEFAULT_THRESHOLD = 0.5

# --- Chargement du modèle ---
model = joblib.load(MODEL_PATH)

thr = DEFAULT_THRESHOLD
if os.path.exists(THRESHOLD_PATH):
    try:
        with open(THRESHOLD_PATH, "r") as f:
            thr = json.load(f).get("threshold", DEFAULT_THRESHOLD)
    except Exception:
        thr = DEFAULT_THRESHOLD

# --- Options des listes déroulantes ---
OPTIONS = {
    "Education": ["High School", "Bachelor's", "Master's", "PhD", "Other"],
    "EmploymentType": ["Full-time", "Part-time", "Self-employed", "Unemployed", "Contractor", "Other"],
    "MaritalStatus": ["Single", "Married", "Divorced", "Widowed", "Other"],
    "HasMortgage": ["No", "Yes"],
    "HasDependents": ["No", "Yes"],
    "LoanPurpose": ["Personal", "Home", "Auto", "Business", "Education", "Other"],
    "HasCoSigner": ["No", "Yes"],
}

# --- Valeurs par défaut ---
DEFAULTS = {
    "Age": 35,
    "Income": 42000,
    "LoanAmount": 12000,
    "CreditScore": 680,
    "MonthsEmployed": 48,
    "NumCreditLines": 5,
    "InterestRate": 7.5,
    "LoanTerm": 36,
    "DTIRatio": 0.28,
    "Education": "Bachelor's",
    "EmploymentType": "Full-time",
    "MaritalStatus": "Single",
    "HasMortgage": "No",
    "HasDependents": "No",
    "LoanPurpose": "Personal",
    "HasCoSigner": "No",
}

st.set_page_config(page_title="Loan Default Prediction", page_icon="💰", layout="centered")

st.title("💰 Loan Default Prediction App")

st.markdown("Remplissez les informations ci-dessous pour prédire le risque de défaut de prêt :")

# --- Interface utilisateur ---
payload = {}
cols = st.columns(2)

# Champs numériques
for i, f in enumerate(["Age", "Income", "LoanAmount", "CreditScore", "MonthsEmployed", "NumCreditLines", "InterestRate", "LoanTerm", "DTIRatio"]):
    with cols[i % 2]:
        payload[f] = st.number_input(f, value=DEFAULTS[f])

# Champs catégoriels
for f in ["Education", "EmploymentType", "MaritalStatus", "HasMortgage", "HasDependents", "LoanPurpose", "HasCoSigner"]:
    payload[f] = st.selectbox(f, OPTIONS[f], index=OPTIONS[f].index(DEFAULTS[f]))

# --- Prédiction ---
if st.button("Prédire"):
    X = pd.DataFrame([payload])
    proba = float(model.predict_proba(X)[0, 1])
    pred = int(proba >= thr)

    st.markdown(f"### 🔍 Probabilité de défaut : **{proba:.3f}**")
    st.markdown(f"### 📈 Seuil : **{thr:.2f}**")
    st.markdown(f"### 🧾 Résultat : {'❌ Défaut probable' if pred==1 else '✅ Pas de défaut'}")

