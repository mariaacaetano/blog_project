from django import forms
from .models import Posts, Comments
from django.contrib.auth import get_user_model

User = get_user_model()

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'description', 'image','tag']

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
              field.widget.attrs['class'] = 'form-control'
              
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']  # Adiciona apenas o campo de corpo do comentário

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # Adiciona a classe de bootstrap



