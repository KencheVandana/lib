from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from custom_logging import setup_logging

# Setup logging
logger = setup_logging()

# Load environment variables
load_dotenv()

class Book(BaseModel):
    title: str
    author: str
    published_date: Optional[str] = None
    genre: Optional[str] = None

class DatabaseManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('Host'),  # Make sure this is 'localhost'
                user=os.getenv('User'),
                password=os.getenv('Password'),
                database=os.getenv('Database')
            )
            if not self.connection.is_connected():
                logger.error("Database connection failed.")
                raise HTTPException(status_code=500, detail="Database connection failed.")
            logger.info("Database connection established.")
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

    def create_table(self):
        with self.connection.cursor() as cursor:
            query = """
            CREATE TABLE IF NOT EXISTS books (
                id INT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                published_date DATE,
                genre VARCHAR(100)
            );
            """
            cursor.execute(query)
            self.connection.commit()
            logger.info("Books table created or already exists.")

    def add_book(self, book_id: int, book: Book):
        with self.connection.cursor() as cursor:
            query = "INSERT INTO books (id, title, author, published_date, genre) VALUES (%s, %s, %s, %s, %s)"
            values = (book_id, book.title, book.author, book.published_date, book.genre)
            cursor.execute(query, values)
            self.connection.commit()
            logger.info(f"Book added: {book.title} (ID: {book_id})")
            return {"message": "Book added successfully."}

    def get_book_by_id(self, book_id: int):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM books WHERE id = %s"
            cursor.execute(query, (book_id,))
            book = cursor.fetchone()
            if book:
                logger.info(f"Book retrieved: {book[1]} (ID: {book_id})")
                return {"id": book[0], "title": book[1], "author": book[2], "published_date": book[3], "genre": book[4]}
            else:
                logger.warning(f"Book not found (ID: {book_id}).")
                raise HTTPException(status_code=404, detail="Book not found.")

    def update_book_by_id(self, book_id: int, book: Book):
        with self.connection.cursor() as cursor:
            query = """
            UPDATE books 
            SET title = %s, author = %s, published_date = %s, genre = %s 
            WHERE id = %s
            """
            values = (book.title, book.author, book.published_date, book.genre, book_id)
            cursor.execute(query, values)
            self.connection.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Book not found for update (ID: {book_id}).")
                raise HTTPException(status_code=404, detail="Book not found.")
            logger.info(f"Book updated: {book.title} (ID: {book_id})")
            return {"message": "Book updated successfully."}

    def delete_book_by_id(self, book_id: int):
        with self.connection.cursor() as cursor:
            query = "DELETE FROM books WHERE id = %s"
            cursor.execute(query, (book_id,))
            self.connection.commit()
            if cursor.rowcount == 0:
                logger.warning(f"Book not found for deletion (ID: {book_id}).")
                raise HTTPException(status_code=404, detail="Book not found.")
            logger.info(f"Book deleted (ID: {book_id})")
            return {"message": "Book deleted successfully."}

    def display_all_books(self):
        with self.connection.cursor() as cursor:
            query = "SELECT * FROM books"
            cursor.execute(query)
            books = cursor.fetchall()
            logger.info("Retrieved all books.")
            return [{"id": book[0], "title": book[1], "author": book[2], "published_date": book[3], "genre": book[4]} for book in books]

# Initialize DatabaseManager
db_manager = DatabaseManager() 
 
