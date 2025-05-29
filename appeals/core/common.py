import secrets
from appeals.config.config import Config
from fastapi import (
        Depends,
        HTTPException,
        status
)
from fastapi.security import (
        HTTPBasic,
        HTTPBasicCredentials
)


class Common():
    security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(Common.security)) -> str:
    is_user = secrets.compare_digest(
        credentials.username,
        "admin"
    )
    is_pass = secrets.compare_digest(
        credentials.password,
        Config.admin_passwd
    )

    if not (is_user and is_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
