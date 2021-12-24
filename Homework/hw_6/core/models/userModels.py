from pydantic import BaseModel


class RegistrationModel(BaseModel):
    login: str
    password: str


class AuthorizationModel(BaseModel):
    login: str
    password: str


class UserModel(BaseModel):
    id: str
    login: str
    follower: int
    follow: int
