from django.contrib import admin
from .models import CustomUser, Profile

# Register the CustomUser model
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('custom_id', 'username', 'email', 'role', 'is_active', 'is_staff')  # Customize the fields to display
    list_filter = ('custom_id', 'role', 'is_staff', 'is_active')  # Add filters
    search_fields = ('custom_id', 'username', 'email')  # Add search functionality
    ordering = ('username',)  # Order by username

admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('custom_id', 'user', 'first_name', 'last_name')  # Fields to display in the list view
    search_fields = ('custom_id','user__username', 'first_name', 'last_name')  # Searchable fields
    ordering = ('last_name',)

    def custom_id(self, obj):
        return obj.user.custom_id 

admin.site.register(Profile, ProfileAdmin)