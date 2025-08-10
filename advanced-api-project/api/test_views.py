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

    def test_list_books_unauthenticated(self):
        """Test that anyone can list books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_book_authenticated_with_login(self):
        """Test creating a book with session login"""
        # Login using Django's session authentication
        self.client.login(username='testuser', password='testpass123')
        
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
        
        # Cleanup
        self.client.logout()

    def test_create_book_authenticated_with_force_auth(self):
        """Test creating a book with forced authentication"""
        # Alternative method using DRF's force_authenticate
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
        
        # Cleanup
        self.client.force_authenticate(user=None)

    def test_update_book_with_login(self):
        """Test updating a book with session login"""
        self.client.login(username='testuser', password='testpass123')
        
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
        
        self.client.logout()

    def test_delete_book_admin_with_login(self):
        """Test deleting a book as admin with login"""
        self.client.login(username='admin', password='testpass123')
        
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.client.logout()

    def test_access_with_invalid_login(self):
        """Test API access with invalid credentials"""
        # Attempt to login with wrong password
        login_success = self.client.login(username='testuser', password='wrongpass')
        self.assertFalse(login_success)
        
        url = reverse('book-list')
        data = {
            'title': 'Should Fail',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'isbn': '1234567890123',
            'page_count': 100,
            'language': 'en'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_behavior(self):
        """Test that logout properly prevents access"""
        self.client.login(username='testuser', password='testpass123')
        
        # Verify logged in access
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Logout and verify access is denied
        self.client.logout()
        data = {
            'title': 'Should Fail After Logout',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'isbn': '1234567890123',
            'page_count': 100,
            'language': 'en'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)