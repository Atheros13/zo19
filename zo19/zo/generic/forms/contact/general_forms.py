from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError


class GeneralContactForm(forms.Form):

    title = 'General'
    description = 'Click to send a general message'

    name = forms.CharField(label='Name', max_length=30, required=True)
    email = forms.EmailField(label="Email Address", required=True)
    phone = forms.CharField(label="Phone Number", max_length=30, required=False)
    message = forms.CharField(label='Message', widget=forms.Textarea(), required=True)

    def process_contact(self, user=False, hub=False, tournament=False):
        
        f = self.cleaned_data

        email = 'none@none.com'
        if f['email']:
            email = f['email']
        elif user:
            email = user.email
        
        subject = '%s Contact' % self.title

        message = 'Name: %s\n' % f['name']
        if f['phone']:
            message += 'Phone: %s\n\n' % f['phone']
        message += f['message']
        
        send_mail(subject, message, email, ['info@zo-sports.com'])

        return True, 'error message'

class GeneralUserContactForm(GeneralContactForm):

    title = 'General'
    description = 'Click to send a general message'

    # need to change name so it auto populates with user.__str__()
    name = forms.CharField(label='Name', max_length=30, required=True)

    def process_contact(self, *args, **kwargs):

        return True, 'error message'

class TechnicalContactForm(GeneralContactForm):

    title = 'Technical'
    description = 'Click for technical issues, please include as much information as possible'

    def process_contact(self, *args, **kwargs):

        return True, 'error message'

