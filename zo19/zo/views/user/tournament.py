from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from zo.views.generic.permission import TempPasswordCheck

from datetime import datetime


from django.forms import ModelForm
from zo.models.test import AnotherTest

class TestForm(ModelForm):

    class Meta:
        model = AnotherTest
        fields = ['distance', 'yearless']

class UserTournamentsView(View):

    template_name = 'zo/public/test.html'

    def get(self, request, *args, **kwargs):

        test = AnotherTest.objects.all()[0]

        t = TestForm(instance=test)


        return render(
            request,
            self.template_name,
            {
                'title':'Tournaments',
                'message': 'Tournament stuff goes here',
                'year':datetime.now().year,
                'form':t,
            }
        )

    def post(self, *args, **kwargs):

        print(args, kwargs)

        t = TestForm(self.request.POST)

        print(t.instance)

        if t.is_valid():
            print(t.cleaned_data)
            t.save()

        return self.get(self.request)