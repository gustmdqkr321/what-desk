from pydantic import BaseModel
from typing import List


class UserSignIn(BaseModel):
    user_id: str
    password: str


class UserInfo(BaseModel):
    user_id: str
    name: str | None = None
    email: str | None = None
    image: str | None = None


class UserForm(UserSignIn, UserInfo): ...


class HashedUser(UserInfo):
    user_id: str
    hashed_password: str | None = None


class UserExternalMap(BaseModel):
    external_id: str
    provider: str
    user_id: str


class TokenResult(BaseModel):
    user: UserInfo
    access_token: str


class CommentForm(BaseModel):
    post_id: int
    content: str


class Comment(CommentForm):
    comment_id: int
    author_id: str


class BasePost(BaseModel):
    title: str
    category: str


class PostForm(BasePost):
    content: str


class PostPreview(BasePost):
    author_id: str
    post_id: int
    like_count: int
    view_count: int


class Post(PostPreview):
    content: str
    comments: List[Comment]


class Image(BaseModel):
    image_id: str
    filename: str
