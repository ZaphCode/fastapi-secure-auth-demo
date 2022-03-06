from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from routers.auth import router as auth_router


app = FastAPI(version=1.0, title='Secure Auth testing')

#* Set static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

#* Set custom exception handlers
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


#* Add routers
app.include_router(router=auth_router)