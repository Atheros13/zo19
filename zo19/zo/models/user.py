from __future__ import unicode_literals
from django.db import models
from django.conf import settings 
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import ugettext_lazy as _

from .abstract import Address, NamePerson

class UserManager(BaseUserManager):
    
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    ''' '''

    ### IN ATTRIBUTES ###
    # name

    ## OWN ATTRIBUTES
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True)
    phone_number = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # is ZO-SPORTS staff i.e. can access /admin
    is_authorised = models.BooleanField(default=False) # Authorised/Verified User - create Hubs/Tournaments

    ## OUT ATTRIBUTES
    gender = models.ForeignKey(to='zo.Gender', on_delete=models.SET_NULL, null=True, related_name='users')

    ### MISC ###
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    ### META DATA ###
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        
    def __str__(self):
        try:
            return self.name.__str__()
        except:
            return self.email

    ### FUNCTIONS ###
    def email_user(self, subject, message, from_email='no-reply@zo-sports.com', **kwargs):
        
        ''' Sends an email to this User. '''

        send_mail(subject, message, from_email, [self.email])

#

class UserName(NamePerson):

    ''' A NamePerson inherited model, for use with a User. '''

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE, related_name='name')

class UserAddress(Address):

    ''' An Address inherited model, for use with a User. '''

    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE, related_name='address')

class UserTemporaryPassword(models.Model):

    password = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE, related_name='temporary_password')

class UserPasswordRequest(models.Model):

    ''' '''

    email = models.EmailField()
    user = models.OnToOneField(User, on_delete=models.CASCADE)

    def contact_user(self):

        message = 'Hi %s,\n\n' % self.user.name
        message += 'You have requested to reset the password to your ZO-SPORTS login. '
        message += 'The link to reset your password is below:\n\n'
        message += 'www.zo-sports.com/password/reset/13%s \n\n' % self.id
        message += 'If you did not request this reset, please ignore this email or if '
        message += 'you are concerned about security, contact ZO-SPORTS through the website.'
        message += '\n\nKind regards,\n\nZO-SPORTS'

        self.user.email_user('ZO-SPORTS Password Reset', message)

