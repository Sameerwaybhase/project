from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "UP"

def test_get_products():
    res = client.get("/products")
    assert res.status_code == 200
    assert len(res.json()["products"]) > 0

def test_order_unauthorized():
    res = client.post("/orders", json={"product_id": 1, "quantity": 2})
    assert res.status_code == 401
