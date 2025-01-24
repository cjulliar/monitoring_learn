from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, DataQualityPreset
from evidently.metrics import DatasetDriftMetric
import pandas as pd
from sklearn.datasets import load_wine
import threading
import time
import os
from prometheus_client import Gauge
import logging
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset
from sklearn.model_selection import train_test_split

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Métriques Evidently pour Prometheus
drift_gauge = Gauge('data_drift_score', 'Data Drift Score')

class ModelMonitor:
    def __init__(self):
        logger.info("Initializing ModelMonitor...")
        
        # Créer un dossier pour les rapports
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        logger.info(f"Reports directory created at {self.reports_dir}")
        
        self._initialize_data()
        
        self.prediction_count = 0
        
        # Démarrer le monitoring en arrière-plan
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def _initialize_data(self):
        # Charger les données Wine
        wine = load_wine()
        self.data = pd.DataFrame(data=wine.data, columns=wine.feature_names)
        self.data['target'] = wine.target
        
        # Diviser en données de référence et de production
        self.reference_data, self.current_data = train_test_split(
            self.data, 
            train_size=0.5, 
            shuffle=True, 
            stratify=self.data['target']
        )

    def generate_data_drift_report(self):
        report = Report(metrics=[
            DataDriftPreset(),
        ])
        
        report.run(current_data=self.current_data, 
                  reference_data=self.reference_data,
                  column_mapping=None)
        
        report.save_html(os.path.join(self.reports_dir, "data_drift_report.html"))
        
    def generate_data_stability_test(self):
        test_suite = TestSuite(tests=[
            DataStabilityTestPreset(),
        ])
        
        test_suite.run(current_data=self.current_data,
                      reference_data=self.reference_data,
                      column_mapping=None)
        
        test_suite.save_html(os.path.join(self.reports_dir, "data_stability_test.html"))

    def log_prediction(self, features, prediction, latency):
        try:
            # Convertir features en DataFrame si ce n'est pas déjà le cas
            if not isinstance(features, pd.DataFrame):
                features = pd.DataFrame([features], columns=self.reference_data.columns)
            
            self.current_data = pd.concat([self.current_data, features])
            self.prediction_count += 1
            logger.info(f"Logged prediction #{self.prediction_count}")
            
            # Générer un rapport tous les 5 prédictions
            if self.prediction_count % 5 == 0:
                logger.info(f"Triggering report generation after {self.prediction_count} predictions")
                self._generate_reports()
        except Exception as e:
            logger.error(f"Error in log_prediction: {e}")

    def _generate_reports(self):
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            logger.info(f"Starting report generation at {timestamp}")
            
            # Vérifier les données
            logger.info(f"Current data shape: {self.current_data.shape}")
            logger.info(f"Reference data shape: {self.reference_data.shape}")
            
            # Rapport de Data Drift
            data_drift_report = Report(metrics=[DataDriftPreset()])
            data_drift_report.run(reference_data=self.reference_data, 
                                current_data=self.current_data)
            
            report_path = os.path.join(self.reports_dir, f"data_drift_{timestamp}.html")
            data_drift_report.save_html(report_path)
            logger.info(f"Data drift report saved to {report_path}")
            
            # Rapport de Qualité des Données
            quality_report = Report(metrics=[DataQualityPreset()])
            quality_report.run(reference_data=self.reference_data, 
                             current_data=self.current_data)
            
            quality_path = os.path.join(self.reports_dir, f"data_quality_{timestamp}.html")
            quality_report.save_html(quality_path)
            logger.info(f"Data quality report saved to {quality_path}")
            
        except Exception as e:
            logger.error(f"Error generating reports: {e}", exc_info=True)

    def _monitoring_loop(self):
        while True:
            if len(self.current_data) >= 50:
                self._generate_reports()
                self.current_data = pd.DataFrame()
            time.sleep(60) 