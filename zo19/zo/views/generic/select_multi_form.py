from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest

from django.views import View

from datetime import datetime

class SelectMultiFormView(View):

    template_name = 'zo/generic/select_multi_form.html'
    form = None

    title = ''
    forms = []
    extra_actions = []
    layout = ''
    message = []

    def get(self, *args, **kwargs):

        return render(
            self.request,
            self.template_name,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':self.title,
                'forms': self.forms,
                'extra_actions': self.extra_actions,
                'form': self.form,
                'message':self.message,
                'year':datetime.now().year,
            }
        )

    def post(self, *args, **kwargs):

        # checks buttons that bring up forms
        for f in self.forms:
            if self.request.POST.get('Form Choice %s' % f.title):
                self.form = f
            #
            elif self.request.POST.get(f.title):
                form = f(self.request.POST)
                if form.is_valid():
                    # returns True if process was successful or returns the form itself (with errors added)
                    form_check = form.process_form(self.request)
                    if form_check == True:
                        return self.success(f)
                    else:
                        self.form = form_check

        # processes any buttons which do another action, i.e. redirect to a password change request page
        for e in self.extra_actions:
            if self.request.POST.get('Action Choice %s' % e.title):
                return e().process_action(self.request)
       
        return self.get()

    def success(self, form):

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':'Success',
                'message':'Your %s form has been successfully sent' % form.title,
                'year':datetime.now().year,
            }
        )