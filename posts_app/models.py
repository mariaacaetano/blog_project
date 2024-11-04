from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField  # Certifique-se de que isso está correto

# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey("PostTag", on_delete=models.CASCADE, null=True)

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
    create_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, null=True)
    
    def __str__ (self):
        return self.body
    