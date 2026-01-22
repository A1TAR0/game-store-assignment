from google.cloud import firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_firestore_client():
    """Initialize and return Firestore client"""
    project_id = os.getenv('GCP_PROJECT_ID')
    if not project_id:
        raise ValueError("GCP_PROJECT_ID not found in environment variables")
    return firestore.Client(project=project_id)

# Initialize client
db = get_firestore_client()