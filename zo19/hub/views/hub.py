from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from zo.views.generic.permission import TempPasswordCheck

from hub.models.hub import Hub

from datetime import datetime

class HubView(LoginRequiredMixin, TempPasswordCheck, View):

    template_name = 'hub/hub/index.html'

    def get(self, request, pk, hub_name, *args, **kwargs):

        hub = Hub.objects.all().get(pk=pk)

        return render(
            request,
            self.template_name,
            {
                'title':'Hub View',
                'hub':hub,
                'year':datetime.now().year,
            }
        )
