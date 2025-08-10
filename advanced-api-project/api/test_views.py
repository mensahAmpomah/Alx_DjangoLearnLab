from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data and client"""
        # Create test users
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='user@example.com',
            password='testpass123'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
            published_date='1925-04-10',
            isbn='9780743273565',
            page_count=180,
            language='en'
        )
        self.book2 = Book.objects.create(
            title='To Kill a Mockingbird',
            author='Harper Lee',
            published_date='1960-07-11',
            isbn='9780061120084',
            page_count=281,
            language='en'
        )
        self.book3 = Book.objects.create(
            title='1984',
            author='George Orwell',
            published_date='1949-06-08',
            isbn='9780451524935',
            page_count=328,
            language='en'
        )
        
        # Set up API client
        self.client = APIClient()

    def test_list_books(self):
        """Test retrieving a list of books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # Assuming pagination

    def test_retrieve_single_book(self):
        """Test retrieving a single book"""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        """Test creating a book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'isbn': '1234567890123',
            'page_count': 100,
            'language': 'en'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.latest('id').title, 'New Book')

    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication"""
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'isbn': '1234567890123',
            'page_count': 100,
            'language': 'en'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Test updating a book as authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', args=[self.book1.id])
        data = {
            'title': 'Updated Title',
            'author': self.book1.author,
            'published_date': self.book1.published_date,
            'isbn': self.book1.isbn,
            'page_count': self.book1.page_count,
            'language': self.book1.language
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        url = reverse('book-list')
        response = self.client.get(url, {'author': 'Harper Lee'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'To Kill a Mockingbird')

    def test_search_books_by_title(self):
        """Test searching books by title"""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Gatsby'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'The Great Gatsby')

    def test_delete_book_admin(self):
        """Test deleting a book as admin"""
        self.client.force_authenticate(user=self.admin)
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_non_admin(self):
        """Test deleting a book as non-admin user"""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)