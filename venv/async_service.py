from fastapi import HTTPException
from pydantic import BaseModel
import aiomysql
import os
from dotenv import load_dotenv
from custom_logging import setup_logging

# Setup logging
logger = setup_logging()

# Load environment variables
load_dotenv()

class Book(BaseModel):
    title: str
    author: str
    published_date: str = None
    genre: str = None

class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def init(self):
        """Initialize the database connection pool."""
        try:
            self.pool = await aiomysql.create_pool(
                host=os.getenv('Host'),
                user=os.getenv('User'),
                password=os.getenv('Password'),
                db=os.getenv('Database'),
                autocommit=True
            )
            logger.info("Database connection pool established.")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

    async def close(self):
        """Close the connection pool."""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("Database connection pool closed.")

    async def create_table(self):
        """Create books table if not exists."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = """
                CREATE TABLE IF NOT EXISTS books (
                    id INT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    published_date DATE,
                    genre VARCHAR(100)
                );
                """
                await cursor.execute(query)
                logger.info("Books table created or already exists.")

    async def add_book(self, book_id: int, book: Book):
        """Add a book to the database."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = "INSERT INTO books (id, title, author, published_date, genre) VALUES (%s, %s, %s, %s, %s)"
                values = (book_id, book.title, book.author, book.published_date, book.genre)
                await cursor.execute(query, values)
                logger.info(f"Book added: {book.title} (ID: {book_id})")
                return {"message": "Book added successfully."}

    async def get_book_by_id(self, book_id: int):
        """Retrieve a book by its ID."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = "SELECT * FROM books WHERE id = %s"
                await cursor.execute(query, (book_id,))
                book = await cursor.fetchone()
                if book:
                    logger.info(f"Book retrieved: {book[1]} (ID: {book_id})")
                    return {"id": book[0], "title": book[1], "author": book[2], "published_date": book[3], "genre": book[4]}
                else:
                    logger.warning(f"Book not found (ID: {book_id}).")
                    raise HTTPException(status_code=404, detail="Book not found.")

    async def update_book_by_id(self, book_id: int, book: Book):
        """Update a book by its ID."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = """
                UPDATE books 
                SET title = %s, author = %s, published_date = %s, genre = %s 
                WHERE id = %s
                """
                values = (book.title, book.author, book.published_date, book.genre, book_id)
                await cursor.execute(query, values)
                if cursor.rowcount == 0:
                    logger.warning(f"Book not found for update (ID: {book_id}).")
                    raise HTTPException(status_code=404, detail="Book not found.")
                logger.info(f"Book updated: {book.title} (ID: {book_id})")
                return {"message": "Book updated successfully."}

    async def delete_book_by_id(self, book_id: int):
        """Delete a book by its ID."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = "DELETE FROM books WHERE id = %s"
                await cursor.execute(query, (book_id,))
                if cursor.rowcount == 0:
                    logger.warning(f"Book not found for deletion (ID: {book_id}).")
                    raise HTTPException(status_code=404, detail="Book not found.")
                logger.info(f"Book deleted (ID: {book_id})")
                return {"message": "Book deleted successfully."}

    async def display_all_books(self):
        """Retrieve all books from the database."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = "SELECT * FROM books"
                await cursor.execute(query)
                books = await cursor.fetchall()
                logger.info("Retrieved all books.")
                return [{"id": book[0], "title": book[1], "author": book[2], "published_date": book[3], "genre": book[4]} for book in books]

db_manager = DatabaseManager()
