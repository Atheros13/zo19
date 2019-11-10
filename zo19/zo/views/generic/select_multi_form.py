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
    form_type = ''
    layout = ''
    message = []
    error_message = []

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
                'error_message': self.error_message,
                'year':datetime.now().year,
            }
        )

    def post(self, *args, **kwargs):

        # processes any buttons which choose a form
        for f in self.forms:
            if self.request.POST.get('Form Choice %s' % f.title):
                self.form = f
                return self.get()
            elif self.request.POST.get(f.title):
                contact_form = f(self.request.POST)
                if contact_form.is_valid():
                    check, error_message = contact_form.process_form(self.request)
                    if check:
                        return self.contact_success(f)
                    else:
                        self.error_message = error_message
                else:
                    self.error_message = []

                self.form = f(self.request.POST)
                return self.get()

        # processes any buttons which do another action, i.e. redirect to a password change request page
        for e in self.extra_actions:
            if self.request.POST.get('Action Choice %s' % e.title):
                return e().process_action(self.request)

    def contact_success(self, form):

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':'Success',
                'message':'Your %s %s form has been successfully sent' % (form.title, self.form_type),
                'year':datetime.now().year,
            }
        )