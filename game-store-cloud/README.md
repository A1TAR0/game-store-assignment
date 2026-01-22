# Game Store Cloud Application

A cloud-based video game store application built with Python, Flask, and Google Cloud Platform.

## Features
- User authentication and authorization
- Game catalog browsing
- Shopping cart and order processing
- User reviews and ratings
- Wishlist functionality

## Tech Stack
- **Backend**: Python, Flask
- **Databases**: Google Cloud SQL (PostgreSQL), Firestore
- **Cloud Platform**: Google App Engine, Cloud Functions
- **Authentication**: Firebase Auth / Custom implementation
- **Version Control**: GitHub

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your credentials
6. Run: `python main.py`

## Database Setup
[To be added]

## Deployment
[To be added]

# Testing Guide

## Running Unit Tests

### Run all tests
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_models.py -v
```

### Run with coverage
```bash
pytest --cov=app tests/
```

### Run specific test class
```bash
pytest tests/test_models.py::TestUserModel -v
```

## Cloud Functions Testing

### Test Email Function Locally
```bash
cd cloud_functions/send_order_email
functions-framework --target=send_order_email --debug
```

Then test with:
```bash
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{"email":"test@example.com","order_id":123,"total":99.99,"items":[{"title":"Test Game","quantity":1}]}'
```

### Test Recommendation Function Locally
```bash
cd cloud_functions/recommend_games
functions-framework --target=recommend_games --debug
```

Then test with:
```bash
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{"genres":["RPG"],"platforms":["PC"],"budget":60}'
```

## Test Coverage Goals
- Models: 80%+
- Routes: 70%+
- Utilities: 90%+