from .init import curs
from models.creature import Creature

curs.execute(
    """
    CREATE TABLE IF NOT EXISTS creature (
        name TEXT PRIMARY KEY,
        country TEXT,
        area TEXT,
        description TEXT,
        aka TEXT
    )
    """
)


def row_to_model(row: tuple) -> Creature:
    """Convert row tuple into Creature object"""
    name, country, area, description, aka = row
    return Creature(name, country, area, description, aka)


def model_to_dict(creature: Creature) -> dict:
    """Convert Creature object to a dictionary"""
    return creature.model_dump()


def get_one(name: str) -> Creature | None:
    """Find and return a Creature object by name"""
    query = """
            SELECT * FROM creature
            WHERE name = :name
            """
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    return row_to_model(row)


def get_all() -> list[Creature]:
    """Return all Creature objects in the database"""
    query: str = "SELECT * FROM creature"
    curs.execute(query)
    rows: list[tuple] = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    """Add a new creature to the dataabse"""
    query: str = """
            INSERT INTO creature (name, country,area, description, aka)
            VALUES (:name, :country, :area, :description, :aka)
            """
    params: dict = model_to_dict(creature)
    curs.execute(query, params)
    return get_one(creature.name)


def modify(creature: Creature) -> Creature:
    """Modify or update a creature"""
    query: str = """
            UPDATE creature
            SET name = :name,
                country = :country,
                area = :area,
                description = :description,
                aka = :aka
            WHERE name = :original_name
            """
    params: dict = model_to_dict(creature)
    params["original_name"] = creature.name
    curs.execute(query, params)
    return get_one(creature.name)


def delete(name: str) -> bool:
    """Remove a creature from the database"""
    query: str = "DELETE FROM creature WHERE name = :name"
    params: dict = {"name": name}
    res = curs.execute(query, params)
    return bool(res)
