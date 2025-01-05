import pytest
from fastapi.testclient import TestClient
from models.explorer import Explorer
from main import app

client = TestClient(app)


@pytest.fixture(scope="session")
def sample() -> Explorer:
    return Explorer(name="Optimus Prime", country="SPC", description="")


def test_create(sample):
    resp = client.post(f"/explorer", json=sample.model_dump())
    assert resp.status_code == 201
    assert resp.json() == sample.model_dump()


def test_create_duplicate(sample):
    resp = client.post(f"/explorer", json=sample.model_dump())
    assert resp.status_code == 409


def test_get_one(sample):
    resp = client.get(f"/explorer/{sample.name}")
    assert resp.status_code == 200
    assert resp.json() == sample.model_dump()


def test_get_one_missing():
    resp = client.get("/explorer/non_existent_explorer")
    assert resp.status_code == 404


def test_modify(sample):
    sample.description = "Transformer"
    resp = client.patch(f"/explorer/{sample.name}", json=sample.model_dump())
    assert resp.status_code == 200
    assert resp.json() == sample.model_dump()


def test_modify_missing(sample):
    resp = client.patch("/explorer/non_existent_explorer", json=sample.model_dump())
    assert resp.status_code == 404


def test_delete(sample):
    resp = client.delete(f"/explorer/{sample.name}")
    assert resp.status_code == 204
    assert resp.text == ""


def test_delete_missing(sample):
    resp = client.delete(f"/explorer/{sample.name}")
    assert resp.status_code == 404
