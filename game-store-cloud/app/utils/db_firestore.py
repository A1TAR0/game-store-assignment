from google.cloud import firestore
import os

def get_firestore_client():
    """Initialize and return Firestore client"""
    project_id = os.getenv('GCP_PROJECT_ID')
    return firestore.Client(project=project_id)

# Initialize client
db = get_firestore_client()