import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy
from django.views import generic
from .models import Posts
from .forms import PostsForm


# Create your views here.
def post_list(request):
    template_name = 'post-list.html' # template
    posts = Posts.objects.all() # query com todas as postagens
    context = { # cria context para chamar no template
        'posts': posts
        }
    return render(request, template_name, context) # render


def post_create(request):
    if request.method == 'POST': # para metodo POST
        form = PostsForm(request.POST, request.FILES) # pega as informações do form
        if form.is_valid(): # se for valido
            form = form.save(commit=False)
            form.save() # salva
            
            messages.success(request, 'O post foi criado com sucesso') # mensagem quando cria o post
            return HttpResponseRedirect(reverse('post-list')) # coloquei para retornar post-list
        
    form = PostsForm() # senão carrega o formulario  
    return render(request, 'post-form.html', {"form": form}) # nesse template


def post_detail(request, id):
    template_name = 'post-detail.html' # template
    post = Posts.objects.get(id=id) # Metodo Get
    context = { # cria context para chamar no template
        'post': post
        }
    return render(request, template_name, context) # render


def post_update(request, id):
    post = get_object_or_404(Posts, id=id) # id do post
    form = PostsForm(request.POST or None, request.FILES or None, instance=post) # pega as informações do form
    if form.is_valid(): # se for valido
        form.save() # salva
        
        messages.warning(request, 'O post foi atualizado com sucesso') # mensagem quando cria o post
        return HttpResponseRedirect(reverse('post-detail', args=[post.id])) # coloquei para retornar post-list
         
    return render(request, 'post-form.html', {"form": form}) # nesse template


def post_delete(request, id):
    post = get_object_or_404(Posts, id=id)  # Garante que retorna 404 se não existir
    if request.method == 'POST':
        # Verifica se há uma imagem associada ao post e a remove
        if post.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, post.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, post.image.path))
        
        post.delete()  # Deleta o post do banco de dados
        messages.error(request, 'O post foi deletado com sucesso')
        return HttpResponseRedirect(reverse('post-list'))  # Redireciona para a lista de posts
    
    return render(request, 'post-delete.html', {'post': post})  # Renderiza a página de confirmação

class SignUpView(generic.CreateView): 
   form_class = UserCreationForm
   success_url = reverse_lazy('login') 
   template_name = 'registration/signup.html'