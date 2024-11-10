from django import forms
from .models import Posts, Comments, Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Campos que você quer exibir

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


class ProfileEditForm(forms.ModelForm):
    # Campos de edição do perfil
    username = forms.CharField(max_length=150, disabled=True)  # 'username' somente leitura
    first_name = forms.CharField(max_length=30, required=False)  # Campos editáveis
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)  # 'email' editável

    class Meta:
        model = Profile  # Modelo relacionado ao perfil
        fields = ['bio', 'date_of_birth', 'favorite_song']  # Campos do perfil
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})  # Isso faz com que o campo se torne um seletor de data
        }

    def __init__(self, *args, **kwargs):
        # Passando o usuário atual para o formulário para garantir que o campo 'username' esteja bloqueado
        self.user = kwargs.pop('user')
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        # Preenchendo os campos com os dados do usuário
        self.fields['username'].initial = self.user.username
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email

        # Preenchendo os campos do perfil (bio, data de nascimento, música favorita)
        try:
            profile = self.user.profile  # Acessando o perfil do usuário
            self.fields['bio'].initial = profile.bio
            self.fields['date_of_birth'].initial = profile.date_of_birth
            self.fields['favorite_song'].initial = profile.favorite_song
        except Profile.DoesNotExist:
            # Caso o perfil não exista (o que não deveria acontecer normalmente)
            pass

    def save(self, commit=True):
        # Salvando as alterações tanto no modelo Profile quanto no modelo User
        user = self.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Salvar as mudanças no modelo User
        if commit:
            user.save()

        # Agora salvar as alterações no Profile
        profile, created = Profile.objects.get_or_create(user=self.user)  # Tenta obter o perfil ou cria um novo
        profile.bio = self.cleaned_data['bio']
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.favorite_song = self.cleaned_data['favorite_song']

        if commit:
            profile.save()

        return profile




class ProfilePictureForm(forms.ModelForm):
    cropped_image = forms.ImageField(required=True, label="Escolha a imagem cortada")

    class Meta:
        model = Profile
        fields = ['profile_picture']  
        

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label="Pesquisar")