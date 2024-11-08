import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from routing_async import router
from app import app  # Assuming app.py contains the FastAPI app instance
from async_service import db_manager, Book

# Create TestClient instance
client = TestClient(app)

# Sample data for testing
book_data = {
    "title": "Test Book",
    "author": "Test Author",
    "published_date": "2023-01-01",
    "genre": "Fiction"
}

@pytest.fixture
def mock_db():
    """
    Fixture to mock database interactions with async functionality.
    This is applied before every test to ensure db_manager methods are mocked as async.
    """
    db_manager.add_book = AsyncMock(return_value={"message": "Book added successfully."})
    db_manager.get_book_by_id = AsyncMock(return_value={"id": 1, **book_data})
    db_manager.update_book_by_id = AsyncMock(return_value={"message": "Book updated successfully."})
    db_manager.delete_book_by_id = AsyncMock(return_value={"message": "Book deleted successfully."})
    db_manager.display_all_books = AsyncMock(return_value=[
        {"id": 1, **book_data},
        {"id": 2, "title": "Another Book", "author": "Another Author", "published_date": "2022-06-10", "genre": "Non-Fiction"}
    ])

def test_add_book(mock_db):
    response = client.post("/books/?book_id=1", json=book_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully."}

def test_get_book_by_id(mock_db):
   
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2023-01-01",
        "genre": "Fiction"
    }


def test_update_book(mock_db):

    updated_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "published_date": "2024-01-01",
        "genre": "Drama"
    }
    response = client.put("/books/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Book updated successfully."}


def test_delete_book(mock_db):
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully."}


def test_display_all_books(mock_db):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Test Book", "author": "Test Author", "published_date": "2023-01-01", "genre": "Fiction"},
        {"id": 2, "title": "Another Book", "author": "Another Author", "published_date": "2022-06-10", "genre": "Non-Fiction"}
    ]
