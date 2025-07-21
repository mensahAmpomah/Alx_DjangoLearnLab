from . models import Book, Author, Librarian, Library

books = Book.objects.filter(author=Author)     
for book in books:
     print(book.title)

book1 = Book.objects.create(title="My Word",author=Author)                                       ou",author=author)    
book2 = Book.objects.create(title="Psalms for you",author=Author)

library = Library.objects.create(name="Ketia")
library.books.set([book1,book2])

librarian = Librarian.objects.create(name="Yaw Manu",library=library)

books = Book.object.filter(author__name= "Kofi Mante")
for book in library.books.all():
    print(book.title)

library = Library.objects.get(name="Accra Library")
print(library.librarian.name)