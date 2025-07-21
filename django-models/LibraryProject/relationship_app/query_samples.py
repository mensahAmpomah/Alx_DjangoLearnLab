from relationship_app.models import Library

library = Library.objects.get(name="Accra Library")
books = library.books.all()
for book in books:
    print(book.title)

from relationship_app.models import Book

book1 = Book.objects.get(title="Django Basics")
book2 = Book.objects.get(title="Advanced Django")

library.books.set([book1, book2])