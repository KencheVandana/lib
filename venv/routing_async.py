from fastapi import APIRouter
from async_service import db_manager, Book

router = APIRouter()

# Connect to the database when the app starts
@router.on_event("startup")
async def startup():
    await db_manager.init()

# Close db_manager pool on shutdown
@router.on_event("shutdown")
async def shutdown():
    await db_manager.close()

# Route to add a book
@router.post("/books/")
async def add_book(book_id: int, book: Book):
    return await db_manager.add_book(book_id, book)

# Route to get a book by ID
@router.get("/books/{book_id}")
async def get_book(book_id: int):
    return await db_manager.get_book_by_id(book_id)

# Route to update a book by ID
@router.put("/books/{book_id}")
async def update_book(book_id: int, book: Book):
    return await db_manager.update_book_by_id(book_id, book)

# Route to delete a book by ID
@router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    return await db_manager.delete_book_by_id(book_id)

# Route to display all books
@router.get("/books/")
async def display_books():
    return await db_manager.display_all_books()



