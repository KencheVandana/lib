from fastapi import APIRouter
from service import db_manager, Book  

router = APIRouter()

# Route to add a book
@router.post("/books/")
def add_book(book_id: int, book: Book):
    return db_manager.add_book(book_id, book)

# Route to get a book by ID
@router.get("/books/{book_id}")
def get_book(book_id: int):
    return db_manager.get_book_by_id(book_id)

# Route to update a book by ID
@router.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    return db_manager.update_book_by_id(book_id, book)

# Route to delete a book by ID
@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    return db_manager.delete_book_by_id(book_id)

# Route to display all books
@router.get("/books/")
def display_books():
    return db_manager.display_all_books()
