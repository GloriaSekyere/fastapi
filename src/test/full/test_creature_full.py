import pytest
from main import app
from fastapi.testclient import TestClient
from models.creature import Creature


client = TestClient(app)


@pytest.fixture(scope="session")
def sample() -> Creature:
    return Creature(name="Kakai", country="PT", area="LIS", description="", aka="Ghost")


def test_create(sample):
    resp = client.post("/creature", json=sample.model_dump())
    assert resp.status_code == 201
    assert resp.json() == sample.model_dump()


def test_create_duplicate(sample):
    resp = client.post("/creature", json=sample.model_dump())
    assert resp.status_code == 409


def test_get_one(sample):
    resp = client.get(f"/creature/{sample.name}")
    assert resp.status_code == 200
    assert resp.json() == sample.model_dump()


def test_get_one_missing():
    resp = client.get("/creature/non_existent_creature")
    assert resp.status_code == 404


def test_modify(sample):
    sample.area = "KSI"
    resp = client.patch(f"/creature/{sample.name}", json=sample.model_dump())
    assert resp.status_code == 200
    assert resp.json() == sample.model_dump()


def test_modify_missing(sample):
    resp = client.patch(f"/creature/non_existent_creature", json=sample.model_dump())
    assert resp.status_code == 404


def test_delete(sample):
    resp = client.delete(f"/creature/{sample.name}")
    assert resp.status_code == 204
    assert resp.text == ""


def test_delete_missing(sample):
    resp = client.delete(f"/creature/{sample.name}")
    assert resp.status_code == 404
