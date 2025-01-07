import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
basic = HTTPBasic()

secret_username = "kakra"
secret_pwd = "1234"


@app.get("/auth")
def get_auth(credentials: HTTPBasicCredentials = Depends(basic)) -> dict:
    if (credentials.username == secret_username) and (
        secret_pwd == credentials.password
    ):
        return {"username": credentials.username, "password": credentials.password}
    raise HTTPException(status_code=401, detail="Wrong username or password")


if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)
