from django.db import models
from django.conf import settings 

from .user import UserName, UserTemporaryPassword

class UserSignUp(models.Model):

    ''' Creates a record of a request to create a new User. This record can be declined (and 
    therefore the instance deleted) or accepted and the self.process_signup() method 
    will process the signup and email the User (and then the instance should be deleted). '''

    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)

    def process_signup(self):

        ''' The primary method used in all inheritances to process each signup. '''

        self.create_user()
        self.create_email_message()
        self.send_email()

    def create_user(self):

        ''' Create a random temporay password, create a User with basic information 
        and assign that password. Create a UserName with basic information and link to 
        the User. Send an email to the User which gives them their log in details. '''

        self.password = settings.AUTH_USER_MODEL.objects.make_random_password()

        self.user = settings.AUTH_USER_MODEL(email=self.email, is_staff=self.is_staff, phone_number=self.phone)
        self.user.set_password(self.password)
        self.user.save()

        name = UserName(firstname=self.firstname, surname=self.surname)
        name.user = user
        name.save()

        temp = UserTemporaryPassword(password=self.password, user=self.user)
        temp.save()

    def create_email_message(self):

        ''' Creates a self.email_message with log in details, 
        which can be sent to the new User.'''

        self.email_subject = 'ZO-SPORTS Login Details'

        self.email_message = 'Hi %s,\n\n' % self.firstname
        self.email_message += 'You can now log in at www.zo-sports.com/login '
        self.email_message += 'using the following details:\n\n'
        self.email_message += 'Username: %s\nTemporary Password: %s\n\n' % (self.email, self.password)
        self.email_message += 'When you first log in, you will be asked to set a new password '
        self.email_message += 'and complete some of your profile.'
        self.email_message += 'n\nWelcome to ZO-SPORTS.'

    def send_email(self):

        ''' Sends an email to the User with details of their successful signup. '''

        self.user.email_user(self.email_subject, self.email_message)

class UserHubSignUp(UserSignUp):

    ''' Creates a record of a request to create a new User and Hub. This record can be declined (and 
    therefore the instance deleted) or accepted and the self.process_signup() method 
    will process the signup and email the User (and then the instance should be deleted). '''

    #hub_type = models.ForeignKey(to='hub.HubType', on_delete=models.CASCADE)
    hub_name = models.CharField(max_length=30)
    hub_phone = models.CharField(max_length=30)
    hub_street = models.CharField(max_length=50)
    hub_towncity = models.CharField(max_length=50)

    def process_signup(self):

        ''' The primary method used in all inheritances to process each signup. '''

        self.create_user()
        self.create_hub()
        self.create_email_message()
        self.send_email()

    def create_hub(self):

        ''' '''

        self.hub = None

    def create_email_message(self):

        ''' Creates a self.email_message with log in details,
        and Hub confirmation, which can be sent to the new User.'''

        self.email_subject = 'ZO-SPORTS Login and Hub Confirmation'

        self.email_message = 'Hi %s,\n\n' % self.firstname
        self.email_message += 'You can now log in at www.zo-sports.com/login '
        self.email_message += 'using the following details:\n\n'
        self.email_message += 'Username: %s\nTemporary Password: %s\n\n' % (self.email, self.password)
        self.email_message += 'When you first log in, you will be asked to set a new password '
        self.email_message += 'and complete some of your profile, before you are fully signed up.'

        self.email_message += '\n\n%s has also been added as a Hub in the ZO-SPORTS system ' % self.hub
        self.email_message += 'and you have been listed as the Main Contact. '
        self.email_message += 'You can access %s through the Hub tab when you are fully signed up.' % self.hub

        self.email_message += '\n\nWelcome to ZO-SPORTS.'

class HubSignUp(UserHubSignUp):

    ''' Creates a record of a request to create a Hub. This record can be declined (and 
    therefore the instance deleted) or accepted and the self.process_signup() method 
    will process the signup and email the User (and then the instance should be deleted). 
    Inherits from UserHubSignUp but mostly only uses the Hub parts of that model.'''

    firstname = None
    surname = None
    phone = None
    is_staff = None

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def create_user(self):

        ''' Creates self.email and self.firstname values, from the self.user model, 
        so that they can be used in the email to be sent to the User. '''

        self.email = self.user.email
        self.firstname = self.user.name.firstname

    def create_email_message(self):

        ''' Creates a self.email_message with Hub confirmation, 
        which can be sent to the User.'''

        self.email_subject = 'ZO-SPORTS Hub Confirmation'

        self.email_message = 'Hi %s,\n\n' % self.firstname

        self.email_message += '\n\n%s has been added as a Hub in the ZO-SPORTS system ' % self.hub
        self.email_message += 'and you have been listed as the Main Contact. '
        self.email_message += 'You can access %s through the Hub tab when you sign in.' % self.hub

        self.email_message += '\n\nKind regards, ZO-SPORTS.'
