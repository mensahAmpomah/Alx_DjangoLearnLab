from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Article, Book
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'bookshelf/article_list.html', {'articles': articles})

@permission_required('bookshelf.can_create', raise_exception=True)
def article_create(request):
    # Logic for creating article
    return render(request, 'bookshelf/article_create.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Logic for editing article
    return render(request, 'bookshelf/article_edit.html', {'article': article})

@permission_required('bookshelf.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # Logic for deleting article
    return render(request, 'bookshelf/article_delete.html', {'article': article})


def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Securely handle form data
            return redirect('book_list')  # or wherever you want to redirect
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})