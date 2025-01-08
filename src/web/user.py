import os
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service
from error import Missing, Duplicate

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")

# This dependency makes a post to "/user/token"
# (from a form containing a username and password)
# and returns an access token.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# This endpoint is directed to by any call that has the
# oauth2_dep() dependency:
@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get username and password from OAuth form,
    return access token"""
    user = service.auth_user(form_data.name, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.name}, expires=expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Return the current access token"""
    return {"token": token}


@router.get("/")
def get_all() -> list[User]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> User:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/", status_code=201)
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/")
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


"""
Authentication Steps

Here's a review of that heap of code from the previous sections:

If an endpoint has the dependency oauth2_dep() (in web/user.py), a form containing username and password fields is generated and sent to the client.

After the client fills out and submits this form, the username and password (hashed with the same algorithm as those already stored in the local database) are matched against the local database.

If a match occurs, an access token is generated (in JWT format) and returned.

This access token is passed back to the web server as an Authorization HTTP header in subsequent requests. This JWT token is decoded on the local server to the username and other details. This name does not need to be looked up in the database again.

The username is authenticated, and the server can do whatever it likes with it.

What can the server do with this hard-won authentication information? The server can do the following:

Generate metrics (this user, this endpoint, this time) to help study what's being viewed, by whom, for how long, and so on.

Save user-specific information.

JWT

This section contains some details on the JWT. You really don't need them to use all the earlier code in this chapter, but if you're a little curious…

A JWT is an encoding scheme, not an authentication method. The low-level details are defined in RFC 7519. It can be used to convey authentication information for OAuth2 (and other methods), and I'll show that here.

A JWT is a readable string with three dot-separated sections:

Header: Encryption algorithm used, and token type

Payload: …​

Signature: …​

Each section consists of a JSON string, encoded in Base 64 URL format. Here's an example (which has been split at the dots to fit on this page):

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
As a plain ASCII string that's also safe to use in URLs, it can be passed to web servers as part of the URL, a query parameter, HTTP header, cookie, and so on.

JWT avoids a database lookup, but this also means that you can't detect a revoked authorization directly.
"""
