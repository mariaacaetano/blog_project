from django.contrib import admin
from .models import Posts, PostTag, Comments

# Register your models here.
admin.site.register(Posts)
admin.site.register(PostTag)
admin.site.register(Comments)