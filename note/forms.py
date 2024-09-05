from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Note


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ModelForm to automatically handle form fields corresponding to the model’s attributes.
class NoteForm(ModelForm):
    class Meta:
        # The form is based on the Note model.
        model = Note
        fields = ['title', 'text', 'subject', 'category']
        
        #Tailwind classes (form-control) are used for styling.
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'text':forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
            'subject':forms.TextInput(attrs={'class': 'form-control'}),
            'category':forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditNoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['category','subject','title','text']

