import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from routing import router
from app import app  
from service import db_manager

# Initialize TestClient with the FastAPI app
client = TestClient(app)
@pytest.fixture
def mock_db_manager():
    db_manager.add_book = MagicMock(return_value={"message": "Book added successfully."})
    db_manager.get_book_by_id = MagicMock(return_value={
        "id": 1,
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2023-01-01",
        "genre": "Fiction"
    })
    db_manager.update_book_by_id = MagicMock(return_value={"message": "Book updated successfully."})
    db_manager.delete_book_by_id = MagicMock(return_value={"message": "Book deleted successfully."})
    db_manager.display_all_books = MagicMock(return_value=[
        {"id": 1, "title": "Test Book", "author": "Test Author", "published_date": "2023-01-01", "genre": "Fiction"},
        {"id": 2, "title": "Another Book", "author": "Another Author", "published_date": "2022-05-15", "genre": "Non-fiction"}
    ])
def test_add_book(mock_db_manager):
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2023-01-01",
        "genre": "Fiction"
    }
    response = client.post("/books/?book_id=1", json=book_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully."}

def test_get_book_by_id(mock_db_manager):
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2023-01-01",
        "genre": "Fiction"
    }

def test_update_book_by_id(mock_db_manager):
    updated_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "published_date": "2024-02-01",
        "genre": "Drama"
    }
    response = client.put("/books/1", json=updated_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Book updated successfully."}

def test_delete_book_by_id(mock_db_manager):
  
    response = client.delete("/books/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully."}

def test_display_all_books(mock_db_manager):
    response = client.get("/books/")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Test Book", "author": "Test Author", "published_date": "2023-01-01", "genre": "Fiction"},
        {"id": 2, "title": "Another Book", "author": "Another Author", "published_date": "2022-05-15", "genre": "Non-fiction"}
    ]
