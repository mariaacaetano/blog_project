from django import forms
from django.contrib.auth.models import User
from .models import BlogUser

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label='Usuário', max_length=150)
    first_name = forms.CharField(label='Nome', max_length=30)
    last_name = forms.CharField(label='Sobrenome', max_length=30)
    email = forms.EmailField(label='Email')
    birth_date = forms.DateField(label='Data de Nascimento', widget=forms.SelectDateWidget())
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput())

    class Meta:
        model = BlogUser  # Utilize o modelo BlogUser para capturar os campos extras
        fields = ['first_name', 'last_name', 'birth_date', 'username', 'email', 'password']  # Inclua todos os campos relevantes

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            raise forms.ValidationError("O nome de usuário deve ter pelo menos 4 caracteres.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")
        
        return cleaned_data
