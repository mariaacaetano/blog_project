from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BlogUser

class BlogUserAdmin(UserAdmin):
    model = BlogUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    # Definindo os campos do formulário
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'birth_date')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'is_staff', 'is_active'),
        }),
    )
    
    # Para redefinir a maneira como as senhas são configuradas
    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(BlogUser, BlogUserAdmin)
