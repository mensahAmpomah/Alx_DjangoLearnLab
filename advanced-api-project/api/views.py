from django.shortcuts import render
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Creating of Book Here.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# list all books
class BookListView(generics.ListAPIView):
    queryset = Book.Objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['title', 'author', 'publication_year']

    search_fields = ['title', 'author']

    ordering_fields = ['title', 'publication_year']

    ordering = ['title']

# Retrieve single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.Objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Update a Book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.Objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Delete a Book

class BookDeleteView(generics.UpdateAPIView):
    queryset = Book.Objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


