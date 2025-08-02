from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book
from django.contrib.auth.models import User

class BookAPITestCase(TestCase):
    
    def setUp(self):
        # Create test user and authenticate
        self.user = User.objects.create_user(username='Power', password='power123')
        self.client = APIClient()
        self.client.login(username='Power', password='power123')
        
        # Create some books
        self.book1 = Book.objects.create(title="Angels and Demons", author="Dan Brown", publication_year=2015)
        self.book2 = Book.objects.create(title="The Hating Game", author="Sally Thorne", publication_year=2019)
        self.book3 = Book.objects.create(title="Django Rest Framework", author="Sam Brown", publication_year=2022)
    
    def test_create_book(self):
        # Test the creation of a new book
        data = {
            "title": "New Book",
            "author": "Alice Green",
            "publication_year": 2023
        }
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['author'], data['author'])
        self.assertEqual(response.data['publication_year'], data['publication_year'])
    
    def test_update_book(self):
        # Test updating a book's details
        data = {
            "title": "The Hating Game",
            "author": "Sally Thorne",
            "publication_year": 2021
        }
        response = self.client.put(f'/api/books/{self.book1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['author'], data['author'])
        self.assertEqual(response.data['publication_year'], data['publication_year'])
    
    def test_delete_book(self):
        # Test deleting a book
        response = self.client.delete(f'/api/books/{self.book2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure the book no longer exists
        response = self.client.get(f'/api/books/{self.book2.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_books(self):
        # Test listing all books
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return 3 books
    
    def test_filter_books_by_title(self):
        # Test filtering books by title
        response = self.client.get('/api/books/', {'title': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return all 3 books containing 'Django' in the title
    
    def test_search_books(self):
        # Test searching books by author
        response = self.client.get('/api/books/', {'search': 'John Doe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return only the book by 'John Doe'
    
    def test_order_books_by_publication_year(self):
        # Test ordering books by publication year
        response = self.client.get('/api/books/', {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2015)
        self.assertEqual(response.data[1]['publication_year'], 2019)
        self.assertEqual(response.data[2]['publication_year'], 2021)
    
    def test_permissions(self):
        # Test that unauthorized users cannot modify books
        self.client.logout()
        data = {
            "title": "Unauthorized Book",
            "author": "Unauthorized Author",
            "publication_year": 2023
        }
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test unauthorized deletion
        response = self.client.delete(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
