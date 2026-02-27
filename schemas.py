from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    bio: str | None = None
    avatar_url: str | None = None

# =========================
# USER SCHEMAS
# =========================


class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =========================
# TOKEN SCHEMAS
# =========================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# =========================
# POST SCHEMAS
# =========================

class PostCreate(BaseModel):
    caption: str


class PostUpdate(BaseModel):
    caption: Optional[str] = None


class PostOut(BaseModel):
    id: int
    author_id: int
    caption: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =========================
# MEDIA SCHEMAS
# =========================

class MediaCreate(BaseModel):
    post_id: int   # 👈 ОСЫ ЖОЛДЫ ҚОС
    url: str
    mime_type: str
    width: Optional[int] = 1080
    height: Optional[int] = 1080
    order_idx: Optional[int] = 1

class MediaOut(BaseModel):
    id: int
    post_id: int
    url: str
    mime_type: str
    width: Optional[int] = None
    height: Optional[int] = None
    order_idx: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MediaUpdate(BaseModel):
    url: Optional[str] = None
    description: Optional[str] = None

# =========================
# COMMENT SCHEMAS
# =========================

class CommentCreate(BaseModel):
    post_id: int
    text: str


class CommentOut(BaseModel):
    id: int
    post_id: int
    author_id: int
    text: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =========================
# LIKE SCHEMAS
# =========================

class LikeOut(BaseModel):
    user_id: int
    post_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =========================
# FOLLOW SCHEMAS
# =========================

class FollowCreate(BaseModel):
    followee_id: int


class FollowOut(BaseModel):
    follower_id: int
    followee_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
# =========================
# COMMENT UPDATE SCHEMA
# =========================

class CommentUpdate(BaseModel):
    text: Optional[str] = None


from pydantic import BaseModel

class RefreshTokenCreate(BaseModel):
    user_id: int
