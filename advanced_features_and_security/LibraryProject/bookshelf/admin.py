from django.contrib import admin
from .models import Book
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin 
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','publication_year')
    list_filter = ('author','publication_year')
    search_fields = ('title','author')



# Register your models here.

class CustomerUserAdmin(UserAdmin):
    pass

admin.site.register(CustomUser,CustomerUserAdmin)