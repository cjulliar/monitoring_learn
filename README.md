# Monitoring d’une application avec Evidently AI, Prometheus, et Grafana

## **Description du projet**

Ce projet vise à démontrer la robustesse d'une API de prédiction basée sur un modèle de machine learning grâce à un système complet de monitoring. Il intègre les outils suivants :

- **Evidently AI** pour surveiller les performances du modèle et détecter les dérives (data drift, concept drift, target drift).
- **Prometheus** pour collecter des métriques sur l’API et l’infrastructure.
- **Grafana** pour visualiser ces métriques dans des tableaux de bord interactifs.

Ce README explique comment déployer et utiliser le projet.

---

## **Prérequis**

- **Docker** et **Docker Compose** installés sur votre machine.
- Python 3.8 ou une version supérieure si vous souhaitez exécuter les scripts Python localement.

---

## **Structure du projet**

```
.
├── app/                          # Code source de l'API
├── prometheus/
│   └── prometheus.yml            # Configuration Prometheus
├── grafana/
│   ├── provisioning/             # Configuration Grafana
│   └── config.monitoring         # Variables d'environnement Grafana
├── monitoring_ml/                # Scripts de monitoring ML
│   ├── api_wine.ipynb            # Notebook pour l'API Wine
│   ├── file2.html                # Rapport Evidently AI
│   └── o_drift.html              # Rapport de dérive Evidently AI
├── requirements.txt              # Dépendances Python
├── docker-compose.yml            # Orchestration des services
└── README.md                     # Documentation
```

---

## **Démarrage rapide**

1. **Cloner le dépôt** :
   ```bash
   git clone <url_du_depot>
   cd <nom_du_depot>
   ```

2. **Créer et activer un environnement Python** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sous Windows : .\venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer les services** :
   ```bash
   docker-compose up -d
   ```

5. **Accéder aux services** :
   - **API FastAPI** : [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Prometheus** : [http://localhost:9090](http://localhost:9090)
   - **Grafana** : [http://localhost:3000](http://localhost:3000)
     - Identifiants par défaut : `admin` / `admin`

6. **Exécuter le Notebook `api_wine.ipynb`** :
   - Lancer Jupyter Notebook :
     ```bash
     jupyter notebook
     ```
   - Ouvrir le fichier `monitoring_ml/api_wine.ipynb` et exécuter les cellules.

---

## **Fonctionnalités**

### **1. API FastAPI**

L'API fournit un endpoint `/predict` pour générer des prédictions à partir d'un modèle de machine learning. 

- **Endpoints disponibles** :
  - `/predict` : Retourne une prédiction basée sur les données envoyées.
  - `/metrics` : Expose des métriques collectées pour Prometheus.

### **2. Prometheus**

Prometheus collecte les métriques suivantes :
- Nombre de requêtes API.
- Temps de réponse moyen.
- Taux d’erreurs (codes 4xx et 5xx).
- Utilisation des ressources système (CPU, RAM, disque).

Ces métriques sont configurées dans `prometheus/prometheus.yml`.

### **3. Grafana**

Grafana permet de visualiser les métriques collectées dans des tableaux de bord interactifs.

- **Tableaux de bord disponibles** :
  - **API Monitoring** :
    - Répartition des requêtes (2xx, 4xx, 5xx).
    - Temps de réponse moyen.
    - Volume total de requêtes.
  - **Infrastructure Monitoring** :
    - Utilisation du CPU.
    - Utilisation de la mémoire.
    - Utilisation du disque.

### **4. Evidently AI**

Evidently AI analyse les performances du modèle et les dérives dans les données :
- **Data Drift** : Comparaison des distributions des données d’entrée avec un jeu de référence.
- **Performance Drift** : Suivi des performances du modèle (précision, F1-score, etc.).

Un rapport Evidently est généré dans un fichier HTML :
```bash
python generate_evidently_report.py
```

---

## **Détails techniques**

### **Docker Compose**

Le fichier `docker-compose.yml` orchestre les services suivants :

- **`app`** : Conteneur pour l’API FastAPI.
- **`prometheus`** : Service de collecte des métriques.
- **`grafana`** : Service de visualisation des métriques.
- **`node-exporter`** : Service pour surveiller les ressources système.

Pour vérifier les logs des services :
```bash
docker-compose logs -f <nom_du_service>
```

### **Configuration Prometheus**

Le fichier `prometheus/prometheus.yml` contient :
```yaml
scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['172.16.238.10:8000']
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['172.16.238.13:9100']
```

### **Configuration Grafana**

Les dashboards Grafana sont configurés dans `grafana/provisioning/`. Les métriques de Prometheus sont ajoutées comme source de données.

---

## **Tests et validation**

1. **Tester l'API** :
   - Envoyer une requête à l'endpoint `/predict` avec un jeu de données.
   ```bash
   curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"feature1": 1.0, "feature2": 2.0}'
   ```

2. **Valider les métriques** :
   - Accéder à Prometheus pour visualiser les métriques.
   - Vérifier les tableaux de bord Grafana.

3. **Générer un rapport Evidently** :
   - Exécute le script de rapport :
   ```bash
   python generate_evidently_report.py
   ```

4. **Consulter les rapports Evidently** :
   - Ouvre les fichiers `monitoring_ml/file2.html` et `monitoring_ml/o_drift.html` dans un navigateur pour visualiser les analyses.
![Dashboard Grafana](<Dashboard Grafana.png>)
---

## **Astuces de dépannage**

- **Problème : Les services ne démarrent pas** :
  - Vérifie que Docker est bien installé et en cours d’exécution.
  - Lance `docker-compose down && docker-compose up -d`.

- **Problème : Pas de données dans Grafana** :
  - Vérifie la configuration Prometheus dans Grafana.
  - Assure-toi que l’API génère des métriques sur `/metrics`.

---

## **Ressources utiles**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [Evidently AI Documentation](https://docs.evidentlyai.com/)

---

## **Auteur**

Projet réalisé par **Cyju3000**, équipe technique.

