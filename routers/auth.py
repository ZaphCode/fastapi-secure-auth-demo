from fastapi import APIRouter, Body, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from auth.jwt import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from datetime import timedelta
from schemas.forms import LoginForm

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login",)
async def login_user(
    request: Request, 
    form_data: LoginForm = Body(..., examples=LoginForm.get_examples()), 
    Auth: AuthJWT = Depends()
):
    if form_data.email != 'test@test.com' and form_data.password != 'test1234':
        raise HTTPException(detail='Invalid credentials', status_code=400)
    access_token = Auth.create_access_token(subject='abcd-1234', expires_time=timedelta(seconds=30))
    refresh_token = Auth.create_refresh_token(subject='abcd-1234', expires_time=timedelta(minutes=5))
    Auth.set_access_cookies(access_token, max_age=30)
    Auth.set_refresh_cookies(refresh_token, max_age=300)
    return {"status": "success"}


@router.post('/refresh')
def refresh(Auth: AuthJWT = Depends()):
    Auth.jwt_refresh_token_required()
    current_user_id = Auth.get_jwt_subject()
    new_access_token = Auth.create_access_token(subject=current_user_id, expires_time=timedelta(seconds=30))
    # Set the JWT and CSRF double submit cookies in the response
    Auth.set_access_cookies(new_access_token, max_age=30)
    return {"msg": "The token has been refresh"}


@router.delete('/logout')
def logout(Auth: AuthJWT = Depends()): 
    Auth.jwt_required()
    Auth.unset_access_cookies()
    Auth.unset_refresh_cookies()
    return {"msg": "Successfully logout"}


@router.get('/protected')
def protected(request: Request, Auth: AuthJWT = Depends()):
    # try:
    #     Auth.jwt_required()
    # except AuthJWTException:
    #     print('a')
    #     return RedirectResponse(url='/login', status_code=302)
    Auth.jwt_required()
    current_user_id = Auth.get_jwt_subject()
    return templates.TemplateResponse("protected.html", {"request": request, "id": current_user_id})
