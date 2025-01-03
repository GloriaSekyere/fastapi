from fastapi import APIRouter
from models.explorer import Explorer
import service.explorer as service

router = APIRouter(prefix="/explorer")


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Explorer | None:
    return service.get_one(name)


@router.post("")
@router.post("/")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.patch("")
@router.patch("/")
def modify(explorer: Explorer) -> Explorer:
    return service.modify(explorer)


@router.delete("/{name}")
def delete(name: str) -> bool:
    return service.delete(name)
