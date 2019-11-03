from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from datetime import datetime

from zo.models import UserTemporaryPassword

class UserSettingsView(LoginRequiredMixin, View):

    template_name = 'zo/user/settings.html'

    def get(self, request, *args, **kwargs):

        if UserTemporaryPassword.objects.filter(user=self.request.user):
            temporary = True
        else:
            temporary = False

        return render(
            request,
            self.template_name,
            {
                'title':'Home Page',
                'year':datetime.now().year,
                'temporary':temporary,
            }
        )
