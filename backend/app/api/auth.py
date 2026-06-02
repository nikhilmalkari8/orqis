from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service, get_current_user_id
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, service: Annotated[AuthService, Depends(get_auth_service)]):
    return service.signup(body.email, body.password)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, service: Annotated[AuthService, Depends(get_auth_service)]):
    return service.login(body.email, body.password)


@router.get("/me", response_model=UserOut)
def me(
    user_id: Annotated[str, Depends(get_current_user_id)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return service.get_user(user_id)
