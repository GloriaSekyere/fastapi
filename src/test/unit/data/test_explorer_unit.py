import os
import pytest
from models.explorer import Explorer
from error import Duplicate, Missing

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Twyla Dill", country="USA", description="Kakra's wife")


def test_create(sample):
    resp = explorer.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = explorer.create(sample)


def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = explorer.get_one("non_existent_explorer")


def test_modify(sample):
    sample.country = "GHA"
    resp = explorer.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    with pytest.raises(Missing):
        person: Explorer = Explorer(name="Not Real", country="NA", description="")
        _ = explorer.modify(person.name, person)


def test_delete(sample):
    resp = explorer.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        _ = explorer.delete(sample.name)
