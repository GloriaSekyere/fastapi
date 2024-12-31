from models.explorer import Explorer

_explorers = [
    Explorer(name="Claude Hande", country="FR", description="Scarce during full moons"),
    Explorer(name="Noah Weiser", country="DE", description="Myopic machete man"),
]


def get_one(name: str) -> Explorer | None:
    """Get a single explorer by name"""
    for explorer in _explorers:
        if name == explorer.name:
            return explorer
    return None


def get_all() -> list[Explorer]:
    """Get all explorers"""
    return _explorers


def create(explorer: Explorer) -> Explorer:
    """Add a new explorer"""
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """Modify an exisiting explorer"""
    return explorer


def replace(explorer: Explorer) -> Explorer:
    return explorer


def delete(name: str) -> bool | None:
    """Delete an explorer by name"""
    return None
