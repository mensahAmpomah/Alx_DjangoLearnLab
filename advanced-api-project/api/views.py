from django.shortcuts import render
from .models import Book, Author
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


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


