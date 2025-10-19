# Loan Default Prediction — MLOps (Flask + MLflow + AWS)

This project adapts your professor's Flask pattern to a **loan default prediction** problem.

## Quickstart (local)

```bash
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/train.py --data data/loans.csv --experiment-name "loan-default-baseline"
python app.py
```

Open: http://127.0.0.1:5000

## MLflow
Start MLflow UI (optional):
```bash
mlflow ui --port 5001
```
The training script logs metrics: **accuracy**, **f1**, **roc_auc**.

## Docker
```bash
docker build -t loan-default-app .
docker run -p 5000:5000 loan-default-app
```

## AWS (ECS + ECR via GitHub Actions)
- Create an **ECR** repo and an **ECS** cluster/service.
- Add GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.
- Edit `.github/workflows/aws.yml` environment names to yours.
- Push to `main` to trigger deployment.
```

