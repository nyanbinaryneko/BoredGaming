"""
Definition of views.
"""

from django.shortcuts import render
from app.forms import MailingListForm
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .models import Lead
#from mailchimp import utils

MAILCHIMP_LIST_ID = ""

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'BoredGaming',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Want to chat? Have a great feature idea? Drop me a line!',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if(request.method == "POST"):
        add_email_to_mailing_list(request.POST['email'])
        return render(
            request,
            'app/about.html',
            {
                'title':'BoredGaming.io',
                'message':'Your favorite group finder.',
                'year':datetime.now().year,
                'form': MailingListForm,
                'success': True,
            }
        )
    else:
        return render(
            request,
            'app/about.html',
            {
                'title':'BoredGaming.io',
                'message':'Your favorite group finder.',
                'year':datetime.now().year,
                'form': MailingListForm,
            }
        )

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home') #TODO: take user to their profile page 
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

#TODO: CHECK TO SEE IF THE EMAIL IS IN THERE MORE THAN ONCE, IF SO, THROW AN ERROR MESSAGE
#THIS WORKS FOR NOW
def add_email_to_mailing_list(email):
    lead = Lead()
    lead.email_address = email
    lead.save()
