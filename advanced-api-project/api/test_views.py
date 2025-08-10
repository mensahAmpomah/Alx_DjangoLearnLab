from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
# from rest_framework.test import APIClient

from rest_framework.test import APITestCase

from .models import Book  # assumes Book model exists with fields: title, author, publication_year

User = get_user_model()


def create_book(**kwargs):
    """Helper to create Book objects with defaults."""
    defaults = {
        "title": "Default Title",
        "author": "Default Author",
        "publication_year": datetime.now().year,
    }
    defaults.update(kwargs)
    return Book.objects.create(**defaults)


class BookAPITests(TestCase):
    """Tests for Book API endpoints including CRUD, filtering, searching, ordering, and permissions."""

    def setUp(self):
        self.client = APITestCase()

        # Create users: one normal user who will be used to authenticate
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create several books to use in list/filter/search/order tests
        self.book1 = create_book(title="Learn Python", author="Alice", publication_year=2019)
        self.book2 = create_book(title="Advanced Django", author="Bob", publication_year=2021)
        self.book3 = create_book(title="Python Tips", author="Alice", publication_year=2023)

        # URL names (these must match your urls.py)
        self.list_url = reverse("book-list")          # /books/
        self.create_url = reverse("book-create")      # /books/create/
        # detail/update/delete will be built with pk in each test

    # ---------- List / Read (unauthenticated allowed) ----------
    def test_list_books_public_access(self):
        """GET /books/ should be accessible without authentication and return all books."""
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Expect at least the three created books
        titles = [b["title"] for b in res.json()]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertIn(self.book3.title, titles)

    def test_retrieve_book_detail_public_access(self):
        """GET /books/<pk>/ should be accessible without authentication."""
        url = reverse("book-detail", args=[self.book2.pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data["title"], self.book2.title)
        self.assertEqual(data["author"], self.book2.author)

    # ---------- Create (authenticated required) ----------
    def test_create_book_requires_authentication(self):
        """POST /books/create/ should be blocked for unauthenticated users."""
        payload = {"title": "New Book", "author": "Jane", "publication_year": datetime.now().year}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book and data is saved correctly."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "New Book", "author": "Jane", "publication_year": 2020}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.json()
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["author"], payload["author"])
        self.assertEqual(int(data["publication_year"]), payload["publication_year"])

    def test_create_book_future_publication_year_fails(self):
        """Creating a book with a future publication_year should return HTTP 400."""
        self.client.force_authenticate(user=self.user)
        next_year = datetime.now().year + 1
        payload = {"title": "Future Book", "author": "Time Traveler", "publication_year": next_year}
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # ensure validation error about publication_year is present
        self.assertTrue("publication_year" in res.json() or "Publication year" in str(res.json()))

    # ---------- Update (authenticated required) ----------
    def test_update_book_requires_authentication(self):
        """PUT/PATCH /books/update/<pk>/ blocked for unauthenticated users."""
        url = reverse("book-update", args=[self.book1.pk])
        payload = {"title": "Hacked Title"}
        res = self.client.patch(url, payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """Authenticated user can update a book."""
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", args=[self.book1.pk])
        payload = {"title": "Learn Python - Updated"}
        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, payload["title"])

    # ---------- Delete (authenticated required) ----------
    def test_delete_book_requires_authentication(self):
        """DELETE /books/delete/<pk>/ blocked for unauthenticated users."""
        url = reverse("book-delete", args=[self.book2.pk])
        res = self.client.delete(url)
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book."""
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete", args=[self.book2.pk])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book2.pk)

    # ---------- Filtering ----------
    def test_filter_by_author(self):
        """Filtering ?author=Alice returns only books by Alice."""
        res = self.client.get(self.list_url, {"author": "Alice"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertTrue(all(item["author"] == "Alice" for item in data))
        self.assertGreaterEqual(len(data), 1)

    def test_filter_by_publication_year(self):
        """Filtering ?publication_year=2021 returns the expected book(s)."""
        res = self.client.get(self.list_url, {"publication_year": 2021})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertTrue(all(int(item["publication_year"]) == 2021 for item in data))

    # ---------- Search ----------
    def test_search_by_title(self):
        """Search ?search=python should return books whose title or author match 'python' (case-insensitive)."""
        res = self.client.get(self.list_url, {"search": "python"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        # titles should include both "Learn Python" and "Python Tips"
        titles = [item["title"].lower() for item in data]
        self.assertIn("learn python", titles)
        self.assertIn("python tips", titles)

    # ---------- Ordering ----------
    def test_ordering_by_publication_year_descending(self):
        """Ordering ?ordering=-publication_year should return results with newest first."""
        res = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        years = [int(item["publication_year"]) for item in data]
        # Ensure list is sorted in non-increasing order
        self.assertEqual(years, sorted(years, reverse=True))

    # ---------- Combined queries ----------
    def test_search_and_order_combined(self):
        """You can combine search and ordering query params."""
        res = self.client.get(self.list_url, {"search": "python", "ordering": "-publication_year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        # All returned items should be related to 'python'
        self.assertTrue(all("python" in item["title"].lower() or "python" in item["author"].lower() for item in data))
        years = [int(item["publication_year"]) for item in data]
        self.assertEqual(years, sorted(years, reverse=True))

    # ---------- Edge / extra checks ----------
    def test_detail_not_found_returns_404(self):
        """Requesting a non-existent book returns 404."""
        url = reverse("book-detail", args=[99999])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)