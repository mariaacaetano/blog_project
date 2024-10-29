from django.contrib import admin
from .models import Posts, PostTag

# Register your models here.
admin.site.register(Posts)
admin.site.register(PostTag)