import pandas as pd, joblib
from sklearn.metrics import classification_report
model = joblib.load('artifacts/best_model.joblib')
df = pd.read_csv('data/loans.csv')
X = df.drop(columns=['Default','LoanID'])
y = df['Default']
pred = model.predict(X)
print(classification_report(y, pred))
