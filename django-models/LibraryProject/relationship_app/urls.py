from django.urls import path
from .views import list_books, LibraryDetailView
from .views import Login_view, Logout_view

urlpatterns = [
    path('books/', list_books, name='list_books'), 
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', Login_view as_view(tempalte_name="relationship_app/login.html"), name='login'),
    path('logout/', Logout_view as_view(tempalte_name="relationship_app/logout.html"), name='logout'), 
]