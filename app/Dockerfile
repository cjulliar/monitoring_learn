FROM python:3.11-slim

WORKDIR /app/

# Copier d'abord requirements.txt seul
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Créer le dossier reports
RUN mkdir reports

# Copier le reste des fichiers
COPY . .

# Générer le modèle
RUN python generate_ml.py

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
