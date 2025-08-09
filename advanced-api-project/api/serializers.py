from .models import Author, Book
from rest_framework import serializers

class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'



class BookSerializers(serializers.ModelSerializer):
    authors = AuthorSerializers(many=True, read_only=True)
    class Meta:
        model = Book
        fields = '__all__'