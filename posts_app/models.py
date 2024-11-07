from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Certifique-se de que o CKEditor está instalado corretamente

# Modelos
class Posts(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(default="")
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey("PostTag", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']


class PostTag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.tag_name
    

class Comments(models.Model):
    body = RichTextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.body



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    favorite_song = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    temp_profile_picture = models.ImageField(upload_to='temp_profile_pics/', null=True, blank=True)  # Campo temporário

    def __str__(self):
        return self.user.username