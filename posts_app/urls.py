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
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('comentario/<int:id>/editar/', views.editar_comentario, name='editar_comentario'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('ckeditor/', include('ckeditor_uploader.urls')),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('search/', views.search, name='search'),
    
    path('complete_profile', views.complete_profile, name='complete_profile'),
    path('profile/edit/info/', views.edit_profile_info, name='edit_profile_info'),
    path('profile/edit/picture/', views.edit_profile_picture, name='edit_profile_picture'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('author_profile/<str:username>/', views.author_profile, name='author_profile'),

    path('ciencia/', views.pages_ciencia, name='pages_ciencia'),
    path('cultura/', views.pages_cultura, name='pages_cultura'),
    path('design/', views.pages_design, name='pages_design'),
    path('educacao/', views.pages_educacao, name='pages_educacao'),
    path('entretenimento/', views.pages_entretenimento, name='pages_entretenimento'),
    path('politica/', views.pages_politica, name='pages_politica'),
    path('saude/', views.pages_saude, name='pages_saude'),
    path('tecnologia/', views.pages_tecnologia, name='pages_tecnologia'),
]