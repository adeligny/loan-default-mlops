# Fichier de Test Git 

Date: 19/10/2025 22:32
Auteur: Tindo Raoulf
Projet: Loan Default MLOps
Statut: En apprentissage 

## Description
Ce fichier sert à pratiquer Git sans impacter le projet.

## Objectifs du Projet (README.md)

### 1. Installation et Configuration
- Créer un environnement virtuel Python
- Installer les dépendances (requirements.txt)
- Configurer Flask et MLflow

### 2. Entraînement du Modèle
- Charger les données loans.csvm- Entraîner le modèle de prédictionm- Commande: python src/train.py --data data/loans.csvmm### 3. Tracking avec MLflow
- Enregistrer les métriques: precision, f1, roc_auc
- Lancer l'interface: mlflow ui --port 5001
- Comparer les expériences

### 4. Lancer l'Application Flask
- Démarrer le serveur: python app.py
- Accès: http://127.0.0.1:5000
- API de prédiction en temps réel

### 5. Conteneurisation Docker
- Build: docker build -t loan-default-app .
- Run: docker run -p 5000:5000 loan-default-app
- Environnement isolé et portable

### 6. Configuration AWS (ECS + ECR)
- Créer un repository ECR
- Créer un cluster ECS
- Créer un service ECS

### 7. Secrets GitHub
- Ajouter AWS_ACCESS_KEY_ID
- Ajouter AWS_SECRET_ACCESS_KEY
- Configuration sécurisée

## Statistiques
Commits effectués: 17
