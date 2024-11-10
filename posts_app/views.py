import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views import generic
from django.db.models import Q
from .models import Posts, Comments, Profile, Like, CommentLike, Follow
from .forms import PostsForm, UserProfileForm, ProfilePictureForm, ProfileEditForm, CommentsForm, CustomUserCreationForm, SearchForm
# Create your views here.# views.py
from django.shortcuts import render
from .models import Posts, PostTag
from django.core.paginator import Paginator

def post_list(request):
    template_name = 'post_list.html'  # Template
    posts = Posts.objects.all()  # Consulta com todas as postagens
    tags = PostTag.objects.all()  # Consulta com todas as tags

    # Paginação
    paginator = Paginator(posts, 15)  # Exibe 15 posts por página
    page_number = request.GET.get('page')  # Obtém o número da página atual
    page_obj = paginator.get_page(page_number)  # Obtém a página solicitada

    context = {  # Cria o contexto para passar para o template
        'posts': page_obj,  # Passa apenas a página atual
        'tags': tags,  # Adiciona as tags ao contexto
    }
    
    return render(request, template_name, context)  # Renderiza o template com o contexto

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
    is_liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False  # Verifica curtida

    # Processamento do formulário de comentários
    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', id=post.id)

    else:
        comment_form = CommentsForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked  # Passa o estado da curtida
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

    # Se a requisição for do tipo POST
    if request.method == 'POST':
        # Remove a imagem associada ao post (se houver)
        if post.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, post.image.path)):
            os.remove(os.path.join(settings.MEDIA_ROOT, post.image.path))
        
        post.delete()

        # Se a requisição for AJAX, retorna uma resposta JSON
        if request.is_ajax():
            return JsonResponse({'success': True})

        # Caso contrário, mostra a mensagem de sucesso e redireciona para a lista de posts
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
    return render(request, 'complete_profile.html', {'form': form})




class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm  # Use o formulário personalizado
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('complete_profile')


@login_required
def profile_view(request, username):
    username = request.user.username
    user = User.objects.get(username=username)
    profile = user.profile
    followers = user.profile.followers.all()  # Usuários que seguem este perfil
    following = user.profile.following.all()  # Usuários que este perfil segue

    posts = user.posts.all()  # Exemplo de como obter as postagens
    comments = user.comments.all()  # Exemplo de como obter os comentários

    followers_count = followers.count()
    following_count = following.count()

    context = {
        'profile': profile,
        'user': user,
        'posts': posts,
        'comments': comments,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count,
    }

    return render(request, 'profile.html', context)



@login_required
def edit_profile_picture(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            # Use a imagem cortada para atualizar o campo profile_picture do modelo
            profile.profile_picture = form.cleaned_data['cropped_image']
            profile.save()
            return redirect('profile', username=request.user.username)  # Redireciona para a página de perfil após salvar
    else:
        form = ProfilePictureForm()

    return render(request, 'edit_profile_picture.html', {'form': form})



@login_required
def edit_profile_info(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()  # Salvando as alterações no formulário
            return redirect('profile', username=request.user.username)  # Redireciona para o perfil após salvar
    else:
        form = ProfileEditForm(user=request.user)  # Criando o formulário e passando o usuário logado

    return render(request, 'edit_profile_info.html', {'form': form})  # Renderizando a página com o formulário

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    if request.user.is_authenticated:
        # Verifica se o usuário já curtiu o post
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # Descurte
        else:
            post.likes.add(request.user)  # Curte
    return redirect('post_detail', id=post.id) 


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    # Verifica se o usuário já curtiu este comentário
    if not CommentLike.objects.filter(user=request.user, comment=comment).exists():
        # Cria uma nova curtida
        CommentLike.objects.create(user=request.user, comment=comment)

    return redirect('post_detail', id=comment.post.id)



def author_profile(request, username):
    author = get_object_or_404(User, username=username)
    author_profile = author.profile

    # Verifica se o usuário logado está seguindo o autor
    is_following = request.user.profile.following.filter(id=author.id).exists()

    # Obtém as publicações e comentários feitos pelo autor
    posts = Posts.objects.filter(author=author)
    post_count = posts.count()
    comments = Comments.objects.filter(author=author)

    # Obtém a lista de seguidores e seguidos do autor
    followers = author_profile.followers.all()
    following = author_profile.following.all()
    
    followers_count = followers.count()
    following_count = following.count()

    # Debug: Verifique se os seguidores estão sendo carregados corretamente
    print("Followers:", followers)
    print("Following:", following)

    # Passa para o template as informações do autor
    return render(request, 'author_profile.html', {
        'author': author,
        'author_profile': author_profile,
        'is_following': is_following,
        'posts': posts,
        'post_count': post_count,
        'comments': comments,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count
    })


@login_required
def follow_user(request, username):
    author = get_object_or_404(User, username=username)  # Obtém o autor do perfil
    if author == request.user:  # Não pode seguir a si mesmo
        messages.error(request, 'Não pode seguir a si mesmo.')
        return redirect('author_profile', username=username)  # Redireciona de volta para o perfil do autor

    profile = request.user.profile
    if author in profile.following.all():
        # Se já está seguindo, então desfaz o seguimento
        profile.following.remove(author)
        author.profile.followers.remove(request.user)  # Remove da lista de seguidores do autor
        messages.success(request, f'Você deixou de seguir {author.username}.')
    else:
        # Se não está seguindo, adiciona ao seguimento
        profile.following.add(author)
        author.profile.followers.add(request.user)  # Adiciona à lista de seguidores do autor
        messages.success(request, f'Agora você segue {author.username}.')

    # Atualiza os contadores (seguindo e seguidores)
    author.profile.save()  # Salva as alterações no perfil do autor
    profile.save()  # Salva as alterações no perfil do usuário logado

    return redirect('author_profile', username=username) 
    
# Função para deixar de seguir um usuário
@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    
    # Verifica se o usuário logado está tentando deixar de seguir a si mesmo
    if request.user != user_to_unfollow:
        request.user.profile.following.remove(user_to_unfollow)
        user_to_unfollow.profile.followers.remove(request.user)

    return redirect('profile', username=user_to_unfollow.username)  # Redireciona para o perfil do usuário





def search(request):
    query = request.GET.get('query', '')
    users = []
    posts = []
    
    if query:
        # Pesquisar posts (pelo título, descrição e autor)
        posts = Posts.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(author__username__icontains=query)
        )
        
        # Pesquisar usuários (pelo nome de usuário e outros campos, como o nome completo)
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    
    return render(request, 'search_results.html', {'posts': posts, 'users': users, 'query': query})


def pages_entretenimento(request):
    template_name = 'post_pages/entretenimento.html'
    entretenimento_tag = get_object_or_404(PostTag, tag_name="ENTRETENIMENTO")
    posts = Posts.objects.filter(tag=entretenimento_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)

def pages_ciencia(request):
    template_name = 'post_pages/ciencia.html'
    ciencia_tag = get_object_or_404(PostTag, tag_name="CIENCIA")
    posts = Posts.objects.filter(tag=ciencia_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)

def pages_cultura(request):
    template_name = 'post_pages/cultura.html'
    cultura_tag = get_object_or_404(PostTag, tag_name="CULTURA")
    posts = Posts.objects.filter(tag=cultura_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)

def pages_design(request):
    template_name = 'post_pages/design.html'
    design_tag = get_object_or_404(PostTag, tag_name="DESIGN")
    posts = Posts.objects.filter(tag=design_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)

def pages_educacao(request):
    template_name = 'post_pages/educacao.html'
    educacao_tag = get_object_or_404(PostTag, tag_name="EDUCACAO")
    posts = Posts.objects.filter(tag=educacao_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)

def pages_politica(request):
    template_name = 'post_pages/politica.html'
    politica_tag = get_object_or_404(PostTag, tag_name="POLITICA")
    posts = Posts.objects.filter(tag=politica_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)

def pages_saude(request):
    template_name = 'post_pages/saude.html'
    saude_tag = get_object_or_404(PostTag, tag_name="SAUDE")
    posts = Posts.objects.filter(tag=saude_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)

def pages_tecnologia(request):
    template_name = 'post_pages/tecnologia.html'
    tecnologia_tag = get_object_or_404(PostTag, tag_name="TECNOLOGIA")
    posts = Posts.objects.filter(tag=tecnologia_tag)  
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)
