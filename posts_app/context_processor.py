# myapp/context_processors.py
from .models import PostTag

def tag_list(request):
    tags = PostTag.objects.all()  # Recupera todas as tags
    return {'tags': tags}  # Retorna as tags no contexto global
