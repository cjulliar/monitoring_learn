# Monitoring d'une application ML avec Evidently AI, Prometheus, et Grafana

## Description du projet

Ce projet démontre la mise en place d'un système complet de monitoring pour une API de prédiction ML. Il utilise le dataset Wine de scikit-learn et intègre :

- Une **API FastAPI** pour les prédictions
- **Evidently AI** pour la détection des dérives (data drift, concept drift)
- **Prometheus** pour la collecte des métriques
- **Grafana** pour la visualisation des performances

## Architecture

```
.
├── app/                    # Code source de l'API
│   ├── main.py            # API FastAPI
│   ├── monitoring.py      # Monitoring Evidently AI
│   ├── generate_ml.py     # Génération du modèle
│   └── Dockerfile         # Configuration Docker
├── prometheus/
│   └── prometheus.yml     # Configuration Prometheus
├── grafana/
│   ├── provisioning/      # Configuration Grafana
│   └── config.monitoring  # Variables d'environnement
├── docker-compose.yml     # Orchestration des services
└── README.md
```

## Prérequis

- Docker et Docker Compose
- Python 3.11 ou supérieur (pour le développement local)

## Installation

1. **Cloner le dépôt** :
```bash
git clone <url-du-repo>
cd <nom-du-projet>
```

2. **Lancer les services** :
```bash
docker-compose up --build
```

## Services disponibles

- **API FastAPI** : http://localhost:8000
  - Documentation Swagger : http://localhost:8000/docs
  - Métriques Prometheus : http://localhost:8000/metrics
- **Prometheus** : http://localhost:9090
- **Grafana** : http://localhost:3000 (admin/admin)

## Test de l'API

Vous pouvez tester l'API via Swagger UI ou avec curl :

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
  "features": [
    14.23,
    1.71,
    2.43,
    15.6,
    127.0,
    2.80,
    3.06,
    0.28,
    2.29,
    5.64,
    1.04,
    3.92,
    1065.0
  ]
}'
```

## Monitoring avec Grafana

Le dashboard Grafana inclut :

![Dashboard Grafana](Dashboard%20Grafana.png)

### Métriques système
- Utilisation CPU
- Utilisation mémoire
- Utilisation disque

### Métriques API
- Distribution des codes HTTP (2xx, 4xx, 5xx)
- Temps de réponse moyen
- Nombre de requêtes par seconde

### Métriques ML
- Nombre de prédictions
- Score de dérive des données
- Distribution des prédictions

## Monitoring avec Evidently AI

Le projet utilise Evidently AI pour :
- Détecter le data drift
- Surveiller la qualité des prédictions
- Générer des rapports de performance

Les rapports sont générés automatiquement et accessibles via l'API.

## Architecture technique

### API FastAPI
- Endpoint `/predict` pour les prédictions
- Intégration avec Prometheus pour les métriques
- Monitoring en temps réel avec Evidently AI

### Prometheus
- Collecte des métriques système et API
- Stockage temporel des données
- Base pour les visualisations Grafana

### Grafana
- Tableaux de bord personnalisables
- Visualisation en temps réel
- Alertes configurables

## Développement local

1. **Créer un environnement virtuel** :
```bash
python -m venv env
source env/Scripts/activate  # Windows
```

2. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Générer le modèle** :
```bash
python app/generate_ml.py
```

## Contribution

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

## Génération des rapports Evidently AI

Les rapports de monitoring ML sont générés via un endpoint dédié :

```bash
# Générer les rapports de data drift et stabilité
curl -X POST "http://localhost:8000/generate_reports"
```

Deux rapports HTML sont générés dans le dossier `reports/` :
- `data_drift_report.html` : Analyse des dérives dans les données
- `data_stability_test.html` : Tests de stabilité des données

Ces rapports permettent de :
- Visualiser les changements dans la distribution des features
- Détecter les anomalies dans les données
- Suivre la stabilité du modèle dans le temps
- Identifier les potentiels problèmes de qualité des données

Pour visualiser les rapports, ouvrez les fichiers HTML générés dans votre navigateur.