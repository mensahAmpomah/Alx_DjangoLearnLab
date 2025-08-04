# Creating a book instance

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Output
<Book: Book object (1)>

# Retrieve the book
book = Book.objects.get("1984")

book.title
# Output : '1984'

book.author 
# Output : 'George Orwell'

book.publication_year
# Output : 1949


# Update the title

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Deleting the book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

Book.objects.all()

# Output: <QuerySet []>