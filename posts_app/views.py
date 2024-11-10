import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render
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
from .models import Posts, Comments, Profile, Like, CommentLike, Follow
from .forms import PostsForm, UserProfileForm, ProfileForm, ProfilePictureForm, ProfileEditForm, CommentsForm, CustomUserCreationForm


# Create your views here.# views.py
from django.shortcuts import render
from .models import Posts, PostTag

def post_list(request):
    template_name = 'post_list.html'  # template
    posts = Posts.objects.all()  # consulta com todas as postagens
    tags = PostTag.objects.all()  # consulta com todas as tags
    context = {  # cria o contexto para passar para o template
        'posts': posts,
        'tags': tags,  # adiciona as tags ao contexto
    }
    return render(request, template_name, context)  # renderiza o template com o contexto


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
def profile_view(request, username=None):
    if username is None:
        username = request.user.username
    
    user = get_object_or_404(User, username=username)
    profile = user.profile  # Obtendo o perfil associado ao usuário
    posts = Posts.objects.filter(author=user)  # Obtendo posts feitos pelo usuário
    comments = Comments.objects.filter(author=user)

    # Obtendo seguidores e seguidos
    followers = user.profile.followers.all()  # Acessando a lista de seguidores
    following = user.profile.following.all()  # Acessando a lista de pessoas que o usuário está seguindo
    
    followers_count = user.followers.count()  # Seguindo a relação "followers"
    following_count = user.following.count()  # Seguindo a relação "following"

    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
        'posts': posts,
        'comments': comments,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,  # Adicionando contagem de seguidores
        'following_count': following_count   # Adicionando contagem de seguidos
    })



@login_required
def edit_profile_picture(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            # Use a imagem cortada para atualizar o campo profile_picture do modelo
            profile.profile_picture = form.cleaned_data['cropped_image']
            profile.save()
            return redirect('profile')  # Redireciona para a página de perfil após salvar
    else:
        form = ProfilePictureForm()

    return render(request, 'edit_profile_picture.html', {'form': form})

@login_required
def edit_profile_info(request):
    profile = get_object_or_404(Profile, user=request.user)  # Obtém o perfil existente do usuário
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)  # Passa a instância do perfil
        if form.is_valid():
            form.save()  # Atualiza o perfil existente
            return redirect('profile')  # Redireciona após a atualização
    else:
        form = ProfileForm(instance=profile)  # Carrega o formulário com os dados atuais do perfil
    
    return render(request, 'edit_profile_info.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    # Verifica se o usuário já curtiu este post
    if not Like.objects.filter(user=request.user, post=post).exists():
        # Cria uma nova curtida
        Like.objects.create(user=request.user, post=post)

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
    # Obtém o perfil do autor com base no 'username' fornecido na URL
    author = get_object_or_404(User, username=username)
    author_profile = author.profile

    # Verifica se o usuário logado está seguindo o autor
    is_following = request.user.profile.following.filter(id=author.id).exists()

    # Obtém as publicações feitas pelo autor
    posts = Posts.objects.filter(author=author)
    post_count = posts.count()
    comments = Comments.objects.filter(author=author)

    # Passa para o template as informações do autor e se está seguindo ou não
    return render(request, 'author_profile.html', {
        'author': author,
        'author_profile': author_profile,
        'is_following': is_following,
        'posts': posts,
        'post_count': post_count,
        'comments':comments
    })


    
@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = request.user.profile

    # Seguir ou deixar de seguir
    if user_to_follow in profile.following.all():
        profile.following.remove(user_to_follow)
    else:
        profile.following.add(user_to_follow)

    return redirect('profile', username=user_to_follow.username)



@login_required
def unfollow_user(request, username):
    # Obtém o usuário a ser deixado de seguir
    user_to_unfollow = get_object_or_404(User, username=username)

    # Verificar se o usuário logado está tentando deixar de seguir alguém que não é ele mesmo
    if request.user != user_to_unfollow:
        # Encontrar a relação de follow entre o usuário logado e o usuário a ser deixado de seguir
        follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow).first()
        
        # Se existir essa relação, deletar
        if follow:
            follow.delete()  # Remove o seguimento

    # Redireciona de volta para o perfil do autor
    return redirect('author_profile', username=username)
