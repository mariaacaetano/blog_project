from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_create', views.post_create, name='post_create'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('comments/delete/<int:id>/', views.comment_delete, name='comment_delete'),
    path('post_update/<int:id>', views.post_update, name='post_update'),
    path('post_delete/<int:id>/', views.post_delete, name='post_delete'),
    path('complete_profile', views.complete_profile, name='complete_profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('ckeditor/', include('ckeditor_uploader.urls')),  
]