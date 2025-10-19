import argparse, os, joblib, time
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import mlflow

# Stockage local MLflow
mlflow.set_tracking_uri("file:mlruns")
os.environ["MLFLOW_DISABLE_ENV_MANAGER"] = "1"


def build_preprocessor(df: pd.DataFrame):
    X = df.drop(columns=["Default", "LoanID"])
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
    pre = ColumnTransformer(
        [("num", StandardScaler(), num_cols),
         ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)]
    )
    return pre


def fit_and_log_once(experiment_name: str,
                     model_name: str,
                     model,
                     X_train, X_test, y_train, y_test,
                     pre,
                     seed: int):
    """
    Respecte la consigne :
    - un modèle => un experiment
    - un lancement => un run
    On logge uniquement les métriques (+ seed & params essentiels).
    """
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=f"{model_name}_seed{seed}"):
        pipe = Pipeline([("pre", pre), ("clf", model)])
        pipe.fit(X_train, y_train)

        y_pred = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") else None

        acc = accuracy_score(y_test, y_pred)
        f1  = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba) if y_proba is not None else float("nan")

        # Trace minimale mais utile
        mlflow.log_param("model", model_name)
        mlflow.log_param("seed", seed)
        if model_name == "logreg":
            mlflow.log_param("C", model.C)
            mlflow.log_param("solver", model.solver)
        elif model_name == "decision_tree":
            mlflow.log_param("max_depth", model.max_depth)
        elif model_name == "random_forest":
            mlflow.log_param("n_estimators", model.n_estimators)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("roc_auc", auc)

        return pipe, {"accuracy": acc, "f1": f1, "roc_auc": auc}


def main(data_path: str, seed_arg: str | int):
    os.makedirs("artifacts", exist_ok=True)

    # 1) Seed: auto -> timestamp, sinon conversion int
    if seed_arg == "auto":
        seed = int(time.time() % (2**31 - 1))
    else:
        seed = int(seed_arg)

    # 2) Data
    df = pd.read_csv(data_path)
    y  = df["Default"]
    X  = df.drop(columns=["Default", "LoanID"])

    pre = build_preprocessor(df)

    # 3) Split avec seed variable pour obtenir des métriques différentes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y, shuffle=True
    )

    results = []

    # 4) Modèles avec seed
    # LogisticRegression: pour que la seed ait un effet, on choisit un solver qui l'utilise (liblinear)
    logreg = LogisticRegression(max_iter=300, class_weight="balanced", C=1.0,
                                solver="liblinear", random_state=seed)
    clf_lr, met_lr = fit_and_log_once("logreg", "logreg", logreg,
                                      X_train, X_test, y_train, y_test, pre, seed)
    results.append(("logreg", clf_lr, met_lr))

    tree = DecisionTreeClassifier(class_weight="balanced", random_state=seed, max_depth=5)
    clf_dt, met_dt = fit_and_log_once("decision_tree", "decision_tree", tree,
                                      X_train, X_test, y_train, y_test, pre, seed)
    results.append(("decision_tree", clf_dt, met_dt))

    rf = RandomForestClassifier(class_weight="balanced", random_state=seed, n_estimators=100)
    clf_rf, met_rf = fit_and_log_once("random_forest", "random_forest", rf,
                                      X_train, X_test, y_train, y_test, pre, seed)
    results.append(("random_forest", clf_rf, met_rf))

    # 5) Sauvegarde du meilleur modèle (AUC puis F1)
    best = sorted(results, key=lambda t: (np.nan_to_num(t[2]["roc_auc"]), t[2]["f1"]), reverse=True)[0]
    joblib.dump(best[1], "artifacts/best_model.joblib")

    print("\n✅ Entraînement terminé.")
    print("→ Seed utilisée     :", seed)
    print("→ Meilleur modèle   :", best[0])
    print("→ Metrics           :", best[2])
    print("→ Modèle sauvegardé : artifacts/best_model.joblib")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="data/loans.csv")
    parser.add_argument("--seed", type=str, default="auto",
                        help="Entier pour reproductibilité, ou 'auto' pour varier à chaque run.")
    args = parser.parse_args()
    main(args.data, args.seed)
