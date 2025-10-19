# Fichier de Test Git 

Date: 19/10/2025 22:23# ============================================
# Assurez-vous d'être sur la bonne branche
# ============================================
cd C:\Users\User\Documents\Projet_MLOPS_bon\Projet_MLOPS-1\loan-default-mlops

# Vérifiez votre branche actuelle
git branch

# Si vous n'êtes pas sur feature/commits-simples, créez une nouvelle branche
git checkout main
git pull origin main
git checkout -b feature/ajout-readme-doc

# ============================================
# COMMIT : Ajout de la documentation du README
# ============================================
@"
# Documentation du Projet Loan Default MLOps

 **Date :** 19/10/2025 22:23  
 **Auteur :** Tindo Raoulf  
 **Dépôt :** https://github.com/adeligny/loan-default-mlops

---

##  Présentation du Projet

**Prévision des défauts de paiement  MLOps (Flask + MLflow + AWS)**

Ce projet adapte un modèle Flask pour un problème de **prédiction de défaut de prêt**.
Il utilise une stack MLOps complète avec :
-  **Flask** : Framework web pour l'API
-  **MLflow** : Tracking des expériences ML
-  **AWS** : Déploiement cloud (ECS + ECR)
-  **Docker** : Conteneurisation de l'application

---

##  Démarrage Rapide (Local)

### 1 Configuration de l'environnement

**Sur Windows (PowerShell) :**
\\\powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
\\\

**Sur Linux/Mac :**
\\\ash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\\\

### 2 Entraînement du modèle
\\\ash
python src/train.py --data data/loans.csv --experiment-name "loan-default-baseline"
\\\

**Ce script va :**
- Charger les données de prêts
- Entraîner le modèle de classification
- Enregistrer les métriques dans MLflow : \precision\, \1\, \oc_auc\

### 3 Lancer l'application Flask
\\\ash
python app.py
\\\

 **Accès :** http://127.0.0.1:5000

---

##  MLflow - Interface de Tracking

### Démarrer l'interface MLflow
\\\ash
mlflow ui --port 5001
\\\

 **Accès :** http://127.0.0.1:5001

### Métriques enregistrées
- **Precision** : Précision du modèle
- **F1-Score** : Équilibre précision/rappel
- **ROC-AUC** : Performance de classification

Vous pouvez comparer différentes expériences et versions du modèle via l'interface MLflow.

---

##  Docker - Conteneurisation

### Construire l'image Docker
\\\ash
docker build -t loan-default-app .
\\\

### Lancer le conteneur
\\\ash
docker run -p 5000:5000 loan-default-app
\\\

 **Accès :** http://localhost:5000

**Avantages :**
-  Environnement isolé et reproductible
-  Déploiement simplifié
-  Compatibilité multi-plateforme

---

##  AWS - Déploiement Cloud (ECS + ECR)

### Configuration AWS

#### 1 Prérequis
- Compte AWS actif
- AWS CLI configuré
- Créer un **repository ECR** (Elastic Container Registry)
- Créer un **cluster ECS** (Elastic Container Service)
- Créer un **service ECS**

#### 2 Secrets GitHub à ajouter
Allez dans **Settings**  **Secrets and variables**  **Actions** :

| Secret | Description |
|--------|-------------|
| \AWS_ACCESS_KEY_ID\ | ID de la clé d'accès AWS |
| \AWS_SECRET_ACCESS_KEY\ | Clé secrète AWS |

#### 3 Configuration du workflow
Modifiez \.github/workflows/aws.yml\ avec vos paramètres :
- Nom du repository ECR
- Nom du cluster ECS
- Nom du service ECS
- Région AWS

#### 4 Déploiement automatique
\\\ash
git add .
git commit -m "feat: configuration AWS"
git push origin main
\\\

Le **push sur main** déclenche automatiquement :
1. Construction de l'image Docker
2. Push vers ECR
3. Déploiement sur ECS
4. Mise à jour du service

---

##  Architecture du Projet

\\\
loan-default-mlops/

 data/
    loans.csv              # Données d'entraînement

 src/
    train.py               # Script d'entraînement

 app.py                     # Application Flask
 requirements.txt           # Dépendances Python
 Dockerfile                 # Configuration Docker

 .github/
    workflows/
        aws.yml            # CI/CD GitHub Actions

 mlruns/                    # Données MLflow (local)
\\\

---

##  Workflow MLOps Complet

\\\
1. Développement Local
    Entraînement du modèle (train.py)
    Tracking MLflow
    Test de l'API Flask
   
2. Versionning Git
    Commit des changements
    Push vers GitHub
   
3. CI/CD (GitHub Actions)
    Tests automatiques
    Build Docker image
    Push vers AWS ECR
   
4. Déploiement AWS
    Pull image depuis ECR
    Déploiement sur ECS
    Service accessible publiquement
\\\

---

##  Métriques de Performance

| Métrique | Description | Objectif |
|----------|-------------|----------|
| **Precision** | Taux de vrais positifs | > 85% |
| **Recall** | Capacité à détecter les défauts | > 80% |
| **F1-Score** | Moyenne harmonique | > 82% |
| **ROC-AUC** | Performance globale | > 0.90 |

---

##  Technologies Utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.8+ | Langage principal |
| Flask | 2.x | API Web |
| MLflow | 2.x | Tracking ML |
| Docker | Latest | Conteneurisation |
| AWS ECS | - | Orchestration |
| AWS ECR | - | Registry Docker |
| GitHub Actions | - | CI/CD |

---

##  Cas d'Usage

Ce système de prédiction peut être utilisé par :
-  **Banques** : Évaluer le risque de crédit
-  **Fintechs** : Automatiser l'approbation de prêts
-  **Analystes** : Analyser les tendances de défaut
-  **Data Scientists** : Améliorer les modèles prédictifs

---

##  Commandes Utiles

### Gestion de l'environnement virtuel
\\\ash
# Activer
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Désactiver
deactivate
\\\

### Docker
\\\ash
# Voir les conteneurs actifs
docker ps

# Arrêter un conteneur
docker stop <container_id>

# Supprimer une image
docker rmi loan-default-app
\\\

### MLflow
\\\ash
# Supprimer les expériences
rm -rf mlruns/

# Exporter un modèle
mlflow models serve -m runs:/<run_id>/model -p 5002
\\\

---

##  Troubleshooting

### Problème : Module non trouvé
\\\ash
pip install -r requirements.txt --upgrade
\\\

### Problème : Port déjà utilisé
\\\ash
# Changer le port dans app.py
app.run(port=5001)
\\\

### Problème : Docker build échoue
\\\ash
# Nettoyer le cache Docker
docker system prune -a
\\\

---

##  Sécurité

 **Important :**
- Ne jamais commiter les clés AWS dans Git
- Utiliser des secrets GitHub pour les credentials
- Limiter les permissions IAM au strict nécessaire
- Activer le HTTPS en production

---

##  Support

-  **Email :** tindoraoulf@gmail.com
-  **GitHub Issues :** [Créer une issue](https://github.com/adeligny/loan-default-mlops/issues)
-  **Discussions :** [GitHub Discussions](https://github.com/adeligny/loan-default-mlops/discussions)

---

** Note :** Ce document sert de référence pour comprendre le projet sans modifier le code source.

*Dernière mise à jour : 19/10/2025 à 22:23*
