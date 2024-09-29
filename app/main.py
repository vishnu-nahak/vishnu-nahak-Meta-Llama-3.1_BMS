# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas
from .database import get_db
from .llama import generate_summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Route
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the JKTech Book Management API"}


# Book Endpoints
@app.post("/books/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.Book])
async def read_books(db: AsyncSession = Depends(get_db)):
    return await crud.get_books(db=db)

@app.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db)):
    updated_book = await crud.update_book(db=db, book_id=book_id, book=book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@app.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted_book = await crud.delete_book(db=db, book_id=book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book

# Review Endpoints
@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
async def create_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_review(db=db, book_id=book_id, review=review)

@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
async def read_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_reviews(db=db, book_id=book_id)

# Summary Endpoint
@app.get("/books/{book_id}/summary")
async def read_book_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await crud.get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Generate summary using the Llama model
    summary = await generate_summary(book.title, book.author, book.genre, book.year_published)
    
    return {
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "year_published": book.year_published,
        "summary": summary
    }


# Generate Summary Endpoint
@app.post("/generate-summary/", response_model=schemas.SummaryResponse)
async def generate_summary_endpoint(content: str):
    if not content:
        raise HTTPException(status_code=400, detail="Content is required")
    summary = await generate_summary(content)
    return {"summary": summary}

