from .init import curs, IntegrityError
from error import Duplicate, Missing
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
    return Creature(
        name=name, country=country, area=area, description=description, aka=aka
    )


def model_to_dict(creature: Creature) -> dict:
    """Convert Creature object to a dictionary"""
    return creature.model_dump()


def get_one(name: str) -> Creature:
    """Find and return a Creature object by name"""
    query = """
            SELECT * FROM creature
            WHERE name = :name
            """
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Creature {name} does not exist")


def get_all() -> list[Creature]:
    """Return all Creature objects in the database"""
    query: str = "SELECT * FROM creature"
    curs.execute(query)
    rows: list[tuple] = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    if not creature:
        return None
    """Add a new creature to the dataabse"""
    query: str = """
            INSERT INTO creature (name, country,area, description, aka)
            VALUES (:name, :country, :area, :description, :aka)
            """
    params: dict = model_to_dict(creature)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"Creature {creature.name} already exists")
    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature:
    """Modify or update a creature"""
    if not (name and creature):
        return None
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
    params["original_name"] = name
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(creature.name)
    else:
        raise Missing(msg=f"Creature {name} does not exist")


def delete(name: str):
    """Remove a creature from the database"""
    if not name:
        return False
    query: str = "DELETE FROM creature WHERE name = :name"
    params: dict = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Creature {name} does not exist")
