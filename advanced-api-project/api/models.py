from django.db import models

# Author models below

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Book models below
class Book(models.Model):
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="authors")

    def __str__(self):
        return self.title
