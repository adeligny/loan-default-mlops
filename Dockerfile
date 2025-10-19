# ============================================================
# Dockerfile pour l'app Flask Loan Default Prediction
# ============================================================

# Étape 1 : base Python légère
FROM python:3.11-slim

# Empêcher Python d'écrire des fichiers .pyc et d'utiliser le buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer le dossier de travail
WORKDIR /app

# Installer dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copier tout le code de l’application
COPY . .

# Exposer le port sur lequel Flask tourne
EXPOSE 5000

# Démarrer l’app avec Gunicorn
# "src.app:app" = chemin vers ton objet Flask (fichier src/app.py contenant app = Flask(__name__))
CMD ["gunicorn", "--workers", "2", "--threads", "4", "--bind", "0.0.0.0:5000", "app:app"]
