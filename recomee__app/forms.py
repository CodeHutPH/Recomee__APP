# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Remove help texts
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

         # Add custom CSS classes
        self.fields['username'].widget.attrs['class'] = 'user-input'
        self.fields['password1'].widget.attrs['class'] = 'password-input'
        self.fields['password2'].widget.attrs['class'] = 'confirm-password'

        # Placeholder labels    
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password (atleast 8 characters)'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

        # Remove labels
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    