from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_create', views.post_create, name='post_create'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('comments/delete/<int:id>/', views.comment_delete, name='comment_delete'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/<int:id>/like/', views.like_post, name='like_post'),  # Nova rota para curtir
    path('post_update/<int:id>', views.post_update, name='post_update'),
    path('post_delete/<int:id>/', views.post_delete, name='post_delete'),
    path('complete_profile', views.complete_profile, name='complete_profile'),
    path('profile/', views.profile_view, name='profile'),  
    path('perfil/<str:username>/', views.author_profile, name='author-profile'),
    path('profile/edit/info/', views.edit_profile_info, name='edit_profile_info'),
    path('profile/edit/picture/', views.edit_profile_picture, name='edit_profile_picture'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('comentario/<int:id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('ckeditor/', include('ckeditor_uploader.urls')),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('follow/<str:username>/', views.follow_user, name='follow'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow'),

]