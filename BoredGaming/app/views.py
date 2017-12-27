"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from app.forms import RemoveOwnedGameForm
from app.forms import RemoveLikedGameForm
from app.forms import AddOwnedGameForm
from app.models import Game
from app.forms import AddLikedGameForm
from app.forms import AddNewGameForm
from app.forms import ProfileForm
from app.forms import UserForm
from django.db.transaction import atomic
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from app.forms import MailingListForm
from app.forms import SignUpForm
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import Lead

def landing_page(request):
    """Renders the landing page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = MailingListForm(request.POST)
        if form.is_valid():
            lead = Lead()
            lead.email_address = request.POST['email']
            lead.save()
            return render(
                request,
                'app/about.html',
                {
                    'title': 'BoredGaming.io',
                    'year': datetime.now().year,
                    'thank_you': True,
                }
             )
        else:
            return render(
                request,
                'app/landingpage.html',
                {
                    'title': 'BoredGaming.io',
                    'year': datetime.now().year,
                    'form': MailingListForm,
                    'error': 'Please enter an email address.',
                 }
              )
    else:
        return render(
            request,
            'app/landingpage.html',
            {
                'title':'BoredGaming.io',
                'year':datetime.now().year,
                'form': MailingListForm,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'BoredGaming.io - Contact',
            'message':'Want to chat? Have a great feature idea? Drop me a line!',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
            request,
            'app/about.html',
            {
                'title':'BoredGaming.io - About',
                'subtitle': 'BoredGaming.io',
                'message':'Your favorite group finder.',
                'message2': ' Here are the features we\'re launching with.',
                'year':datetime.now().year
            }
        )

def signup(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = SignUpForm()
    return render(
        request,
        'app/signup.html',
       {
           'title': 'BoredGaming.io - Sign Up',
           'form': form,
           'year': datetime.now().year
       })

@login_required(login_url='/')
def home(request):
    assert isinstance(request, HttpRequest)
    add_new_game_form = AddNewGameForm()
    add_game_liked_form = AddLikedGameForm()
    add_game_owned_form = AddOwnedGameForm()
    remove_game_liked_form = RemoveLikedGameForm(request.user)
    remove_gamed_owned_form = RemoveOwnedGameForm(request.user)
    if request.method == 'POST':
        user = request.user
        error_message = ''
        if request.POST['add_liked']:
            if request.POST['game']:
                game = get_object_or_404(Game, id = request.POST['game'])
                if game in user.profile.games_liked.all():
                    error_message = 'You already like ' + game.name
                else:
                    user.profile.games_liked.add(game)
            elif request.POST['name']:
                game_tuple = Game.objects.get_or_create(name = request.POST['name']) #get_or_create returns a tuple...TIL
                user.profile.games_liked.add(game_tuple[0])
        if request.POST['add_owned']:
            if request.POST['game']:
                game = get_object_or_404(Game, id = request.POST['game'])
                if game in user.profile.games_owned.all():
                    error_message = 'You already own ' + game.name
                else:
                    user.profile.games_owned.add(game)
            elif request.POST['name']:
                game_tuple = Game.objects.get_or_create(name = request.POST['name']) #get_or_create returns a tuple...TIL
                user.profile.games_owned.add(game_tuple[0])
        if request.POST['remove_liked']:
            game = get_object_or_404(Game, id = request.POST['games_liked'])
            user.profile.games_liked.remove(game)
            user.save()
        if request.POST['remove_owned']:
            game = get_object_or_404(Game, id = request.POST['games_owned'])
            user.profile.games_owned.remove(game)
        user.save()
        return render(
            request,
            'app/homepage.html',
            {
                'title': 'Welcome!',
                'year': datetime.now().year,
                'new_game_form':  add_new_game_form,
                'add_game_liked_form': add_game_liked_form,
                'add_game_owned_form': add_game_owned_form,
                'remove_game_liked_form': remove_game_liked_form,
                'remove_game_owned_form': remove_gamed_owned_form,
                'updated': True,
                'error_message': error_message
            })
    else:
        return render(
            request,
            'app/homepage.html',
            {
                'title': 'Welcome!',
                'year': datetime.now().year,
                'new_game_form':  add_new_game_form,
                'add_game_liked_form': add_game_liked_form,
                'add_game_owned_form': add_game_owned_form,
                'remove_game_liked_form': remove_game_liked_form,
                'remove_game_owned_form': remove_gamed_owned_form
            })

@login_required(login_url='/')
@transaction.atomic
def update_profile(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(
            request,
            'app/editprofile.html',
            {
                'user_form': user_form,
                'profile_form': profile_form,
                'title': 'Edit Profile',
                'year': datetime.now().year,
                'error': 'Please fix the error below.'
             })
    elif request.method == 'POST' and request.FILES['avatar']:
        avatar = request.FILES['avatar']
        user = request.user
        user.profile.avatar = avatar
        user.save()
        return HttpResponseRedirect(reverse('update_profile'))
    else:
        user_form = UserForm(instance = request.user)
        profile_form = ProfileForm(instance = request.user.profile)
        return render(
            request,
            'app/editprofile.html',
            {
                'user_form': user_form,
                'profile_form': profile_form,
                'title': 'Edit Profile',
                'year': datetime.now().year
            })

@login_required(login_url='/')
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    return render(
        request,
        'app/userprofile.html',
        {
            'title': 'BoredGaming - ' + username,
            'year': datetime.now().year
        })

@login_required(login_url='/')
def user_index(request):
    users = User.objects.all()
    return render(
        request,
        'app/userindex.html',
        {
            'title': 'BoredGaming - Users',
            'year': datetime.now().year,
            'users': users
        })
