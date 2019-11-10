from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from zo.forms.public import PasswordResetForm
from zo.views.generic import StaffView
from zo.models import User, UserPasswordReset

from datetime import datetime

class PasswordRequestView(CreateView):
    
    '''
    '''

    model = UserPasswordReset
    template_name = 'zo/generic/createview.html'
    fields = ['email']

    title = 'Password Reset Request'
    layout = 'zo/public'
    submit_text = 'Submit Request'
    message = ['If you need to reset your password, please enter your email address and we will email a reset link.']

    def get(self, request, *args, user_check=True, **kwargs):

        if not user_check:
            self.message = ['This email is not one that belongs to a ZO-SPORTS User.']

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = self.title 
        context['layout'] = '%s/layout.html' % self.layout
        context['year'] = datetime.now().year
        context['submit_text'] = self.submit_text
        context['message'] = self.message

        return context

    def form_valid(self, form):
 
        self.object = form.save(commit=False)
        
        reset_check = UserPasswordReset.objects.filter(email=self.object.email)
        user_check = User.objects.filter(email=self.object.email)
        
        if user_check:
            
            self.object.user = user_check[0]
            self.object.random = User.objects.make_random_password()
            
            if reset_check:
                reset_check[0].contact_user()
                return self.post_redirect(title='Password Reset Re-sent', message='Your password reset link has been re-emailed to you')
            else:
                self.object.save()
                self.object.contact_user()
                return self.post_redirect(title='Password Reset Sent', message='Your password reset link has been emailed to you')

        else:

            return self.get(self.request, user_check=False)

    def post_redirect(self, title='', message=''):

        ''' '''

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':title,
                'message': message,
                'year':datetime.now().year,
            }
        )

class PasswordResetView(FormView):

    form_class = PasswordResetForm
    template_name = 'zo/generic/createview.html'

    title = 'Password Reset'
    layout = 'zo/public'
    submit_text = 'Reset'
    message = []

    def get(self, request, message=None, **kwargs):

        id = self.kwargs['id']
        random = self.kwargs['random']

        reset_check = UserPasswordReset.objects.filter(id=id, random=random)
        if reset_check:
            user = reset_check[0].user.__str__()

            if message == None:
                self.message = ['%s, enter your new password.' % user]
            else:
                self.message = [message]

            return render(
                self.request,
                self.template_name,
                {
                    'layout':'%s/layout.html' % self.layout,
                    'title':self.title,
                    'message': self.message,
                    'year':datetime.now().year,
                    'form':PasswordResetForm, 
                    'submit_text':self.submit_text,
                    'year':datetime.now().year,
                }
            )


        else:

            return render(
                self.request,
                'zo/generic/action_message.html' ,
                {
                    'title':'Error',
                    'message':'''This link has no current password reset request. 
                    Please check the link, 
                    or request a new password reset, 
                    or use the general contact form to contact ZO-SPORTS.''',
                    'layout':'%s/layout.html' % self.layout,
                    'submit_text':None,
                    'year':datetime.now().year,
                }
            )

    def form_valid(self, form):

        id = self.kwargs['id']
        random = self.kwargs['random']

        reset = UserPasswordReset.objects.filter(id=id, random=random)[0]
        user = reset.user

        f = form.cleaned_data

        p1 = f['new_password']
        p2 = f['confirm_password']

        if p1 == p2:
            reset.delete()
            user.set_password(p1)
            user.save()        
            return self.post_redirect()

        return self.get(self.request, message='Those passwords did not match')




    def post_redirect(self):

        ''' '''

        return render(
            self.request,
            'zo/generic/action_message.html' ,
            {
                'layout':'%s/layout.html' % self.layout,
                'title':'Success',
                'message': 'Your password has been successfully changed',
                'year':datetime.now().year,
            }
        )