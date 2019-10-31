from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.list import ListView

from zo.models.signup import UserSignUp, UserHubSignUp, HubSignUp

from datetime import datetime

class ZoAdminConfirmSignUpView(ListView):

    template_name = 'zo/public/index.html'

    def get(self, request, *args, type=None, id=None, **kwargs):

        if type == None:
        
            pass

        elif type == 'user':

            pass

        elif type == 'user_hub':

            pass

        elif type == 'hub':

            pass

    def get_user(self, id):

        pass

    def get_user_hub(self, id):

        pass

    def get_hub(self, id):

        pass

class ConfirmSignUpUserView(ListView):

    model = UserSignUp

class ConfirmSignUpUserHubView(ListView):

    model = UserHubSignUp

class ConfirmSignUpHubView(ListView):

    model = HubSignUp