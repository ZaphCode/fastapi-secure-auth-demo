from fastapi_jwt_auth import AuthJWT as FapiAuthJWT
from .settings import AuthSettings

@FapiAuthJWT.load_config
def get_config():
    return AuthSettings()

AuthJWT = FapiAuthJWT