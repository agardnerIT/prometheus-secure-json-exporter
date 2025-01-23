import secrets
from typing import Annotated

from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

@app.get("/", response_class=JSONResponse)
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"agardnerit"
    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"password123"
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


    foo = {
        "my_first_metric": 25
    }
    return foo
