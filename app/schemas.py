# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    summary: Optional[str] = None

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    review_text: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        orm_mode = True

class SummaryResponse(BaseModel):
    summary: str
