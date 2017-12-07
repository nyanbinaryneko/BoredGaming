"""
Definition of forms.
"""

from django import forms
from django.forms.fields import EmailField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class MailingListForm(forms.Form):
   """Mailing list """
   email = forms.EmailField(required=True)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'name': 'email',
                }
            ))
    username = forms.CharField(
        max_length=30, 
        required=False, 
        help_text='Optional.',
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'username',
                }
            )
        )
    password1 = forms.CharField( 
        required=True, 
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'name': 'password1',
                }
            ),
        label='Password',
        )
    password2 = forms.CharField( 
        required=True,
        widget=forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'name': 'password2',
                }
            ),
        label='Confirm Password',
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        
