"""Pydantic request/response schemas."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Orientation = Literal["both", "horizontal", "vertical"]


# --- Auth -----------------------------------------------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Word lists / templates ----------------------------------------------

class WordItem(BaseModel):
    text: str = Field(min_length=1, max_length=64)
    orientation: Orientation = "both"


class WordListCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    items: list[WordItem] = Field(default_factory=list)
    gap: int = Field(default=1, ge=0, le=5)
    is_template: bool = False


class WordListUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    items: list[WordItem] | None = None
    gap: int | None = Field(default=None, ge=0, le=5)
    is_template: bool | None = None


class WordListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    items: list[WordItem]
    gap: int
    is_template: bool
    created_at: datetime
    updated_at: datetime


# --- Favorites ------------------------------------------------------------

class FavoriteCreate(BaseModel):
    name: str | None = Field(default=None, max_length=120)
    list_id: int | None = None
    grid: dict


class FavoriteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str | None
    list_id: int | None
    grid: dict
    created_at: datetime
