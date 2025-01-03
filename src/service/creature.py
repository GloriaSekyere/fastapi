from models.creature import Creature

# import fake.creature as data

import data.creature as data


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(name: str) -> Creature | None:
    return data.get(name)


def create(creature: Creature) -> Creature:
    return data.create(creature)


def replace(id, creature: Creature) -> Creature:
    return data.replace(id, creature)


def modify(creature: Creature) -> Creature:
    return data.modify(creature)


def delete(name: str) -> bool:
    return data.delete(name)
