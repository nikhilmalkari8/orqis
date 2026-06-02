from app.core.exceptions import UnauthorizedError, ValidationError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse, UserOut


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def signup(self, email: str, password: str) -> TokenResponse:
        if self.user_repo.get_by_email(email):
            raise ValidationError("Email already registered")
        user = self.user_repo.create(email, hash_password(password))
        token = create_access_token(user["_key"])
        return TokenResponse(
            access_token=token,
            user=UserOut(id=user["id"], email=user["email"], display_name=user.get("display_name")),
        )

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            raise UnauthorizedError("Invalid email or password")
        token = create_access_token(user["_key"])
        return TokenResponse(
            access_token=token,
            user=UserOut(id=user["id"], email=user["email"], display_name=user.get("display_name")),
        )

    def get_user(self, user_id: str) -> UserOut:
        user = self.user_repo.get(user_id)
        if not user:
            raise UnauthorizedError("User not found")
        return UserOut(id=user["id"], email=user["email"], display_name=user.get("display_name"))
