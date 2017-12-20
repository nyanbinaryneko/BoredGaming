"""
Definition of forms.
"""

from django import forms
from django.forms.models import ModelChoiceField
from app.models import Game
from app.models import Profile
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
    """Sign up form"""
    email = forms.EmailField(
        max_length = 254,
        help_text ='Required. Please submit a valid email address.',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'name': 'email',
                }
            ))
    username = forms.CharField(
        max_length=30, 
        required=True, 
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'username',
                }
            )
        )
    password1 = forms.CharField( 
        required=True, 
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'name': 'password1',
                }
            ),
        label='Password',
        )
    password2 = forms.CharField( 
        required=True,
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'name': 'password2',
                }
            ),
        label='Confirm Password',
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )

class UserForm(forms.ModelForm):
    email = forms.EmailField(
        max_length = 254,
        help_text='Required. Please submit valid email address.',
        required = True,
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'name': 'email',
                }
            ))
    first_name = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'first_name'
                }
            ))
    last_name = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'last_name'
                }
            ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    """Updates a Profile"""
    bio = forms.CharField(
        max_length = 10000,
        required = False,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'name': 'first_name'
                }
            ))
    hometown = forms.CharField(
        max_length = 100,
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'last_name'
                }
            ))
    rpg_class = forms.CharField(
        max_length = 100,
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'last_name'
                }
            ))

    class Meta:
        model = Profile
        fields = ('bio', 'hometown', 'rpg_class')

class AddNewGameForm(forms.ModelForm):
    """Adds a new Game"""
    name = forms.CharField(
        max_length = 100,
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'name': 'game'
                }
            ))

    class Meta:
        model = Game
        fields = ('name',)

class AddLikedGameForm(forms.ModelForm):
    game = forms.ModelChoiceField(
        queryset = Game.objects.all(),
        empty_label = "Please select a game",
        required = False,
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'name': 'existing_game_liked'
                }
            ))

    class Meta:
        model = Profile
        fields = ()
