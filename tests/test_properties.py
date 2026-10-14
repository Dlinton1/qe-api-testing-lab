import pytest
from fastapi.testclient import TestClient

from app.main import app, properties

client = TestClient(app)
AUTH = {"Authorization": "Bearer local-test-token"}


@pytest.fixture(autouse=True)
def reset_properties():
    properties.clear()


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_property_with_valid_data():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Harbor Apartments", "monthly_rent": 1800},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["name"] == "Harbor Apartments"
    assert body["monthly_rent"] == 1800


def test_list_properties_requires_authentication():
    response = client.get("/api/properties")

    assert response.status_code == 401


def test_create_property_rejects_missing_authentication():
    response = client.post(
        "/api/properties",
        json={"name": "Harbor Apartments", "monthly_rent": 1800},
    )

    assert response.status_code == 401


def test_create_property_rejects_invalid_token():
    response = client.post(
        "/api/properties",
        headers={"Authorization": "Bearer wrong-token"},
        json={"name": "Harbor Apartments", "monthly_rent": 1800},
    )

    assert response.status_code == 401


def test_create_property_rejects_missing_name():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"monthly_rent": 1800},
    )

    assert response.status_code == 422


def test_create_property_rejects_empty_name():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "", "monthly_rent": 1800},
    )

    assert response.status_code == 422


def test_create_property_rejects_name_over_100_characters():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "P" * 101, "monthly_rent": 1800},
    )

    assert response.status_code == 422


def test_create_property_accepts_minimum_valid_rent():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Minimum Rent Property", "monthly_rent": 0.01},
    )

    assert response.status_code == 201


def test_create_property_rejects_zero_rent():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Zero Rent Property", "monthly_rent": 0},
    )

    assert response.status_code == 422


def test_create_property_rejects_negative_rent():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Negative Rent Property", "monthly_rent": -1},
    )

    assert response.status_code == 422


def test_create_property_accepts_maximum_valid_rent():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Maximum Rent Property", "monthly_rent": 1_000_000},
    )

    assert response.status_code == 201


def test_create_property_rejects_rent_above_maximum():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Over Limit Property", "monthly_rent": 1_000_000.01},
    )

    assert response.status_code == 422


def test_create_property_rejects_non_numeric_rent():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Invalid Rent Property", "monthly_rent": "not-a-number"},
    )

    assert response.status_code == 422


def test_create_property_rejects_missing_rent():
    response = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Missing Rent Property"},
    )

    assert response.status_code == 422


def test_created_property_appears_in_list():
    created = client.post(
        "/api/properties",
        headers=AUTH,
        json={"name": "Regression Property", "monthly_rent": 2200},
    )
    assert created.status_code == 201

    listed = client.get("/api/properties", headers=AUTH)

    assert listed.status_code == 200
    assert any(
        item["name"] == "Regression Property"
        for item in listed.json()
    )
