from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BlogUser

class CustomUserAdmin(UserAdmin):
    model = BlogUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets

admin.site.register(BlogUser, CustomUserAdmin)