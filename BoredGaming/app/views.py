"""
Definition of views.
"""

from django.shortcuts import render
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
#from mailchimp import utils

MAILCHIMP_LIST_ID = ""

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
    return render(
        request, 
        'app/homepage.html',
        {
            'title': 'Welcome!',
            'year': datetime.now().year
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
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance= request.user.profile)
        return render(
            request, 
            'app/editprofile.html',
            {
                'user_form': user_form,
                'profile_form': profile_form,
                'title': 'Edit Profile',
                'year': datetime.now().year
                })


