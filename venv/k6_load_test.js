import http from 'k6/http';
import { check, sleep } from 'k6';

// Test configuration
export let options = {
  stages: [
    { duration: '1m', target: 5 },  // Ramp-up to 5 virtual users (VUs)
    { duration: '2m', target: 10 }, // Ramp-up to 10 VUs over 2 minutes
    { duration: '1m', target: 10 }, // Stay at 10 VUs for 1 minute
    { duration: '30s', target: 0 }, // Ramp-down to 0 VUs
  ],
};

// Sample book data
const bookData = (id) => JSON.stringify({
  title: `K6 Load Test Book ${id}`,
  author: `K6 Author ${id}`,
  published_date: "2024-01-01",
  genre: "Fiction"
});

const updatedBookData = (id) => JSON.stringify({
  title: `Updated K6 Load Test Book ${id}`,
  author: `Updated K6 Author ${id}`,
  published_date: "2024-02-01",
  genre: "Non-fiction"
});

const params = {
  headers: {
    'Content-Type': 'application/json',
  },
};

// Define test scenario
export default function () {
  const BASE_URL = 'http://localhost:8000'; 
  const bookId = __VU;  // Unique book ID based on virtual user (VU)

  let addBookRes = http.post(`${BASE_URL}/books/?book_id=${bookId}`, bookData(bookId), params);
  check(addBookRes, { 'Book added successfully': (r) => r.status === 200 });

  let getBookRes = http.get(`${BASE_URL}/books/${bookId}`);
  check(getBookRes, { 'Book retrieved successfully': (r) => r.status === 200 });

  let updateBookRes = http.put(`${BASE_URL}/books/${bookId}`, updatedBookData(bookId), params);
  check(updateBookRes, { 'Book updated successfully': (r) => r.status === 200 });

  let deleteBookRes = http.del(`${BASE_URL}/books/${bookId}`);
  check(deleteBookRes, { 'Book deleted successfully': (r) => r.status === 200 });

  sleep(1);  
}
