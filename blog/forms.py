from django import forms
from blog.models import Post, Comment
from django.contrib.auth.models import User
from blog.models import UserProfileInfo,Contact


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author','title','image','text')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('name','text')

        widgets = {
            'name':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }

#ACCOUNTS
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
   class Meta():
       model = UserProfileInfo
       fields = ('portfolio_site','profile_pic') 

class ContactForm(forms.ModelForm):
    class Meta():
        model = Contact
        fields = ('first_name','last_name','email','message')

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'textinputclass'}),
            'last_name':forms.TextInput(attrs={'class':'textinputclass'}),
            'message':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }