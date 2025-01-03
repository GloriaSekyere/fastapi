from .init import curs
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
    return Explorer(name, country, description)


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
    return row_to_model(row)


def get_all() -> list[Explorer]:
    query = "SELECT * FROM explorer"
    curs.execute(query)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer):
    query = """
            INSERT INTO explorer (name, country, description)
            VALUES (:name, :country, :description)
            """
    params = model_to_dict(explorer)
    curs.execute(query, params)
    return get_one(explorer.name)


def modify(explorer: Explorer) -> Explorer:
    query = """
            UPDATE explorer
            SET name = :name,
                country = :country,
                area = :area,
                description = :description,
                aka = :aka
            WHERE name = :original_name
            """
    params = model_to_dict(explorer)
    params["original_name"] = explorer.name
    curs.execute(query, params)
    return get_one(explorer.name)


def delete(explorer: Explorer) -> bool:
    query = "DELETE FROM explorer WHERE name = :name"
    params = {"name": explorer.name}
    res = curs.execute(query, params)
    return bool(res)
