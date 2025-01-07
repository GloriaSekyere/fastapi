from models.user import User
from error import Missing, Duplicate

# (no hashed password checking in this module)
_users = [
    User(name="kwijobo", hash="abc"),
    User(name="ermagerd", hash="xyz"),
]


def find(name: str) -> User | None:
    for user in _users:
        if user.name == name:
            return user
    return None


def check_missing(name: str) -> bool:
    if not find(name):
        raise Missing(msg=f"Missing user {name}")


def check_duplicate(name: str):
    if find(name):
        raise Duplicate(msg=f"Duplicate user {name}")


def get_all() -> list[User]:
    """Return all users"""
    return _users


def get_one(name: str) -> User:
    """Return one user"""
    check_missing(name)
    return find(name)


def create(user: User) -> User:
    """Add a user"""
    check_duplicate(user.name)
    return user


def modify(name: str, user: User) -> User:
    """Partially modify a user"""
    check_missing(name)
    return user


def delete(name: str) -> None:
    """Delete a user"""
    check_missing(name)
    return None
