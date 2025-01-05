from .init import curs, IntegrityError
from error import Missing, Duplicate
from models.explorer import Explorer

curs.execute(
    """
    CREATE TABLE IF NOT EXISTS explorer (
        name TEXT PRIMARY KEY,
        country TEXT,
        description TEXT
    )
    """
)


def row_to_model(row: tuple) -> Explorer:
    """Convert a row tuple to an Explorer object"""
    name, country, description = row
    return Explorer(name=name, country=country, description=description)


def model_to_dict(explorer: Explorer) -> dict:
    """Convert Explorer object to dictionary"""
    return explorer.model_dump()


def get_one(name: str) -> Explorer:
    query = """
            SELECT * FROM explorer
            WHERE name = :name
            """
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def get_all() -> list[Explorer]:
    query = "SELECT * FROM explorer"
    curs.execute(query)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    if not explorer:
        return None
    query = """
            INSERT INTO explorer (name, country, description)
            VALUES (:name, :country, :description)
            """
    params = model_to_dict(explorer)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists")
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer):
        return None
    query = """
            UPDATE explorer
            SET name = :name,
                country = :country,
                description = :description
            WHERE name = :original_name
            """
    params = model_to_dict(explorer)
    params["original_name"] = name
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {explorer.name} not found")


def delete(name: str):
    if not name:
        return False
    query = "DELETE FROM explorer WHERE name = :name"
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
