from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucess')  # Redireciona após o cadastro
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

