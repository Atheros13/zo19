from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from zo.forms import BootstrapAuthenticationForm
from zo.forms.signup import UserSignUpContactForm, UserHubSignUpContactForm
from zo.generic.views import GenericContactView

from datetime import datetime

class PublicHomeView(View):

    template_name = 'zo/public/index.html'

    def get(self, request, *args, **kwargs):

        return render(
            request,
            self.template_name,
            {
                'title':'Home Page',
                'year':datetime.now().year,
            }
        )

class PublicAboutView(View):

    template_name = 'zo/public/about.html'

    def get(self, request, *args, **kwargs):
        """Renders the about page."""
        #assert isinstance(request, HttpRequest)
        return render(
            request,
            self.template_name,
            {
                'title':'About',
                'message':'Your application description page.',
                'year':datetime.now().year,
            }
        )

class PublicContactView(GenericContactView):

    pass

class PublicSignUpView(GenericContactView):

    title = 'User & Hub Sign Up'
    forms = [UserSignUpContactForm, UserHubSignUpContactForm]
    message = []

class PublicLoginView(LoginView):

    template_name='zo/login.html'
    authentication_form=BootstrapAuthenticationForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Log in'
        context['year'] = datetime.now().year
        return context