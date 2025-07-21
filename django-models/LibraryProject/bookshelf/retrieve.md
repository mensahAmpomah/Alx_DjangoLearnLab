# Retrieve the book
book = Book.objects.get("1984")

book.title
# Output : '1984'

book.author 
# Output : 'George Orwell'

book.publication_year
# Output : 1949