# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

print(f"Connecting to database at: {DATABASE_URL}")  # Debug print statement

# Create the SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
