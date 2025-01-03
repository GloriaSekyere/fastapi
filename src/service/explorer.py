from models.explorer import Explorer
import data.explorer as data


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    return data.get(name)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def modify(explorer: Explorer) -> Explorer:
    return data.modify(explorer)


def delete(name: str) -> bool:
    return data.delete(name)
