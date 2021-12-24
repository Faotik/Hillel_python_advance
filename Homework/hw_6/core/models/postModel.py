from pydantic import BaseModel


class RawCreatePostModel(BaseModel):
    title: str
    description: str


class CreatePostModel(BaseModel):
    title: str
    description: str
    creater: str


class PostModel(BaseModel):
    id: str
    title: str
    description: str
    creater: str
    create_date: str
