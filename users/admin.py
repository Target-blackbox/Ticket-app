from django.contrib import admin
from .models import UserProfile, Manager  # Import your models

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'created_at', 'updated_at')  # Adjust fields as necessary
    search_fields = ('user__username', 'email')  # Enable search by username and email

admin.site.register(UserProfile, UserProfileAdmin)

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_manager', 'created_at')  # Adjust fields as necessary
    search_fields = ('name', 'email')  # Enable search by name and email

admin.site.register(Manager, ManagerAdmin)
