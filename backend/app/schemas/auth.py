from pydantic import BaseModel, EmailStr, constr, validator

from app.settings import get_settings


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class RegistrationForm(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=4)
    email: EmailStr | None

    @validator("password")
    def validate_password(cls, password):
        settings = get_settings()
        password = settings.PWD_CONTEXT.hash(password)
        return password


class RegistrationSuccess(BaseModel):
    message: str
