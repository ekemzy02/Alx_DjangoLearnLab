from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class BookAdmin(admin.ModelAdmin):
 # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters for the admin interface
    list_filter = ('author', 'publication_year')
    
    # Enable search functionality
    search_fields = ('title', 'author')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'date_of_birth', 'profile_photo', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'date_of_birth', 'profile_photo', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
