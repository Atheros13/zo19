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
    message = ['Enter your new password.']

    def get(self, request, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = self.title 
        context['layout'] = '%s/layout.html' % self.layout
        context['year'] = datetime.now().year
        context['submit_text'] = None
        context['message'] = self.message

        return context

        id = self.kwargs['id']
        random = self.kwargs['random']

        reset_check = UserPasswordReset.objects.filter(id=id, random=random)
        if reset_check:
            user = reset_check[0].user
            reset_check[0].delete()

            context = super().get_context_data(**kwargs)

            context['user'] = user

            context['submit_text'] = self.submit_text
            context['message'] = ['Enter your new password.']

            return context

        else:

            return self.post_redirect(title='Error',
                                      message='''This link has no current password reset request. 
                                      Please check the link, 
                                      or request a new password reset, 
                                      or use the general contact form to contact ZO-SPORTS.''')

    def form_valid(self, form):
    
        return super().form_valid(form)

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