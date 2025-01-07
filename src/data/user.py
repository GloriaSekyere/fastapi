from .init import curs, IntegrityError
from models.user import User
from error import Duplicate, Missing

curs.execute(
    """CREATE TABLE IF NOT EXISTS user (
        name TEXT PRIMARY KEY,
        hash TEXT)"""
)

curs.execute(
    """CREATE TABLE IF NOT EXISTS xuser (
        name TEXT PRIMARY KEY,
        hash TEXT)"""
)


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict:
    return user.model_dump()


def get_one(name: str) -> User:
    query = "SELECT * FROM user WHERE name = :name"
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")


def get_all() -> list[User]:
    query = "SELECT * FROM user"
    curs.execute(query)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(user: User, table: str = "user") -> User:
    """Add <user> to user or xuser table"""
    if not user:
        return None
    if table not in ("user", "xuser"):
        raise Exception(f"Invalid table name {table}")
    query = f"INSERT INTO {table} (name, hash) VALUES (:name, :hash)"
    params = model_to_dict(user)
    try:
        curs.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f"{table}: User {user.name} already exists")
    return get_one(user.name)


def modify(name: str, user: User) -> User:
    if not (name and user):
        return None
    query = f"""
            UPDATE user
            SET name = :name, hash = :hash 
            WHERE name = :original_name
            """
    params = model_to_dict(user)
    params["original_name"] = name
    curs.execute(query, params)
    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {name} not found")


def delete(name: str) -> User:
    """Drop user with <name> from user table and add to xuser table"""
    if not name:
        return False
    user = get_one(name)
    query = "DELETE FROM user WHERE name = :name"
    params = {"name": name}
    curs.execute(query, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table="xuser")
