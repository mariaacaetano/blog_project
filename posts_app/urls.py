from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('post-create', views.post_create, name='post-create'),
    path('post-detail/<int:id>/', views.post_detail, name='post-detail'),
    path('post-update/<int:id>', views.post_update, name='post-update'),
    path('post-delete/<int:id>/', views.post_delete, name='post-delete'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('ckeditor/', include('ckeditor_uploader.urls')),  
]