from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Certifique-se de que o CKEditor está instalado corretamente


# Modelos
class Posts(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(default="")
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey("PostTag", on_delete=models.SET_NULL, null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like', related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        
class PostTag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.tag_name
    

class Comments(models.Model):
    body = RichTextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.body


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'comment')  # Impede múltiplas curtidas do mesmo usuário no mesmo comentário

    def __str__(self):
        return f"{self.user.username} liked {self.comment.body[:20]}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    favorite_song = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    temp_profile_picture = models.ImageField(upload_to='temp_profile_pics/', null=True, blank=True)  # Campo temporário
    following = models.ManyToManyField(User, related_name='profile_following')
    followers = models.ManyToManyField(User, related_name='profile_followers')

    def __str__(self):
        return self.user.username
    


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')
        
    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'
