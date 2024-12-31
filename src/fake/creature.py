from model.creature import Creature

_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="Bigfoot",
        description="Yeti's Cousin Eddie",
        country="US",
        area="*",
        aka="Sasquatch",
    ),
]


def get_one(name: str) -> Creature | None:
    """Get a single creature by name"""
    for creature in _creatures:
        if name == creature.name:
            return creature
    return None


def get_all() -> list[Creature]:
    """Get all creatures"""
    return _creatures


def create(creature: Creature) -> Creature:
    """Add a new creature"""
    return creature


def modify(creature: Creature) -> Creature:
    """Modify an exisiting creature"""
    return creature


def replace(creature: Creature) -> Creature:
    return creature


def delete(name: str) -> bool | None:
    """Delete an creature by name"""
    return None
