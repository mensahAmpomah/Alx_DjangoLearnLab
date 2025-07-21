from django.shortcuts import render
from .models import  Library
from django.views.generic import DetailView
# Create your views here.

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


