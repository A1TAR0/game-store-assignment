from app.utils.db_sql import init_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug: print to verify .env is loaded
print(f"Project ID: {os.getenv('GCP_PROJECT_ID')}")
print(f"Connection Name: {os.getenv('CLOUD_SQL_CONNECTION_NAME')}")
print(f"DB Name: {os.getenv('DB_NAME')}")

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")