# app/crud.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app import models, schemas

async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db: AsyncSession) -> list[models.Book]:
    result = await db.execute(select(models.Book))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int) -> models.Book:
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    return result.scalar_one_or_none()

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookUpdate) -> models.Book:
    db_book = await get_book(db, book_id)
    if not db_book:
        return None
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int) -> models.Book:
    db_book = await get_book(db, book_id)
    if not db_book:
        return None
    await db.delete(db_book)
    await db.commit()
    return db_book

async def create_review(db: AsyncSession, book_id: int, review: schemas.ReviewCreate) -> models.Review:
    db_review = models.Review(book_id=book_id, **review.dict(), user_id=1)  # Example user_id, adjust as needed
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_reviews(db: AsyncSession, book_id: int) -> list[models.Review]:
    result = await db.execute(select(models.Review).where(models.Review.book_id == book_id))
    return result.scalars().all()
