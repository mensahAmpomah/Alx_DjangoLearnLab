from django.contrib import admin
from .models import Book
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin 
from django.utils.translation import gettext_lazy as _
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','publication_year')
    list_filter = ('author','publication_year')
    search_fields = ('title','author')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)