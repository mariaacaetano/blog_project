import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views import generic
from .models import Posts, Comments, Profile
from .forms import PostsForm, UserProfileForm, ProfileForm, ProfileEditForm, CommentsForm


# Create your views here.
def post_list(request):
    template_name = 'post_list.html' # template
    posts = Posts.objects.all() # query com todas as postagens
    context = { # cria context para chamar no template
        'posts': posts
        }
    return render(request, template_name, context) # render

def educacao_list(request):
    template_name = 'post_pages/educacao.html'  # Nome do template
    posts = Posts.objects.filter(tag__tag_name="EDUCAÇÃO")  # Filtra postagens pela tag "EDUCAÇÃO"
    context = {  # Context para chamar no template
        'posts': posts
    }
    return render(request, template_name, context)  # Renderiza a página com o contexto

@login_required
def post_create(request):
    form = PostsForm(request.POST or None, request.FILES or None)  # Não é necessário passar 'author' aqui

    if form.is_valid():
        
        post = form.save(commit=False)  # Não salva o post imediatamente
        post.author = request.user # Define o autor como o usuário logado
        post.save()  # Salva o post
        messages.success(request, 'O post foi criado com sucesso.')
        return HttpResponseRedirect(reverse('post_list'))  # Redireciona para a lista de posts

    return render(request, 'post_form.html', {"form": form})  # Renderiza o formulário se não for um POST válido


def post_detail(request, id):
    post = get_object_or_404(Posts, id=id)  # Obtém o post
    comments = post.comments_set.all()  # Obtém todos os comentários associados ao post

    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)  # Cria o formulário com os dados do POST
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)  # Não salva imediatamente
            comment.author = request.user  # Define o autor como o usuário logado
            comment.post = post  # Associa o comentário ao post
            comment.save()  # Salva o comentário
            return redirect('post_detail', id=post.id)  # Redireciona para a página do post

    else:
        comment_form = CommentsForm()  # Cria um novo formulário vazio

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def post_update(request, id):
    post = get_object_or_404(Posts, id=id)
    
    # Verifica se o usuário logado é o autor do post
    if post.author != request.user:
        messages.error(request, 'Você não tem permissão para editar este post.')
        return redirect('post_list')  # Redireciona para a lista de posts, ou outra página

    form = PostsForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'O post foi atualizado com sucesso')
        return HttpResponseRedirect(reverse('post_detail', args=[post.id]))
    
    return render(request, 'post_form.html', {"form": form, "post": post})


@login_required
def editar_comentario(request, id):
    comentario = get_object_or_404(Comments, id=id)

    # Verifica se o usuário é o autor ou um administrador
    if request.user != comentario.author and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar este comentário.')
        return redirect('post_detail', id=comentario.post.id)

    if request.method == 'POST':
        form = CommentsForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comentário atualizado com sucesso!')
            return redirect('post_detail', id=comentario.post.id)
    else:
        form = CommentsForm(instance=comentario)

    return render(request, 'editar_comentario.html', {'form': form, 'comentario': comentario})


@login_required
def comment_delete(request, id):
    comment = get_object_or_404(Comments, id=id)

    # Verifica se o usuário é o autor do comentário ou um admin
    if request.user == comment.author or request.user.is_staff and request.method == "POST":
        comment.delete()
        messages.success(request, 'Comentário excluído com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para excluir este comentário.')

    return redirect('post_detail', id=comment.post.id)  # Redireciona para a página do post

@login_required
def post_delete(request, id):
    post = get_object_or_404(Posts, id=id)

    # Verifica se o usuário logado é o autor do post ou um superadmin
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para deletar este post.')
        return redirect('post_list')  # Redireciona para a lista de posts, ou outra página

    if request.method == 'POST':
        if post.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, post.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, post.image.path))
        
        post.delete()
        messages.success(request, 'O post foi deletado com sucesso.')
        return HttpResponseRedirect(reverse('post_list'))
    
    return render(request, 'post_delete.html', {'post': post})


def complete_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Redirecione para a página inicial ou onde desejar
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'registration/complete_profile.html', {'form': form})



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login') 
    
    def form_valid(self, form):
        # Salva o novo usuário
        user = form.save()
        # Loga o usuário automaticamente após o signup
        login(self.request, user)
        # Redireciona para a página de completar perfil
        return redirect('complete_profile')
    


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile  # Obtendo o perfil do usuário

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        # Se a imagem cortada for enviada temporariamente
        cropped_image = request.FILES.get('cropped_image')
        if cropped_image:
            # Armazene a imagem temporariamente, mas não no banco de dados
            profile.temp_profile_picture = cropped_image

        if form.is_valid():
            # Salve a edição do perfil
            form.save()

            # Se houver uma imagem cortada temporária, salve-a no banco de dados
            if profile.temp_profile_picture:
                profile.profile_picture = profile.temp_profile_picture
                profile.save()
                # Limpar a imagem temporária após salvar
                profile.temp_profile_picture.delete()

            return JsonResponse({'new_image_url': profile.profile_picture.url})

    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})