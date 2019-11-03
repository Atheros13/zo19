from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest

from django.views import View
from zo.forms.generic import GeneralContactForm

from datetime import datetime

class GenericContactView(View):

    template_name = 'zo/generic/contact.html'
    form = None

    title = 'General Contact'
    forms = [GeneralContactForm]
    layout = 'zo/public'
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
                'form': self.form,
                'message':self.message,
                'error_message': self.error_message,
                'year':datetime.now().year,
            }
        )

    def post(self, *args, **kwargs):

        for f in self.forms:
            if self.request.POST.get('Form Choice %s' % f.title):
                self.form = f
                return self.get()
            elif self.request.POST.get(f.title):
                contact_form = f(self.request.POST)
                if contact_form.is_valid():
                    check, error_message = contact_form.process_form()
                    if check:
                        return self.contact_success(f)
                    else:
                        self.error_message = error_message
                else:
                    self.error_message = []

                self.form = f
                return self.get()

    def contact_success(self, form):

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':'Success',
                'message':'Your %s Contact form has been successfully sent' % form.title,
                'year':datetime.now().year,
            }
        )