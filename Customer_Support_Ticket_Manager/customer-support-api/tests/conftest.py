import os

# Configure the test database before importing the application.
os.environ["DATABASE_URL"] = "sqlite:///./test_customer_support.db"

import pytest
from fastapi.testclient import TestClient

from app import models  # Ensure all models are registered.
from app.database import Base, engine
from app.main import app


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)