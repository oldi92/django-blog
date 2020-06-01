from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name' , 'last_name', 'username', 'email', 'password', )


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'text','create_date')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'textinputclass'}),
            'text' : forms.Textarea(attrs={'class':'post-content'}),
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('text',)

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'post-content'})
        }