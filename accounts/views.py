from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.models import User

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Cria um objeto de usuário mas não salva ainda
            user.set_password(form.cleaned_data['password'])  # Define a senha
            user.save()  # Salva o usuário no banco de dados
            login(request, user)  # Faz login automático após registro
            return redirect('home')  # Redireciona para a página inicial ou outra página
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})
