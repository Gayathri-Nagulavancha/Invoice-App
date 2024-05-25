# test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from main import app, get_db

# Configure to use the actual PostgreSQL database
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:pgadmin123@localhost/invoice"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    yield TestingSessionLocal()

def test_get_all_invoices(test_db):
    response = client.get("/invoices/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4

def test_get_invoice_by_id(test_db):
    response = client.get("/invoicebyid/2")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == "INV002"
    assert data["amount"] == 200.0
    assert data["status"] == "Paid"
    assert data["date"] == "2024-05-01T00:00:00"

def test_create_invoice(test_db):
    response = client.post("/addinvoices/", json={"id": 6, "number": "INV004", "amount": 1500.0, "status": "UnPaid", "date": "2024-06-01T00:00:00"})
    assert response.status_code == 201
    data = response.json()
    assert data["number"] == "INV004"
    assert data["amount"] == 1500.0
    assert data["status"] == "UnPaid"
    assert data["date"] == "2024-06-01T00:00:00"

def test_update_invoice(test_db):
    response = client.put("/invoices/3", json={"id": 3, "number": "INV003", "amount": 1200.0, "status": "Paid", "date": "2024-05-05T00:00:00"})
    assert response.status_code == 202
    data = response.json()
    assert data["number"] == "INV003"
    assert data["amount"] == 1200.0
    assert data["status"] == "Paid"
    assert data["date"] == "2024-05-05T00:00:00"

def test_delete_invoice(test_db):
    response = client.delete("/invoices/4")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == "INV001"
    assert data["amount"] == 800.0
    assert data["status"] == "Paid"
    assert data["date"] == "2024-05-01T00:00:00"
    # Check that the invoice no longer exists
    response = client.get("/invoicebyid/4")
    assert response.status_code == 404




# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# async def test_create_invoice():
#     response = await client.post("/invoices/", json={"number": "INV001", "amount": 100.0, "status": "Paid", "date": "2024-05-01T00:00:00"})
#     assert response.status_code == 200
#     assert response.json()["number"] == "INV001"

# async def test_read_invoices():
#     response = await client.get("/invoices/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# async def test_update_invoice():
#     response = await client.put("/invoices/1", json={"amount": 150.0})
#     assert response.status_code == 200
#     assert response.json()["amount"] == 150.0

# async def test_delete_invoice():
#     response = await client.delete("/invoices/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == 1
